const test = require('node:test');
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const {search} = require('../web/search.js');
const data = path.join(__dirname, '../data');
const entries = fs.readdirSync(data).filter(x=>x.endsWith('.json')).flatMap(file=>JSON.parse(fs.readFileSync(path.join(data,file),'utf8')));

test('all entries returned for empty query',()=>assert.equal(search(entries,'').length,entries.length));
test('every exact error is found and ranks at the top',()=>{
  for(const e of entries) assert.equal(search(entries,e.error)[0].error,e.error,e.id);
});
test('timestamp and path prefixes do not hide recognized error',()=>{
  for(const e of entries) assert(search(entries,`[10:00:00] /project/main.py: ${e.error}\nfailed`).some(x=>x.id===e.id),e.id);
});
test('category restricts full text results',()=>{
  for(const cat of ['ci','tls','permissions','packages']) {
    const found=search(entries,'',cat);assert(found.length>0);assert(found.every(e=>e.category===cat));
  }
});
test('unrelated input returns zero',()=>assert.equal(search(entries,'unmatched-phrase-7f8629').length,0));
test('error code search is case insensitive',()=>{
  assert(search(entries,'eresolve').some(e=>e.error.includes('ERESOLVE')));
});
test('curly quotes match ordinary quotes',()=>{
  const e=entries.find(e=>e.error.includes("'"));
  if(e) assert(search(entries,e.error.replace(/'/g,'’')).some(x=>x.id===e.id));
});
test('catalog text is interpreted as plain data',()=>{
  const e={...entries[0],id:'hostile',summary:'<script>alert(1)</script>'};
  assert.equal(search([e],'alert')[0].id,'hostile');
});
