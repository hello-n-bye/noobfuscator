// src/obfuscate.js
// Average obfuscation-time: ~2s

const fs = require("fs");
const { exec } = require("child_process");

// function getRandomComment() {
//    const data = JSON.parse(fs.readFileSync("./ignore-me.json", "utf8"));

//    const types = Object.keys(data.comments);
//    const randomType = types[Math.floor(Math.random() * types.length)];

//    const quotes = data.comments[randomType];
//    const randomQuote = quotes[Math.floor(Math.random() * quotes.length)];

//    return randomQuote;
// }

const path = "./poop.lua";
const configuration = "./config.json";

function encryptString(str) {
   let encrypted = str.split("").map(char => "\\x" + char.charCodeAt(0).toString(16)).join("");
   return encrypted;
}

function getRandomUselessCode() {
   const data = JSON.parse(fs.readFileSync("./ignore-me.json", "utf8"));
   const types = data.code;

   const randomIndex = Math.floor(Math.random() * types.length);
   let uselessCode = types[randomIndex];

   const variableNameLength = Math.floor(Math.random() * 10) + 5;
   const possibleCharacters = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz";

   let variableName = "";
   for (let i = 0; i < variableNameLength; i++) {
      variableName += possibleCharacters.charAt(Math.floor(Math.random() * possibleCharacters.length));
   }

   uselessCode = uselessCode.replace(/_/g, variableName);
   uselessCode = uselessCode.replace(/(['"])(.*?)\1/g, (match, p1, p2) => `${p1}${encryptString(p2)}${p1}`);

   return uselessCode;
}

function obfuscate(lua) {
   let names = lua.match(/(?<=local |function |^)([a-zA-Z_][a-zA-Z0-9_]*)\b/g);

   console.log("Starting obfuscation process...");

   let used = new Set();
   let luaKeywords = ["and", "break", "do", "else", "elseif", "end", "false", "for", "function", "if", "in", "local", "nil", "not", "or", "repeat", "return", "then", "true", "until", "while"];
   names.forEach((name) => {
      if (!luaKeywords.includes(name)) {
         let converted;

         do {
            const variableNameLength = Math.floor(Math.random() * 10) + 5;
            const possibleCharacters = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz";

            converted = "";
            for (let i = 0; i < variableNameLength; i++) {
               converted += possibleCharacters.charAt(Math.floor(Math.random() * possibleCharacters.length));
            }
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

   const lines = lua.split('\n');
   for (let i = 0; i < lines.length; i++) {
      const numberOfUselessLines = Math.floor(Math.random() * 1000) + 1;
      for (let j = 0; j < numberOfUselessLines; j++) {
         const uselessCode = getRandomUselessCode();
         lines[i] += ' ' + uselessCode;
      }
   }
   lua = lines.join('\n');
   
   lua = lua.replace(/"([^"]*)"/g, (match, str) => `"${encryptString(str)}"`);
   // lua = lua.replace(/\b(local|==|do|;)\b/g, (match) => {
   //    if (Math.random() > 0.1) {
   //       return `${match}--[[${getRandomComment()}]]`;
   //    } else {
   //       return match;
   //    }
   // });
   lua = lua.replace(/\b(end|;)\b/g, (match) => `${match} ${getRandomUselessCode()}`);

   return lua;
}

console.log("Reading the config file...");
fs.readFile(configuration, "utf8", (err, configJson) => {
   if (err) {
      console.error(`Error reading the config file: ${err}`);
      return;
   }

   let config = JSON.parse(configJson);

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

         let obfuscated = `([[(_Obfuscated With ${config.name}-${config.version}_)]]):gsub("-", (function(...) ${obfuscate(lua)} end))`;

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
