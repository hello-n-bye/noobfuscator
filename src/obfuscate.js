// src/obfuscate.js
// Renames variables, function names -> turns `local function` into `function`.

// Average obfuscation-time: ~0.667s


const fs = require("fs");
const { exec } = require("child_process");

const path = "./poop.lua";
const configuration = "./config.json";

function encryptString(str) {
   let encrypted = str.split('').map(char => '\\x' + char.charCodeAt(0).toString(16)).join('');
   return encrypted;
}

function obfuscate(lua) {
   let names = lua.match(/(?<=local |function |^)([a-zA-Z_][a-zA-Z0-9_]*)\b/g);

   console.log("Starting obfuscation process...");

   let used = new Set();
   names.forEach((name) => {
      if (name !== "function" && name !== "local") {
         let converted;

         do {
            let num = Math.floor(Math.random() * 10) + 1;
            converted = "_".repeat(num);
         } while (used.has(converted));

         used.add(converted);

         let regex = new RegExp("\\b" + name + "\\b", "g");
         lua = lua.replace(regex, (match, offset, string) => {
            let left = string.slice(0, offset);
            let right = string.slice(offset + match.length);

            if ((left.match(/"/g) || []).length % 2 === 0 && (right.match(/"/g) || []).length % 2 === 0) {
               return converted;
            } else {
               return match;
            }
         });
      }
   });

   lua = lua.replace(/"([^"]*)"/g, (match, str) => {
      return '"' + encryptString(str) + '"';
   });

   return lua;
}


console.log("Reading the config file...");
fs.readFile(configuration, "utf8", (err, configJson) => {
   if (err) {
      console.error(`Error reading the config file: ${err}`);
      return;
   }

   let config = JSON.parse(configJson);
   let obfuscationString = `--> Obfuscated with ${config.name} ${config.version} <--\n\n`;

   console.log("Running minifier on the source-file...");
   exec(`node src/minifier.js ${path}`, (err) => {
      if (err) {
         console.error(`Error running minifier: ${err}`);
         return;
      }

      console.log("Reading the source-file...");
      fs.readFile(path, "utf8", (err, lua) => {
         if (err) {
            console.error(`Error reading the file: ${err}`);
            return;
         }

         let obfuscated = obfuscationString + obfuscate(lua);

         console.log("Writing the obfuscated file...");
         fs.writeFile(path, obfuscated, "utf8", (err) => {
            if (err) {
               console.error(`Error writing the file: ${err}`);
               return;
            }

            console.log(`File obfuscated successfully. Changes saved to ${path}`);
         });
      });
   });
});
