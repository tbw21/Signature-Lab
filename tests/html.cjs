"use strict";
function moduleCode(html) {
 const scripts=[...html.matchAll(/<script\b([^>]*)>([\s\S]*?)<\/script\s*>/gi)];
 if(scripts.length!==1 || !/\btype\s*=\s*["']module["']/i.test(scripts[0][1]) || /\bsrc\s*=/i.test(scripts[0][1])) throw Error('Expected one inline module');
 return scripts[0][2];
}
function csp(html) {
 const tags=[...html.matchAll(/<meta\b[^>]*>/gi)].map(x=>x[0]).filter(t=>/http-equiv=["']Content-Security-Policy["']/i.test(t));
 if(tags.length!==1)throw Error('Expected one CSP');
 const value=tags[0].match(/\bcontent="([^"]*)"/i);if(!value)throw Error('CSP content missing');return value[1];
}
module.exports={moduleCode,csp};
