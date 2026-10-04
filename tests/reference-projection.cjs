'use strict';
// Test-only projection of declared additions, never used by the build/application.
const fs=require('fs'),path=require('path'),assert=require('assert/strict');
const record=JSON.parse(fs.readFileSync(path.resolve(__dirname,'../fixtures/reference-projection.json'),'utf8'));
exports.project=(name,text)=>{text=require("./clarity-projection.cjs").project(name,text);for(const e of [...(record.edits[name]||[])].reverse()){assert.equal(text.split(e.after).length-1,1,'Nonunique declared reversal '+name);text=text.replace(e.after,e.before);}return text;};
