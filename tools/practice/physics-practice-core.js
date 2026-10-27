/* Pure practice logic, shared by the browser and Node tests. */
(function (root) {
  'use strict';
  const topics = [];
  function configure(bank){topics.splice(0,topics.length,...new Set(bank.map(p=>p.topic)));}
  const levels = ['Foundation', 'Intermediate', 'Challenge'];
  function stats(state, topic) {
    const attempts = state.attempts.filter(a => (!topic || a.topic === topic) && !a.review);
    const recent = attempts.slice(-12);
    return {total: attempts.length, correct: attempts.filter(a=>a.correct).length,
      mastery: (recent.filter(a=>a.correct).length+2)/(recent.length+4)};
  }
  function targetLevel(state, topic) {
    const recent = state.attempts.filter(a=>a.topic===topic && !a.review).slice(-5);
    if (!recent.length) return 1;
    let level = recent[recent.length-1].level;
    const last = recent.slice(-2);
    if (last.length === 2 && last.every(a=>a.correct && a.level===level)) level++;
    else if (!recent[recent.length-1].correct) level--;
    return Math.max(1,Math.min(3,level));
  }
  function chooseTopic(state, filter, rng=Math.random, available=topics) {
    if (available.includes(filter)) return filter;
    const weights = available.map(t=>1-stats(state,t).mastery + (stats(state,t).total ? 0 : .2));
    let draw = rng()*weights.reduce((a,b)=>a+b,0);
    return available.find((t,i)=>(draw-=weights[i])<=0) || available[available.length-1];
  }
  function chooseExam(bank, state, filter, currentId, rng=Math.random) {
    const eligible = bank.filter(p=>!filter || p.topic===filter);
    const topic = chooseTopic(state,filter,rng,[...new Set(eligible.map(p=>p.topic))]);
    let unseen = eligible.filter(p=>!state.attempts.some(a=>a.id===p.id));
    const other = unseen.filter(p=>p.id!==currentId);
    if (other.length) unseen = other;
    if (!unseen.length) return null;
    const pool = unseen.filter(p=>p.topic===topic);
    const candidates = pool.length ? pool : unseen;
    const score = p => Math.abs(p.level-targetLevel(state,p.topic));
    const best = Math.min(...candidates.map(score));
    const near = candidates.filter(p=>score(p)===best);
    return near[Math.floor(rng()*near.length)];
  }
  function dayKey(value) {
    const d=new Date(value);
    if(!Number.isFinite(d.getTime()))return '';
    return `${d.getFullYear()}-${String(d.getMonth()+1).padStart(2,'0')}-${String(d.getDate()).padStart(2,'0')}`;
  }
  function pastDays(now=new Date()) {
    return Array.from({length:7},(_,i)=>{const d=new Date(now);d.setHours(0,0,0,0);d.setDate(d.getDate()-i);return {key:dayKey(d),date:d};});
  }
  function dayQuestions(state, day, filter='', excludeCorrect=false) {
    const latest=new Map(), onDay=new Map();
    for(const a of state.attempts){
      const at=Date.parse(a.at);if(!Number.isFinite(at))continue;
      const previous=latest.get(a.id);
      if(!previous||at>=Date.parse(previous.at))latest.set(a.id,a);
      if(dayKey(a.at)===day){const previousDay=onDay.get(a.id);if(!previousDay||at>=Date.parse(previousDay.at))onDay.set(a.id,a);}
    }
    return [...onDay.values()].sort((a,b)=>Date.parse(b.at)-Date.parse(a.at)).filter(a=>!excludeCorrect||!latest.get(a.id).correct)
      .map(a=>state.items[a.id]?.problem).filter(p=>p&&(!filter||p.topic===filter));
  }
  function problemNumber(problem){return problem.number;}
  function chapterQuestions(bank,chapter){return bank.filter(p=>p.chapter===chapter).sort((a,b)=>a.number-b.number);}
  function chapterSets(bank){
    return [...new Set(bank.map(p=>p.chapter))].map(chapter=>{const questions=chapterQuestions(bank,chapter),p=questions[0];return {chapter,title:p.chapterTitle,number:p.chapterNumber,count:questions.length};});
  }
  function chapterProgress(state, questions) {
    const ids=new Set(questions.map(p=>p.id)), latest=new Map();
    for(const a of state.attempts){
      if(!ids.has(a.id) || !Number.isFinite(Date.parse(a.at)))continue;
      const previous=latest.get(a.id);
      if(!previous || Date.parse(a.at)>=Date.parse(previous.at))latest.set(a.id,a);
    }
    return {answered:latest.size,correct:[...latest.values()].filter(a=>a.correct).length,latest};
  }
  // Stroke data stays offline and survives backups without saving large screenshots.
  function normalizeInk(ink){
    if(!ink||!Number.isInteger(ink.width)||!Number.isInteger(ink.height)||ink.width<1||ink.height<1||ink.width>4096||ink.height>4096||!Array.isArray(ink.strokes)||!ink.strokes.length||ink.strokes.length>1000)return null;
    let count=0;
    const valid=ink.strokes.every(s=>s&&/^#[0-9a-f]{6}$/i.test(s.color)&&Number.isFinite(s.width)&&s.width>=1&&s.width<=20&&Array.isArray(s.points)&&s.points.length>0&&s.points.every(p=>p&&Number.isFinite(p.x)&&Number.isFinite(p.y)&&p.x>=0&&p.y>=0&&p.x<=ink.width&&p.y<=ink.height)&&(count+=s.points.length)<=40000);
    if(!valid)return null;
    return {width:ink.width,height:ink.height,strokes:ink.strokes.map(s=>({tool:'pen',width:s.width,color:s.color,points:s.points.map(p=>({x:p.x,y:p.y}))}))};
  }
  function record(state,problem,choice,elapsed,correct,response={}){
    if(typeof correct!=='boolean')throw Error('Rate your work after comparing it with the solution.');
    choice=String(choice||'').trim().slice(0,12000);
    const review=state.attempts.some(a=>a.id===problem.id);
    const answerInk=response.answerInk?normalizeInk(response.answerInk):null;
    if(response.answerInk&&!answerInk)throw Error('This handwritten answer is too large to save. Please shorten it or use the steps pad for longer working.');
    const assessment=response.assessment==='ai'?'ai':'self';
    if(assessment==='ai'&&!validVerification(response.answerVerification,correct))throw Error('A reliable answer verification is required to save an automatic result.');
    if(problem.generatedData)state.generated={...state.generated,[problem.id]:problem.generatedData};
    state.attempts.push({id:problem.id,topic:problem.topic,level:problem.level,kind:problem.kind,chapter:problem.chapter,title:problem.title,choice,answer:problem.answer,correct,review,assessment,seconds:Math.max(0,elapsed||0),at:new Date().toISOString(),answerInputMode:response.answerInputMode==='handwritten'?'handwritten':'typed',...(answerInk?{answerInk}:{}),...(assessment==='ai'?{answerVerification:JSON.parse(JSON.stringify(response.answerVerification))}:{})});
    if(Object.keys(root.AdaptivePractice?.skills||{}).includes(response.practiceSkill))state.attempts[state.attempts.length-1].practiceSkill=response.practiceSkill;
    const old=state.items[problem.id]||{};
    state.items[problem.id]={problem,manual:!!old.manual,missed:!correct,aiConcern:!!old.aiConcern};
    return correct;
  }
  // Keep only bank references in backups/storage: diagrams belong to the embedded bank.
  function compact(state){return {...state,items:Object.fromEntries(Object.entries(state.items).map(([id,item])=>[id,{...item,problem:{id}}]))};}
  function validVerification(v,correct){return !!v&&['correct','partly_correct','incorrect'].includes(v.verdict)&&['high','medium'].includes(v.confidence)&&typeof v.feedback==='string'&&v.feedback.trim().length>0&&v.feedback.length<=6000&&correct===(v.verdict==='correct');}
  function normalizePreferences(value,bank){
    const mode=['adaptive','coach','chapter','random','review','day'].includes(value?.mode)?value.mode:'adaptive';
    const chapter=bank.some(p=>p.chapter===value?.chapter)?value.chapter:'';
    const available=[...new Set(bank.filter(p=>!chapter||p.chapter===chapter).map(p=>p.topic))];
    const topics=Array.isArray(value?.topics)?available.filter(t=>value.topics.includes(t)):available;
    return {mode,chapter,topics};
  }
  function validState(state,bank){
    if(!state||state.version!==1||!Array.isArray(state.attempts)||state.attempts.length>50000||!state.items||typeof state.items!=='object'||Array.isArray(state.items))return false;
    if(state.generated!==undefined&&(!state.generated||typeof state.generated!=='object'||Array.isArray(state.generated)||Object.keys(state.generated).length>5000||!Object.entries(state.generated).every(([id,d])=>id===d?.id&&root.AdaptivePractice?.normalize(d,bank))))return false;
    const ids=new Set([...bank,...(root.AdaptivePractice?.problems(state,bank)||[])].map(p=>p.id)),str=(v,n)=>typeof v==='string'&&v.length<=n;
    return state.attempts.every(a=>a&&ids.has(a.id)&&str(a.choice,12000)&&typeof a.correct==='boolean'&&typeof a.review==='boolean'&&['self','ai'].includes(a.assessment)&&(a.assessment!=='ai'||validVerification(a.answerVerification,a.correct))&&str(a.at,50)&&Number.isFinite(Date.parse(a.at))&&Number.isFinite(a.seconds)&&a.seconds>=0&&Object.hasOwn(state.items,a.id)&&(!a.answerInk||!!normalizeInk(a.answerInk))&&(a.answerInputMode===undefined||['typed','handwritten'].includes(a.answerInputMode)))&&
      Object.entries(state.items).every(([id,x])=>ids.has(id)&&x&&x.problem?.id===id&&typeof x.manual==='boolean'&&typeof x.missed==='boolean');
  }
  function hydrate(state,bank){
    const generated=Object.fromEntries(Object.entries(state.generated||{}).map(([id,d])=>[id,root.AdaptivePractice.normalize(d,bank)]));
    const byId=new Map([...bank,...(root.AdaptivePractice?.problems({generated},bank)||[])].map(p=>[p.id,p]));
    const attempts=state.attempts.map(a=>{const p=byId.get(a.id);return {id:p.id,topic:p.topic,level:p.level,kind:p.kind,chapter:p.chapter,title:p.title,choice:a.choice,answer:p.answer,correct:a.correct,review:false,assessment:a.assessment,seconds:a.seconds,at:a.at,answerInputMode:a.answerInputMode==='handwritten'?'handwritten':'typed',...(a.answerInk?{answerInk:normalizeInk(a.answerInk)}:{}),...(a.assessment==='ai'?{answerVerification:a.answerVerification}:{}),...(a.aiReview?{aiReview:a.aiReview}:{}),...(a.aiReviewedAt?{aiReviewedAt:a.aiReviewedAt}:{})};});
    const seen=new Set();for(const a of attempts){a.review=seen.has(a.id);seen.add(a.id);}
    for(let i=0;i<attempts.length;i++)if(Object.keys(root.AdaptivePractice?.skills||{}).includes(state.attempts[i].practiceSkill))attempts[i].practiceSkill=state.attempts[i].practiceSkill;
    const latest=new Map(attempts.map(a=>[a.id,a]));
    const items=Object.fromEntries(Object.entries(state.items).map(([id,item])=>[id,{problem:byId.get(id),manual:item.manual,missed:latest.has(id)?!latest.get(id).correct:false,aiConcern:false}]));
    return {version:1,attempts,items,...(state.preferences?{preferences:normalizePreferences(state.preferences,bank)}:{}),...(Object.keys(generated).length?{generated}:{})};
  }
  function randomQuestion(bank,state,filter,currentId,rng=Math.random){
    const eligible=bank.filter(p=>!filter||p.topic===filter),other=eligible.filter(p=>p.id!==currentId),pool=other.length?other:eligible;
    return pool.length?pool[Math.floor(rng()*pool.length)]:null;
  }
  function reviewQueue(state, filter) {
    return Object.values(state.items).filter(x=>(x.manual || x.missed || x.aiConcern) && (!filter || x.problem.topic===filter));
  }
  const SUP={'0':'\u2070','1':'\u00b9','2':'\u00b2','3':'\u00b3','4':'\u2074','5':'\u2075','6':'\u2076','7':'\u2077','8':'\u2078','9':'\u2079','+':'\u207a','-':'\u207b','n':'\u207f','x':'\u02e3','a':'\u1d43','b':'\u1d47','c':'\u1d9c','k':'\u1d4f'};
  const SUB={'0':'\u2080','1':'\u2081','2':'\u2082','3':'\u2083','4':'\u2084','5':'\u2085','6':'\u2086','7':'\u2087','8':'\u2088','9':'\u2089','n':'\u2099','x':'\u2093','a':'\u2090','i':'\u1d62','k':'\u2096'};
  const SYMBOLS=[[/\\(?:dfrac|tfrac|frac)\s*\{([^{}]*)\}\s*\{([^{}]*)\}/g,'($1/$2)'],[/\\sqrt\s*\{([^{}]*)\}/g,'\u221a($1)'],
    [/\\(?:times)\b/g,'\u00d7'],[/\\(?:cdot)\b/g,'\u00b7'],[/\\(?:div)\b/g,'\u00f7'],[/\\(?:pm)\b/g,'\u00b1'],[/\\(?:leq|le)\b/g,'\u2264'],[/\\(?:geq|ge)\b/g,'\u2265'],
    [/\\(?:neq|ne)\b/g,'\u2260'],[/\\approx\b/g,'\u2248'],[/\\(?:pi)\b/g,'\u03c0'],[/\\(?:theta)\b/g,'\u03b8'],[/\\(?:degree|circ)\b/g,'\u00b0'],[/\\(?:angle)\b/g,'\u2220'],
    [/\\(?:triangle)\b/g,'\u25b3'],[/\\(?:cdots|dots|ldots)\b/g,'\u2026'],[/\\(?:infty)\b/g,'\u221e'],[/\\(?:overline|underline|mathrm|mathbf|operatorname)\s*\{([^{}]*)\}/g,'$1'],
    [/\\(?:qquad|quad|,|;|:|!|\s)/g,' '],[/\\(?:left|right|displaystyle|limits)\b/g,''],[/\\%/g,'%'],[/\\\$/g,'$'],[/\\&/g,'&'],[/\\#/g,'#'],[/\\_/g,'_'],[/\\\\/g,' ']];
  function latexText(input){
    let t=String(input||'');
    t=t.replace(/\\\$/g,'\u0001').replace(/\$+/g,' ');
    for(let i=0;i<4;i++)t=t.replace(/\\(?:boxed|fbox|text|textbf|textit|mbox|mathbf|mathrm)\s*\{([^{}]*)\}/g,'$1');
    t=t.replace(/\^\s*\{?\s*\\(?:circ|degree)\s*\}?/g,'\u00b0');
    for(let i=0;i<3;i++)for(const [re,to] of SYMBOLS)t=t.replace(re,to);
    t=t.replace(/[\^_]\s*\{\s*\}/g,'');
    t=t.replace(/\^\s*\{?([A-Za-z0-9+-]+)\}?/g,(m,g)=>[...g].every(c=>SUP[c])?[...g].map(c=>SUP[c]).join(''):'^'+g);
    t=t.replace(/_\s*\{?([A-Za-z0-9]+)\}?/g,(m,g)=>[...g].every(c=>SUB[c])?[...g].map(c=>SUB[c]).join(''):'_'+g);
    t=t.replace(/\\[A-Za-z]+/g,'').replace(/[{}]/g,'').replace(/\u0001/g,'$');
    return t.replace(/\s+/g,' ').replace(/\s+([,.;?!])/g,'$1').trim();
  }
  const activityDays=root.ActivityMonitor?.days;
  const api={activityDays,topics,levels,configure,stats,targetLevel,chooseTopic,chooseExam,record,reviewQueue,randomQuestion,compact,validState,hydrate,normalizePreferences,normalizeInk,latexText,dayKey,pastDays,dayQuestions,problemNumber,chapterQuestions,chapterSets,chapterProgress};
  if(typeof module!=='undefined') module.exports=api;
  root.Practice=api;
})(typeof window!=='undefined'?window:globalThis);
