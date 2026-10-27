const test=require('node:test'),assert=require('node:assert/strict');
const {serialize}=require('./review-text.js');
function row(text,x,y,size=9,firstId=0){return [...text].map((text,i)=>({id:firstId+i,text,x:x+i*4.5,end:x+(i+1)*4.5,y,size}));}
test('copy preserves words and inserts spaces between independently styled spans',()=>{
 const glyphs=[...row('SI Units',60,20,10),...row('The unit system',110,20,9,20),...row('is used in physics.',60,31,9,50)];
 assert.equal(serialize(glyphs,[],330),'SI Units The unit system\nis used in physics.');
});
test('copy reads the entire left column before the right column',()=>{
 const glyphs=[...row('Right column',340,20,9,30),...row('Left column',60,20),...row('Second line',60,31,9,60)];
 assert.equal(serialize(glyphs,[],330),'Left column\nSecond line\n\nRight column');
});
test('density equation copies with a real rho and a readable fraction',()=>{
 const glyphs=[{id:1,text:'ρ',x:444,y:481,size:9,end:449},{id:2,text:'=',x:451,y:481,size:9,end:458},{id:3,text:'m',x:464,y:474.7,size:9,end:471},{id:4,text:'V',x:464,y:487.3,size:9,end:471}];
 const fractions=[{above:[3],below:[4],x:461,end:473,y:481,size:9}];
 assert.equal(serialize(glyphs,fractions,330),'ρ = m/V');
});
test('a partial fraction selection never introduces unselected text',()=>{
 const glyphs=[{id:3,text:'m',x:464,y:474.7,size:9,end:471}];
 assert.equal(serialize(glyphs,[{above:[3],below:[4],x:461,end:473,y:481,size:9}],330),'m');
});
test('copy preserves superscripts and subscripts',()=>{
 const glyphs=[...row('v = x',60,40,9),{id:50,text:'2',x:83,y:36,size:5.8,end:86},...row('m',100,60,9,70),{id:71,text:'0',x:105,y:63,size:5.8,end:108}];
 assert.equal(serialize(glyphs,[],330),'v = x²\nm₀');
});
test('typographic ligatures copy as ordinary searchable characters',()=>{
 assert.equal(serialize(row('ﬂux ﬁeld',60,20),[],330),'flux field');
});
