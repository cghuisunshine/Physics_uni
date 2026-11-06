const {test}=require('node:test');
const assert=require('node:assert/strict');
const fs=require('node:fs');
const path=require('node:path');
const {JSDOM}=require('jsdom');
const root=path.resolve(__dirname,'../..');
const catalog=JSON.parse(fs.readFileSync(path.join(root,'content/math-expressions.json'),'utf8'));
const fixture=new JSDOM(fs.readFileSync(path.join(root,'tools/review/fixtures/math-layout.html'),'utf8')).window.document;
const blocks=new Map([...fixture.querySelectorAll('[data-check]')].map(e=>[e.dataset.check,e]));

test('all 660 expressions have rendered math, original copy text, and accessible MathML',()=>{
  assert.equal(catalog.length,660);
  assert.equal(blocks.size,catalog.length);
  assert.equal(fixture.querySelectorAll('.katex-error').length,0);
  for(const row of catalog){
    const block=blocks.get(`${row.topic}/${row.location}`);
    assert.equal(block.querySelector('.equation-value').dataset.plainMath,row.source);
    assert.ok(block.querySelector('.katex-html[aria-hidden=true]'));
    assert.ok(block.querySelector('math semantics'));
    const annotation=block.querySelector('annotation[encoding="application/x-tex"]').textContent;
    for(const part of row.tex.split(';')) assert.ok(annotation.includes(part),`${row.topic}/${row.location}`);
    assert.ok(block.querySelector('.equation-value').getAttribute('href').endsWith(`#proof-${row.location}`));
  }
});

function math(topic,location){return blocks.get(`${topic}/${location}`).querySelector('math');}
test('grouped powers, lower indices, integral limits and exponential arguments keep their structure',()=>{
  const adiabatic=math('adiabatic-gas','main');
  assert.ok([...adiabatic.querySelectorAll('msup')].some(e=>e.lastElementChild.textContent==='γ−1'));
  const carnot=math('carnot','step-3');
  assert.equal([...carnot.querySelectorAll('msup,msubsup')].filter(e=>e.lastElementChild.textContent==='γ−1').length,4);
  const integral=math('constant-acceleration','step-1').querySelector('msubsup');
  assert.equal(integral.children[0].textContent,'∫');assert.equal(integral.children[1].textContent,'0');assert.equal(integral.children[2].textContent,'t');
  const tunnel=math('tunneling','step-2');
  assert.deepEqual([...tunnel.querySelectorAll('msup')].map(e=>e.lastElementChild.textContent),['κx','−κx']);
  assert.ok([...math('planck-radiation','step-4').querySelectorAll('msup')].some(e=>e.firstElementChild.textContent==='e'&&e.lastElementChild.textContent==='x'));
  assert.ok([...math('rc-circuit','main').querySelectorAll('msup')].every(e=>e.lastElementChild.textContent==='−t/(RC)'));
  assert.ok(math('equipartition','step-2').querySelector('mfrac mfrac'));
});

test('every declared math font and stylesheet is local and present',()=>{
  const css=fs.readFileSync(path.join(root,'assets/math/katex.min.css'),'utf8');
  const urls=[...css.matchAll(/url\(([^)]+)\)/g)].map(m=>m[1].replaceAll('"','').replaceAll("'",''));
  assert.ok(urls.length>20);
  for(const file of urls){assert.ok(!file.includes('://'));assert.ok(fs.statSync(path.join(root,'assets/math',file)).size>0,file);}
  assert.ok(fs.existsSync(path.join(root,'assets/math/LICENSE')));
  for(const link of fixture.querySelectorAll('link[rel=stylesheet]')) assert.ok(fs.existsSync(path.resolve(root,'tools/review/fixtures',link.getAttribute('href'))));
});
