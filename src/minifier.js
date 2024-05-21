// Path: src/index.js
// Minified ../input.lua --> The source-file.

const fs = require('fs');
const luamin = require('luamin');

const input = './source.lua';
const loadedFile = fs.readFileSync(input, 'utf8');

const minified = luamin.minify(loadedFile);

const output = './poop.lua';

fs.writeFileSync(output, minified, 'utf8');

console.log(`Minified ${input} --> ${output}`);