const test=require('node:test'),assert=require('node:assert/strict'),fs=require('node:fs'),vm=require('node:vm');
const FQ=require('./physics-followup.js');
const ui=fs.readFileSync(__dirname+'/physics-followup-ui.js','utf8');
const core=fs.readFileSync(__dirname+'/physics-practice-core.js','utf8');
const question={text:'A 2.0 kg trolley accelerates at 3.0 m/s². What is its net force?',choices:['1.5 N','6.0 N','5.0 N','0.67 N','12 N'],answer:'B',explanation:'Use F = ma, as in the original solution: (2.0 kg)(3.0 m/s²) = 6.0 N. Check: kg·m/s² is a newton.'};
const flush=()=>new Promise(setImmediate);
function element(){return {hidden:true,disabled:false,checked:false,textContent:'',children:[],attributes:{},classList:{add(){},toggle(){}},setAttribute(k,v){this.attributes[k]=v;},replaceChildren(...children){this.children=children;},append(...children){this.children.push(...children);}};}
function fixture(options={}){
 const elements=new Map(),storage=new Map(),requests=[];
 if(options.enabled!==undefined)storage.set('physicsUniPracticeFollowUp',String(options.enabled));
 const problem={id:'uni-ch5-p1',kind:options.kind||'textbook',chapterNumber:5,chapterTitle:'Force and Motion—I',number:1,title:'Problem 1 · Newton’s laws',topic:'Ch 5 · 5-1',topicTitle:'Newton’s laws',level:1,html:'Find the net force on the original trolley.',solution:'Use F = ma.',answer:'See worked solution'};
 const attempt={id:problem.id,kind:problem.kind,topic:problem.topic,level:1,title:problem.title,choice:'3 N',correct:options.correct===true,review:false,assessment:'self',seconds:1,at:new Date().toISOString()};
 const context={window:{PhysicsFollowUp:FQ},Date,AbortController,DOMException,setTimeout:options.setTimeout||setTimeout,clearTimeout:options.clearTimeout||clearTimeout,navigator:{onLine:options.online!==false},live:{role:options.role||'idle'},student:'Alice',checked:true,activeAttempt:attempt,current:problem,
  state:{version:1,attempts:[attempt],items:{[problem.id]:{problem,manual:false,missed:!attempt.correct}}},
  document:{createElement:element},$:id=>{if(!elements.has(id))elements.set(id,element());return elements.get(id);},
  localStorage:{getItem:k=>storage.get(k)??null,setItem:(k,v)=>storage.set(k,v)},AI:{endpoint:'https://example.test/tutor'},
  readableHTML:s=>s,questionAndWorkingImage:async()=>({image:'reference-images',mime_type:'image/jpeg',filename:'reference.jpg'}),saved:0,save(){context.saved++;},
  fetch:(...args)=>{requests.push(args);return options.fetch?options.fetch(...args):Promise.resolve({ok:true,json:async()=>({response:question})});}
 };
 vm.createContext(context);vm.runInContext(core,context);context.window.Practice.configure([problem]);vm.runInContext(ui,context);
 return {c:context,$:context.$,requests,attempt,problem,storage};
}
test('protocol validates envelopes, choices, answer keys and complete explanations',()=>{
 for(const envelope of [question,{response:question},{response:'```json\n'+JSON.stringify(question)+'\n```'}])assert.equal(FQ.parseResponse(envelope).answer,'B');
 for(const bad of [{...question,answer:'F'},{...question,answer:''},{...question,choices:['1','2','2','4','5']},{...question,choices:['1','2']},{...question,explanation:''},{response:'broken JSON'},{ok:false}])assert.throws(()=>FQ.parseResponse(bad));
 assert.throws(()=>FQ.parseResponse(question,question.text),/repeated/);
});
test('only enabled missed textbook attempts can generate follow-up practice',async()=>{
 for(const options of [{},{enabled:false},{correct:true},{kind:'generated'},{role:'follower'}]){
  const f=fixture(options);await f.c.startFollowUp();
  const expected=!options.correct&&options.enabled!==false&&!options.kind&&!options.role;
  assert.equal(f.requests.length,expected?1:0);assert.equal(f.$('followup').hidden,!expected);
  if(expected){assert.equal(f.$('followup-choices').children.length,5);assert.equal(f.$('followup-check').disabled,true);}
 }
});
test('request uses the specific missed problem, worked solution and original images',async()=>{
 const f=fixture();await f.c.startFollowUp();const body=JSON.parse(f.requests[0][1].body);
 assert.match(body.message,/SPECIFIC physics concept/);assert.match(body.message,/Use F = ma/);assert.match(body.message,/3 N/);assert.match(body.message,/exactly one correct answer/);assert.equal(body.image,'reference-images');
});
test('wrong and correct follow-ups stay separate from textbook scoring',async()=>{
 const f=fixture();await f.c.startFollowUp();
 f.$('followup-choices').children[0].onclick();f.$('followup-check').onclick();
 assert.equal(f.attempt.followUp.answers[0].correct,false);assert.equal(f.$('followup-solution').hidden,true);
 f.$('followup-retry').onclick();assert.equal(f.$('followup-check').disabled,true);
 f.$('followup-choices').children[1].onclick();f.$('followup-check').onclick();f.$('followup-check').onclick();
 assert.deepEqual(Array.from(f.attempt.followUp.answers,a=>a.correct),[false,true]);
 assert.equal(f.c.state.attempts.length,1);assert.equal(f.attempt.correct,false);assert.equal(f.c.state.items[f.problem.id].missed,true);
 assert.equal(f.c.window.Practice.stats(f.c.state).correct,0);assert.equal(f.$('followup-solution').hidden,false);
});
test('revealing saves the solution state and requires a genuinely new question next',async()=>{
 let calls=0;const next={...question,text:'A 4.0 kg trolley accelerates at 1.5 m/s². What is its net force?'};
 const f=fixture({fetch:async()=>({ok:true,json:async()=>++calls===1?question:next})});await f.c.startFollowUp();
 f.$('followup-choices').children[0].onclick();f.$('followup-check').onclick();f.$('followup-reveal').onclick();
 assert.equal(f.attempt.followUp.revealed,true);assert.match(f.$('followup-solution').textContent,/Answer B/);
 f.$('followup-retry').onclick();await flush();assert.equal(f.requests.length,2);
 assert.ok(JSON.parse(f.requests[1][1].body).message.includes(question.text));assert.equal(f.attempt.followUp.question.text,next.text);assert.equal(f.$('followup-solution').hidden,true);
});
test('offline misses preserve scores and offer a retry once connected',async()=>{
 const f=fixture({online:false});await f.c.startFollowUp();assert.equal(f.requests.length,0);assert.match(f.$('followup-status').textContent,/offline/);
 f.c.navigator.onLine=true;f.$('followup-retry').onclick();await flush();assert.equal(f.requests.length,1);assert.equal(f.attempt.correct,false);
});
test('HTTP errors and malformed responses can be retried without losing the miss',async()=>{
 for(const failure of [{ok:false,status:503},{ok:true,json:async()=>({text:'incomplete'})}]){
  let count=0;const f=fixture({fetch:async()=>++count===1?failure:{ok:true,json:async()=>question}});await f.c.startFollowUp();
  assert.equal(f.$('followup-retry').hidden,false);assert.equal(f.attempt.followUp,undefined);
  f.$('followup-retry').onclick();await flush();assert.equal(f.$('followup-content').hidden,false);assert.equal(f.c.state.attempts.length,1);
 }
});
test('navigation aborts generation and ignores a late service response',async()=>{
 let resolve;const f=fixture({fetch:()=>new Promise(r=>resolve=r)});const pending=f.c.startFollowUp();await flush();
 f.c.resetFollowUp();f.c.current={...f.problem,id:'uni-ch5-p2'};assert.equal(f.requests[0][1].signal.aborted,true);
 resolve({ok:true,json:async()=>question});await pending;assert.equal(f.$('followup').hidden,true);assert.equal(f.attempt.followUp,undefined);
});
test('switching students cannot attach a late response to another profile',async()=>{
 let resolve;const f=fixture({fetch:()=>new Promise(r=>resolve=r)});const pending=f.c.startFollowUp();await flush();
 f.c.resetFollowUp();f.c.student='Bob';f.c.state={version:1,attempts:[],items:{}};
 resolve({ok:true,json:async()=>question});await pending;assert.equal(f.$('followup').hidden,true);assert.equal(f.attempt.followUp,undefined);
});
test('cancel and opt-out abort requests and retain the saved textbook result',async()=>{
 for(const action of ['followup-cancel','followup-enabled']){
  let resolve;const f=fixture({fetch:()=>new Promise(r=>resolve=r)});const pending=f.c.startFollowUp();await flush();
  if(action==='followup-enabled'){f.$(action).checked=false;f.$(action).onchange();assert.equal(f.storage.get('physicsUniPracticeFollowUp'),'false');}else f.$(action).onclick();
  assert.equal(f.requests[0][1].signal.aborted,true);resolve({ok:true,json:async()=>question});await pending;assert.equal(f.attempt.correct,false);assert.equal(f.attempt.followUp,undefined);
 }
});
test('saved questions, retries and revealed solutions survive compact/hydrate and restore',async()=>{
 const f=fixture();await f.c.startFollowUp();f.$('followup-choices').children[0].onclick();f.$('followup-check').onclick();f.$('followup-reveal').onclick();
 const P=f.c.window.Practice,backup=JSON.parse(JSON.stringify(P.compact(f.c.state)));assert.equal(P.validState(backup,[f.problem]),true);
 f.c.state=P.hydrate(backup,[f.problem]);assert.equal(f.c.state.attempts[0].followUp.revealed,true);assert.equal(f.c.state.attempts[0].followUp.answers.length,1);
 f.c.resetFollowUp();assert.equal(f.c.restoreFollowUp(f.problem),true);assert.equal(f.$('followup-solution').hidden,false);assert.equal(f.requests.length,1);
});
test('malformed optional follow-up data never discards legitimate textbook progress',()=>{
 const f=fixture();f.attempt.followUp={question:{text:'broken'},answers:[]};const P=f.c.window.Practice;
 assert.equal(P.validState(f.c.state,[f.problem]),true);const restored=P.hydrate(f.c.state,[f.problem]);assert.equal(restored.attempts.length,1);assert.equal(restored.attempts[0].correct,false);assert.equal(restored.attempts[0].followUp,undefined);
});
test('saved correctness is re-derived from choices, and retry history is bounded',()=>{
 const record=FQ.normalizeRecord({question,answers:[{choice:'A',correct:true,at:new Date().toISOString()}],revealed:true});
 assert.equal(record.answers[0].correct,false);assert.equal(record.revealed,true);
 assert.equal(FQ.normalizeRecord({question,answers:Array(101).fill(record.answers[0])}),null);
});

