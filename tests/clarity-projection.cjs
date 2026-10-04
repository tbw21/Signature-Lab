'use strict';
const fs=require('fs'),path=require('path'),assert=require('assert/strict');
const record=JSON.parse(fs.readFileSync(path.resolve(__dirname,'../fixtures/clarity-projection.json'),'utf8'));
exports.project=(name,text)=>{text=require("./audit-projection.cjs").project(name,text);for(const e of [...(record.edits[name]||[])].reverse()){assert(e.after&&text.split(e.after).length-1===1,'Nonunique clarity reversal '+name);text=text.replace(e.after,e.before);}return text;};