test('generation timeout offers retry and keeps the saved textbook miss',async()=>{
 let expire;const f=fixture({setTimeout:fn=>{expire=fn;return 1;},clearTimeout:()=>{},fetch:(_url,{signal})=>new Promise((_resolve,reject)=>signal.addEventListener('abort',()=>reject(new DOMException('Aborted','AbortError'))))});
 const pending=f.c.startFollowUp();await flush();expire();await pending;
 assert.match(f.$('followup-status').textContent,/timed out/);assert.equal(f.$('followup-retry').hidden,false);assert.equal(f.$('followup-cancel').hidden,true);assert.equal(f.attempt.correct,false);
});
test('the retry limit still lets the student reveal the explanation',async()=>{
 const f=fixture();await f.c.startFollowUp();const record=f.attempt.followUp;
 record.answers=Array.from({length:100},()=>({choice:'A',correct:false,at:new Date().toISOString()}));
 f.c.restoreFollowUp(f.problem);f.$('followup-retry').onclick();f.$('followup-choices').children[0].onclick();f.$('followup-check').onclick();
 assert.equal(f.$('followup-reveal').hidden,false);f.$('followup-reveal').onclick();assert.equal(f.attempt.followUp.revealed,true);assert.equal(f.attempt.followUp.answers.length,100);
});
