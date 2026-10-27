'use strict';
const bank=JSON.parse(document.getElementById('question-bank').textContent);
const AI=window.PhotoReview;
const P=window.Practice, $=id=>document.getElementById(id);
const Adaptive=window.AdaptivePractice;
try{if(localStorage.getItem('physicsUniAdaptiveSource')==='ai')$('adaptive-source').value='ai';}catch{}
let generationRequest=null;
let coachPresented=new Set();
P.configure(bank);
let state={version:1,attempts:[],items:{}}, current=null, selected=null, checked=false, revealed=false, started=Date.now();
let activeAttempt=null, photo=null, photoVersion=0, reviewRequest=null;
let cameraStream=null, cameraOpening=false, cameraVersion=0;
let drawingOpen=false, drawingShift=false;
// drawVersion changes on every edit, so a drawing can be re-checked by AI after it is modified.
let drawVersion=0, reviewedDrawVersion=null;
let submittedAnswer=null;
const drawing=new window.DrawingPad($('drawing-canvas'),()=>{drawVersion++;$('drawing-help').classList.toggle('faded',drawing.hasInk||!!drawing.active);updatePhotoControls();});
function validState(s){return P.validState(s,bank);}
function canonicalize(s) {
  s=P.hydrate(s,bank);
  for(const attempt of s.attempts){
    if(attempt.aiReview){const review=AI.normalize(attempt.aiReview);if(review)attempt.aiReview=review;else delete attempt.aiReview;}
    if(attempt.answerVerification)attempt.answerVerification=AI.normalize(attempt.answerVerification);
    if(typeof attempt.aiReviewedAt!=='string')delete attempt.aiReviewedAt;
  }
  for(const [id,item] of Object.entries(s.items)){
    const reviews=s.attempts.filter(a=>a.id===id&&a.aiReview&&a.aiReview.confidence!=='low'&&['correct','partly_correct','incorrect'].includes(a.aiReview.verdict));
    item.aiConcern=reviews.length?AI.needsReview(reviews[reviews.length-1].aiReview):false;
  }
  return s;
}
// ---- Per-student history (see students.js): local-first, optional Firebase sync ----
const students=window.StudentStore;let student='', updatedAt='';
let stopActivity=null,activityState=null,activityName='',activityGoal=10,activityExists=false;
try{const goal=Number(localStorage.getItem('physicsUniActivityGoal'));if(Number.isInteger(goal)&&goal>=1&&goal<=1000)activityGoal=goal;}catch(e){}
$('activity-goal').value=activityGoal;
let activityExcluded=[];
try{const saved=JSON.parse(localStorage.getItem('physicsUniActivityExcludedWeekdays')||'[3,6]');if(Array.isArray(saved))activityExcluded=saved.filter(n=>Number.isInteger(n)&&n>=0&&n<=6);}catch(e){}
const activityWeekdayInputs=Array.from($('activity-filter').querySelectorAll('input[type="checkbox"]'));
for(const input of activityWeekdayInputs)input.checked=activityExcluded.includes(Number(input.value));
$('activity-filter').addEventListener('change',()=>{
  activityExcluded=activityWeekdayInputs.filter(input=>input.checked).map(input=>Number(input.value));
  try{localStorage.setItem('physicsUniActivityExcludedWeekdays',JSON.stringify(activityExcluded));}catch(e){}
  renderActivity();
});
$('activity-period').onchange=renderActivity;
function renderActivity(){
  const cycle=$('activity-period').value==='cycle';
  $('activity-period-label').textContent=cycle&&activityExcluded.length?'From after the previous tutoring day through the next tutoring day':'Today and the preceding six days';
  $('activity-page-link').href=monitoringLink();
  const list=$('activity-days');list.replaceChildren();if(!activityState)return;
  const days=cycle?window.ActivityMonitor.cycleDays(activityState.attempts,new Date(),activityExcluded):P.activityDays(activityState.attempts,new Date(),activityExcluded);
  if(!days.length){list.textContent='All days in this window are excluded. Uncheck a weekday to show activity.';return;}
  for(const day of days){
    const row=document.createElement('div');row.className='activity-day';
    const labels=document.createElement('div'),label=document.createElement('span'),count=document.createElement('span');
    label.textContent=day.label+(day.upcoming?' · Upcoming':'')+(day.tutoring?' · Tutoring':'');count.textContent=`${day.total} / ${activityGoal} answers`;labels.append(label,count);
    const bar=document.createElement('progress');bar.max=activityGoal;bar.value=Math.min(day.total,activityGoal);bar.setAttribute('aria-label',`${activityName}, ${day.label}: ${day.total} checked answers, goal ${activityGoal}`);
    const detail=document.createElement('p');detail.className='small';detail.style.margin='0';detail.textContent=`${day.correct} correct · ${day.retries} retries · ${describeDuration(day.seconds)} recorded${day.missingTime?' · time missing for '+day.missingTime+' answers':''}`;
    if(day.tutoring){count.textContent='No practice goal';detail.textContent='End of this practice interval.';row.append(labels,detail);}
    else if(day.upcoming){detail.textContent=`Planned practice · goal ${activityGoal} answers`;row.append(labels,bar,detail);}
    else row.append(labels,bar,detail);list.append(row);
  }
}
function viewActivity(){
  if(!$('activity-form').reportValidity())return;
  const name=$('activity-student').value.trim();if(!name){$('activity-student').focus();return;}
  if(stopActivity)stopActivity();activityState=null;activityExists=false;activityName=name;activityGoal=Number($('activity-goal').value);
  try{localStorage.setItem('physicsUniActivityGoal',String(activityGoal));}catch(e){}
  $('activity-title').textContent=name+'’s activity';$('activity-updated').textContent='';renderActivity();
  stopActivity=students.watchActivity(name,{
    onData:data=>{
      activityExists=!!data;activityState=data?readPayload(data):null;
      $('activity-updated').textContent=data?'History last updated: '+(Number.isFinite(Date.parse(data.updatedAt))?new Date(data.updatedAt).toLocaleString('en-CA',{timeZone:'America/Vancouver'})+' (Vancouver)':'Not recorded'):'';
      renderActivity();
    },
    onStatus:(kind,error)=>{
      const messages={'missing-key':'Open Settings (☰), enter the Firebase API key, then choose View activity.',connecting:'Connecting to '+name+'’s synced history…',cached:'Offline or connecting: showing cached history. It may be incomplete.',synced:activityExists?(activityState?'Connected · live updates enabled.':'The saved history could not be read.'):'No synced history found for '+name+'. Enable sync on the student’s device.',error:error?.code==='permission-denied'?'Firebase denied access to this history.':'Unable to connect. Check Firebase settings and your connection, then choose View activity to retry.'};
      $('activity-status').textContent=messages[kind]||'';
    }
  });
}
const openActivity=()=>{$('activity-dialog').showModal();viewActivity();};
$('monitor-button').onclick=openActivity;$('login-monitor').onclick=openActivity;
$('activity-close').onclick=()=>$('activity-dialog').close();
$('activity-dialog').addEventListener('close',()=>{if(stopActivity)stopActivity();stopActivity=null;});
$('activity-form').onsubmit=e=>{e.preventDefault();viewActivity();};
function monitoringLink(){return window.ActivityMonitor.shareURL(location.href,{student:$('activity-student').value.trim()||'Bruce',goal:Number($('activity-goal').value)||10,excluded:activityExcluded,period:$('activity-period').value,key:students.getApiKey()});}
$('activity-page-link').onclick=()=>{$('activity-page-link').href=monitoringLink();};
$('activity-share').onclick=async()=>{
  const url=monitoringLink();
  try{await navigator.clipboard.writeText(url);$('activity-share-status').textContent='Monitoring link copied. Send it to your helper.';}
  catch(e){window.prompt('Copy this monitoring link:',url);}
};
$('activity-goal').oninput=()=>{if($('activity-goal').checkValidity()){activityGoal=Number($('activity-goal').value);try{localStorage.setItem('physicsUniActivityGoal',String(activityGoal));}catch(e){}renderActivity();}};
setInterval(()=>{if($('activity-dialog').open)renderActivity();},60000);
const liveParams=new URLSearchParams(location.search),followRequested=liveParams.has('follow');
let followedQuestion=null;
const live=new window.LivePractice.Session({openDoc:(id,key)=>students.liveRef(id,key),onStatus:setLiveStatus,
  onQuestion:data=>{
    const p=window.LivePractice.unpack(data,bank);
    if(data!==null&&!p){setLiveStatus('invalid');return;}
    followedQuestion=p;show(p,p?'Following live — your answers and progress are your own.':'The host has no question open yet.',true);
  }});
function setLiveStatus(status,error){
  const following=live.role==='follower',hosting=['host','ending'].includes(live.role);
  document.body.classList.toggle('following-live',following);
  $('share-live').hidden=!current||following||hosting;$('share-live').disabled=live.role==='starting';
  $('live-panel').hidden=status==='idle';$('live-link-row').hidden=!hosting||!$('live-link').value;
  $('live-exit').hidden=!following&&!hosting;$('live-exit').disabled=live.role==='ending';$('live-exit').textContent=following?'Leave live session':'Stop sharing';
  const messages={publishing:'Sharing the current question… waiting for a connection if offline.',starting:'Starting live sharing…',hosting:'Live sharing is on. Anyone with this link follows the question you open.',ending:'Stopping live sharing…',connecting:'Connecting to the live session…',following:'Following live. Questions change automatically when the host moves on.',reconnecting:'Reconnecting… showing the last shared question.',ended:'The host stopped sharing, or this session has expired. You can leave to practice on your own.',unavailable:'This live session is unavailable. Check the link or ask the host for a new one.',invalid:'This live session contains an unavailable question.',
    'publish-error':'The latest question could not be shared. Check your connection and try again.', 'stop-error':'Sharing could not be stopped. Check your connection and try Stop sharing again.'};
  $('live-status').textContent=messages[status]||'Live sharing could not connect.';
  if(status==='error')$('live-status').textContent=error?.message==='missing-firebase-api-key'?'Live sharing needs Firebase sync. Open Settings (☰), enter your Firebase API key, then try Share live again.':error?.message==='invalid-firebase-api-key'?'This sharing link has an invalid Firebase key. Ask the host to check Settings and share a new link.':error?.code==='permission-denied'?'Firebase denied access to live sharing. Check the database permissions or use a regular question link.':'Live sharing could not connect. Check your connection and try again.';
}
$('share-live').onclick=async()=>{
  if(!current||live.role!=='idle')return;
  $('live-link').value='';
  try{
    const id=await live.startHost(current);if(!id)return;
    $('live-link').value=window.LivePractice.shareURL(location.href,id,students.getApiKey());setLiveStatus('hosting');
    await live.publish(current);
  }catch(error){/* Status is reported by the session. */}
};
$('live-copy').onclick=async()=>{
  try{await navigator.clipboard.writeText($('live-link').value);$('live-copy').textContent='Copied';setTimeout(()=>$('live-copy').textContent='Copy link',2000);}
  catch(error){$('live-link').focus();$('live-link').select();$('live-status').textContent='Select and copy the live link above.';}
};
$('live-exit').onclick=async()=>{
  if(live.role==='follower'){
    live.leave();followedQuestion=null;const u=new URL(location.href);u.searchParams.delete('follow');u.hash='';history.replaceState(null,'',u);setLiveStatus('idle');
    if(student)next();else showLogin();
  }else try{await live.stopHost();$('live-link').value='';}catch(error){/* Keep Stop sharing available for retry. */}
};
const payloadFor=()=>({version:1,student,updatedAt,state:JSON.stringify(P.compact(state))});
function readPayload(p){try{if(!p||!p.state)return null;const s=typeof p.state==='string'?JSON.parse(p.state):p.state;return validState(s)?canonicalize(s):null;}catch(e){return null;}}
function save(){
  if(!student)return;updatedAt=new Date().toISOString();const payload=payloadFor();
  if(!students.saveLocal(student,payload)){$('storage-message').textContent='Browser storage is unavailable or full. Export your progress before closing.';return;}
  $('storage-message').textContent=students.syncing()?'Saving and syncing…':'Progress saved on this device.';
  students.push(payload);
}
function syncStatus(kind,error){
  const el=$('sync-status');if(!el)return;
  const text={local:'Saved on this device only.',connecting:'Connecting to Firebase…',synced:'Synced across devices · '+new Date().toLocaleTimeString(),error:'Saved on this device; Firebase sync is unavailable'+(error&&error.code==='permission-denied'?' (permission denied by the database rules).':error&&error.message==='firebase-sdk-unavailable'?' (the Firebase library could not load — check the internet connection).':'.')}[kind]||'';
  el.textContent=text;$('student-sync-dot').dataset.state=kind;
  if(kind==='synced'&&$('storage-message').textContent==='Saving and syncing…')$('storage-message').textContent='Progress saved and synced.';
}
function startSync(){if(!student)return;students.start(student,{getLocal:()=>students.loadLocal(student),onStatus:syncStatus,
  onRemote:data=>{const s=readPayload(data);if(!s)return;const previous=JSON.stringify(practiceSelection());cancelGeneration();resetFollowUp();state=s;updatedAt=data.updatedAt||'';students.saveLocal(student,{version:1,student,updatedAt,state:typeof data.state==='string'?data.state:JSON.stringify(data.state)});
    restorePracticeSelection();
    if(activeAttempt)activeAttempt=state.attempts.find(a=>a.at===activeAttempt.at&&a.id===activeAttempt.id)||null;dashboard();
    if(previous!==JSON.stringify(practiceSelection())&&live.role!=='follower')next(true,false);else restoreFollowUp(current);
    $('storage-message').textContent='Loaded the latest progress from another device.';}});}
// A shared question link refers to its stable chapter/question ID.
function shareURL(p){const u=new URL(location.href);u.search='';u.hash='';u.searchParams.set('q',p.id);if(p.generatedData)u.hash=new URLSearchParams({practice:JSON.stringify(p.generatedData)}).toString();return u.toString();}
function sharedFromURL(){
  const id=new URLSearchParams(location.search).get('q'),known=bank.find(p=>p.id===id);if(known)return known;
  try{const raw=new URLSearchParams(location.hash.slice(1)).get('practice');if(raw&&raw.length<26000){const p=Adaptive.problem(JSON.parse(raw),bank);if(p?.id===id)return p;}}catch{}
  return null;
}
let pendingShare=sharedFromURL();
if(new URLSearchParams(location.search).has('q')||new URLSearchParams(location.search).has('g')){try{const u=new URL(location.href);u.searchParams.delete('q');u.searchParams.delete('g');history.replaceState(null,'',u);}catch(e){}}
$('share-question').onclick=async()=>{
  if(!current)return;const url=shareURL(current),label=$('share-label');
  const done=t=>{label.textContent=t;setTimeout(()=>label.textContent='Share',2000);};
  if(navigator.share){try{await navigator.share({title:'University Physics practice question',text:current.title,url});return;}catch(e){if(e.name==='AbortError')return;}}
  try{await navigator.clipboard.writeText(url);done('Link copied');}catch(e){window.prompt('Copy this link to share the question:',url);}
};
function useStudent(name){
  resetFollowUp();cancelGeneration();coachPresented=new Set();
  cancelReview();student=students.login(name);state={version:1,attempts:[],items:{}};updatedAt='';
  const local=students.loadLocal(student),s=readPayload(local);
  if(local&&typeof local.student==='string'&&local.student!==student&&students.idFor(local.student)===students.idFor(student))student=students.login(local.student);
  if(s){state=s;updatedAt=local.updatedAt||'';}
  else if(local)$('storage-message').textContent='Saved progress for '+student+' could not be read. Starting fresh; sync or restore a backup to recover it.';
  else{const legacy=students.takeLegacy();if(legacy&&validState(legacy)){state=canonicalize(legacy);save();$('storage-message').textContent='Earlier progress on this device was moved into '+student+'’s history.';}}
  $('student-name-label').textContent=student;document.title='University Physics · Practice Studio · '+student;
  restorePracticeSelection();hideLogin();dashboard();
  if(live.role==='follower')show(followedQuestion,'Following live — your answers and progress are your own.',true);
  else if(pendingShare){const p=pendingShare;pendingShare=null;show(p,'Shared question — give it a try.');}else next(true,false);
  startSync();
}
function showLogin(){
  const list=$('known-students');list.replaceChildren();
  for(const name of students.known()){const b=document.createElement('button');b.type='button';b.className='known-student';b.textContent=name;if(students.idFor(name)===students.idFor(student))b.setAttribute('aria-current','true');b.onclick=()=>useStudent(name);list.append(b);}
  list.hidden=!list.children.length;$('login-cancel').hidden=!student;$('login-name').value='';$('login-overlay').hidden=false;setTimeout(()=>$('login-name').focus(),0);
}
function hideLogin(){$('login-overlay').hidden=true;}
$('login-form').onsubmit=e=>{e.preventDefault();const name=$('login-name').value.trim();if(name)useStudent(name);else $('login-name').focus();};
$('login-cancel').onclick=hideLogin;$('student-button').onclick=showLogin;
document.addEventListener('keydown',e=>{if(e.key==='Escape'&&!$('login-overlay').hidden&&student)hideLogin();});
// ☰ settings menu (like the family to-do page) holds the Firebase sync settings.
const setSettings=open=>{$('settings-panel').hidden=!open;$('settings-button').setAttribute('aria-expanded',String(open));if(open)setTimeout(()=>$('followup-enabled').focus(),0);};
$('settings-button').onclick=e=>{e.stopPropagation();setSettings($('settings-panel').hidden);};
document.addEventListener('click',e=>{if(!$('settings-panel').hidden&&!e.target.closest('.settings-wrap'))setSettings(false);});
document.addEventListener('keydown',e=>{if(e.key==='Escape'&&!$('settings-panel').hidden){setSettings(false);$('settings-button').focus();}});
$('firebase-key').value=students.getApiKey()?'••••••••':'';
$('sync-enable').onclick=async()=>{const v=$('firebase-key').value.trim();if(v&&!/^•+$/.test(v)&&!students.setApiKey(v)){$('sync-status').textContent='Enter a valid Firebase API key or a sharing link containing one.';return;}if(!students.getApiKey()){$('sync-status').textContent='Enter the Firebase API key first.';return;}$('firebase-key').value='••••••••';startSync();};
$('sync-local').onclick=async()=>{if(live.role==='host'){try{await live.stopHost();$('live-link').value='';}catch(error){return;}}students.setApiKey('');students.stop();$('firebase-key').value='';syncStatus('local');};
$('sync-share').onclick=()=>{const url=students.shareLink();if(!url){$('sync-status').textContent='Turn on sync first. A sync link only carries the key, never progress.';return;}
  if(navigator.share)navigator.share({title:'University Physics Practice Studio',url}).catch(()=>{});else window.prompt('Copy this link to open synced practice on another device:',url);};
const chapters=P.chapterSets(bank);
const topicNames=new Map(bank.map(p=>[p.topic,p.topicTitle?`Ch ${p.chapterNumber} · ${p.topicTitle}`:p.topic]));
const topicName=topic=>topicNames.get(topic)||topic;
let selectedTopics=new Set(P.topics);
let topicsChapter='';
for(const chapter of chapters){const o=document.createElement('option');o.value=chapter.chapter;o.textContent=`Chapter ${chapter.number}: ${chapter.title} · ${chapter.count} questions`;$('practice-chapter').append(o);}
function availableTopics(){return [...new Set(bank.filter(p=>!$('practice-chapter').value||p.chapter===$('practice-chapter').value).map(p=>p.topic))];}
function practiceSelection(){return P.normalizePreferences({mode:$('mode').value,chapter:$('practice-chapter').value,topics:[...selectedTopics]},bank);}
function rememberPracticeSelection(){
  if(!student)return;
  const preferences=practiceSelection();
  if(JSON.stringify(state.preferences)===JSON.stringify(preferences))return;
  state.preferences=preferences;save();
}
function restorePracticeSelection(){
  const preferences=P.normalizePreferences(state.preferences,bank);
  $('mode').value=preferences.mode;$('practice-chapter').value=preferences.chapter;
  refreshTopicOptions();selectedTopics=new Set(preferences.topics);syncTopicSelection();
}
function syncTopicSelection(){
  const available=availableTopics(),count=selectedTopics.size,all=count===available.length;
  $('topic-summary').textContent=!count?'Choose topics':all?($('practice-chapter').value?'Whole chapter':'All topics'):`${count} topic${count===1?'':'s'} selected`;
  $('topic-summary').title=available.filter(t=>selectedTopics.has(t)).map(topicName).join('\n');
  $('topic-selection-status').textContent=`${count} of ${available.length} topics selected · ${scopedQuestions().length} questions`;
  $('topic-all').disabled=all;$('topic-clear').disabled=!count;
  for(const input of $('topic-list').querySelectorAll('input[data-topic]'))input.checked=selectedTopics.has(input.value);
  for(const input of $('topic-list').querySelectorAll('input[data-chapter]')){
    const topics=[...new Set(bank.filter(p=>p.chapter===input.value).map(p=>p.topic))],selected=topics.filter(t=>selectedTopics.has(t)).length;
    input.checked=selected===topics.length;input.indeterminate=selected>0&&selected<topics.length;
  }
}
function refreshTopicOptions(){
  const chapter=$('practice-chapter').value,available=availableTopics();
  const previous=[...new Set(bank.filter(p=>!topicsChapter||p.chapter===topicsChapter).map(p=>p.topic))];
  const wasAll=previous.length===selectedTopics.size&&previous.every(t=>selectedTopics.has(t));
  selectedTopics=new Set(wasAll?available:available.filter(t=>selectedTopics.has(t)));
  if(!selectedTopics.size)selectedTopics=new Set(available);
  topicsChapter=chapter;
  $('topic-list').replaceChildren();
  for(const set of chapters.filter(c=>!chapter||c.chapter===chapter)){
    const topics=[...new Set(bank.filter(p=>p.chapter===set.chapter).map(p=>p.topic))];
    const group=document.createElement('fieldset');group.className='topic-group';
    const legend=document.createElement('legend'),label=document.createElement('label'),input=document.createElement('input');label.className='topic-option topic-chapter';input.type='checkbox';input.value=set.chapter;input.dataset.chapter=set.chapter;
    label.append(input,`Chapter ${set.number}: ${set.title} · Whole chapter`);legend.append(label);group.append(legend);
    input.onchange=()=>{for(const t of topics){if(input.checked)selectedTopics.add(t);else selectedTopics.delete(t);}syncTopicSelection();next(true);};
    for(const topic of topics){
      const label=document.createElement('label'),input=document.createElement('input');label.className='topic-option topic-section';input.type='checkbox';input.value=topic;input.dataset.topic=topic;
      label.append(input,topicName(topic));input.onchange=()=>{if(input.checked)selectedTopics.add(topic);else selectedTopics.delete(topic);syncTopicSelection();next(true);};group.append(label);
    }
    $('topic-list').append(group);
  }
  syncTopicSelection();
}
function scopedQuestions(questions=bank){
  const chapter=$('practice-chapter').value;
  return questions.filter(p=>(!chapter||p.chapter===chapter)&&selectedTopics.has(p.topic));
}
const selectedChapterQuestions=()=>scopedQuestions();
const selectedDayQuestions=day=>scopedQuestions(P.dayQuestions(state,day,'',$('day-exclude-correct').checked));
refreshTopicOptions();
$('bank-count').textContent=`${bank.length.toLocaleString()} textbook questions · ${chapters.length} chapter${chapters.length===1?'':'s'}`;
// "Last tried" for review-queue items: the most recent attempt on that question.
function lastTried(id){let at='';for(const a of state.attempts)if(a.id===id&&a.at>at)at=a.at;return at;}
function describeTime(iso){
  const then=new Date(iso);if(isNaN(then))return '';
  const startOfDay=d=>{const x=new Date(d);x.setHours(0,0,0,0);return x;};
  const days=Math.round((startOfDay(new Date())-startOfDay(then))/86400000);
  const time=then.toLocaleTimeString([],{hour:'numeric',minute:'2-digit'});
  if(days<=0)return 'today at '+time;
  if(days===1)return 'yesterday at '+time;
  if(days<7)return days+' days ago';
  if(days<14)return 'last week';
  if(days<60)return Math.round(days/7)+' weeks ago';
  return 'on '+then.toLocaleDateString([],{month:'short',day:'numeric',year:'numeric'});
}
function describeDuration(seconds){
  if(typeof seconds!=='number'||!Number.isFinite(seconds)||seconds<0)return 'Not recorded';
  const total=Math.round(seconds), hours=Math.floor(total/3600), minutes=Math.floor(total%3600/60), remaining=total%60;
  return [hours?`${hours}h`:'',hours||minutes?`${minutes}m`:'',`${remaining}s`].filter(Boolean).join(' ');
}
// Questions answered in the last 7 days (skipped ones are never recorded as attempts).
function renderRecent(){
  const since=Date.now()-7*86400000, list=$('recent-list');list.replaceChildren();
  const recent=state.attempts.filter(a=>Date.parse(a.at)>=since).sort((x,y)=>y.at.localeCompare(x.at));
  $('recent-count').textContent=recent.length;
  if(!recent.length){list.textContent='No questions answered in the last 7 days.';return;}
  const dayStats=new Map();
  for(const attempt of recent){
    const key=new Date(attempt.at).toDateString(), stats=dayStats.get(key)||{correct:0,total:0,seconds:0,timeRecorded:true};
    stats.total++;if(attempt.correct)stats.correct++;
    if(typeof attempt.seconds==='number'&&Number.isFinite(attempt.seconds)&&attempt.seconds>=0)stats.seconds+=attempt.seconds;
    else stats.timeRecorded=false;
    dayStats.set(key,stats);
  }
  let day='';
  for(const attempt of recent.slice(0,60)){
    const when=new Date(attempt.at), label=describeDay(when), key=when.toDateString();
    if(key!==day){
      day=key;const h=document.createElement('div');h.className='recent-day';const stats=dayStats.get(key);
      const percentage=Math.round(stats.correct/stats.total*100), totalTime=describeDuration(stats.timeRecorded?stats.seconds:undefined);
      const averageTime=describeDuration(stats.timeRecorded?stats.seconds/stats.total:undefined);
      h.textContent=`${label.toUpperCase()} · ${stats.correct}/${stats.total}(${percentage}%) · ${totalTime}(${averageTime})`;list.append(h);
    }
    const problem=state.items[attempt.id]?.problem;
    const b=document.createElement('button');b.className='queue-item recent-item';b.textContent=attempt.title;
    const meta=document.createElement('span');const verdict=document.createElement('span');
    verdict.className='verdict';verdict.dataset.ok=attempt.correct?'yes':'no';verdict.textContent=attempt.correct?'Correct':'Missed';
    meta.append(when.toLocaleTimeString([],{hour:'numeric',minute:'2-digit'})+' · '+topicName(attempt.topic)+(attempt.review?' · review':'')+' · ');meta.append(verdict);
    const duration=document.createElement('span');duration.textContent='Time spent: '+describeDuration(attempt.seconds);
    b.append(meta,duration);
    if(problem)b.onclick=()=>show(problem,'From your last 7 days. Review attempts do not change first-attempt accuracy.');else b.disabled=true;
    list.append(b);
  }
}
function describeDay(date){
  const startOfDay=d=>{const x=new Date(d);x.setHours(0,0,0,0);return x;};
  const days=Math.round((startOfDay(new Date())-startOfDay(date))/86400000);
  return days<=0?'Today':days===1?'Yesterday':date.toLocaleDateString([],{weekday:'long'});
}
function refreshDayControls(){
  const active=$('mode').value==='day';$('day-controls').hidden=!active;
  if(!active)return [];
  const daySelect=$('practice-day'),chosen=daySelect.value;
  daySelect.replaceChildren(...P.pastDays().map(({key,date},i)=>{
    const o=document.createElement('option');o.value=key;
    const label=i===0?'Today':i===1?'Yesterday':date.toLocaleDateString([],{weekday:'long'});
    const count=selectedDayQuestions(key).length;
    o.textContent=`${label} · ${date.toLocaleDateString([],{month:'short',day:'numeric'})} · ${count} question${count===1?'':'s'}`;return o;
  }));
  if([...daySelect.options].some(o=>o.value===chosen))daySelect.value=chosen;
  const questions=selectedDayQuestions(daySelect.value),picker=$('day-question');
  const placeholder=document.createElement('option');placeholder.value='';placeholder.disabled=true;placeholder.textContent=questions.length?'Choose a question':'No matching questions';
  picker.replaceChildren(placeholder,...questions.map((p,i)=>{const o=document.createElement('option');o.value=p.id;o.textContent=`${i+1}. ${p.title} · ${topicName(p.topic)}`;return o;}));
  picker.value=questions.some(p=>p.id===current?.id)?current.id:'';picker.disabled=!questions.length;
  return questions;
}
function showDayQuestion(p,questions){
  const date=new Date($('practice-day').value+'T12:00:00').toLocaleDateString([],{weekday:'long',month:'short',day:'numeric'});
  show(p,p?`${date} · Question ${questions.findIndex(q=>q.id===p.id)+1} of ${questions.length}. This is review practice.`:`No questions match ${date} and the selected chapter/topic${$('day-exclude-correct').checked?' after excluding correct answers':''}. Choose another day or adjust the filters.`);
  $('day-question').value=p?p.id:'';
}
function refreshChapterControls(){
  const active=$('mode').value==='chapter';$('chapter-controls').hidden=!active;
  $('next').textContent='Next question →';$('skip').textContent='Skip for now';
  if(!active)return [];
  const questions=selectedChapterQuestions(),progress=P.chapterProgress(state,questions),picker=$('chapter-question');
  $('chapter-grid').classList.toggle('cross-chapter',!$('practice-chapter').value);
  const inSet=questions.some(p=>p.id===current?.id);
  const placeholder=document.createElement('option');placeholder.value='';placeholder.disabled=true;placeholder.textContent='Choose a question';
  picker.replaceChildren(placeholder,...questions.map(p=>{const o=document.createElement('option');o.value=p.id;const a=progress.latest.get(p.id);o.textContent=`${$('practice-chapter').value?'':`Ch ${p.chapterNumber} · `}Question ${P.problemNumber(p)}${a?a.correct?' · Correct':' · Needs practice':''}`;return o;}));
  picker.value=inSet?current.id:'';picker.disabled=!questions.length;
  $('chapter-progress').textContent=`${progress.answered}/${questions.length} answered · ${progress.correct} correct${progress.answered===questions.length&&questions.length?' · Set complete!':''}`;
  $('chapter-previous').disabled=!inSet||questions[0]?.id===current.id;
  const last=inSet&&questions[questions.length-1].id===current.id;
  if(last){$('next').textContent=`Back to ${$('practice-chapter').value?'':`Ch ${questions[0].chapterNumber} · `}question ${questions[0].number} →`;$('skip').textContent=$('next').textContent;}
  $('chapter-grid').replaceChildren(...questions.map(p=>{
    const number=p.number,a=progress.latest.get(p.id),b=document.createElement('button');b.type='button';b.textContent=$('practice-chapter').value?number:`Ch ${p.chapterNumber} · ${number}`;
    b.className=a?a.correct?'correct':'incorrect':'';
    const label=`Chapter ${p.chapterNumber}, Question ${number}: ${p.title} · ${a?a.correct?'Correct':'Needs practice':'Not answered'}`;
    b.setAttribute('aria-label',label);b.title=label;if(p.id===current?.id)b.setAttribute('aria-current','true');
    b.onclick=()=>{showChapterQuestion(p);$('question-title').focus();};return b;
  }));
  $('chapter-notice').hidden=true;
  return questions;
}
function showChapterQuestion(p){
  const questions=selectedChapterQuestions(),seen=p&&state.attempts.some(a=>a.id===p.id);
  show(p,p?`Chapter ${p.chapterNumber}: ${p.chapterTitle} · Question ${p.number} · ${questions.findIndex(q=>q.id===p.id)+1} of ${questions.length} in this selection. ${seen?'Retrying counts as review.':'Work through the selection at your own pace.'}`:'No questions available for this chapter and topic.');
}
function dashboard(){
  const all=state.attempts, first=all.filter(a=>!a.review);
  $('attempt-count').textContent=all.length;
  $('accuracy').textContent=first.length?`${Math.round(first.filter(a=>a.correct).length/first.length*100)}% correct on first attempts`:'Your progress starts here';
  $('topic-stats').replaceChildren();
  for(const topic of P.topics){const s=P.stats(state,topic), row=document.createElement('div');row.className='topic-row';const labels=document.createElement('div'), name=document.createElement('span'), score=document.createElement('span');name.textContent=topicName(topic);score.textContent=s.total?`${s.correct}/${s.total} correct`:'Not tried yet';labels.append(name,score);const bar=document.createElement('progress');bar.max=100;bar.value=s.total?s.correct/s.total*100:0;bar.setAttribute('aria-label',`${topicName(topic)} first-attempt accuracy`);row.append(labels,bar);$('topic-stats').append(row);}
  const queue=P.reviewQueue(state,'');$('review-count').textContent=queue.length;$('queue').replaceChildren();
  for(const item of queue.slice(-5).reverse()){const b=document.createElement('button');b.className='queue-item';b.textContent=item.problem.title;const status=document.createElement('span');status.textContent=`${topicName(item.problem.topic)} · ${[item.missed?'Missed':'',item.manual?'Flagged':'',item.aiConcern?'Check reasoning':''].filter(Boolean).join(' + ')}`;b.append(status);
    const last=lastTried(item.problem.id);if(last){const when=document.createElement('span');when.className='queue-when';when.textContent='Last tried '+describeTime(last);when.title=new Date(last).toLocaleString();b.append(when);}b.onclick=()=>show(item.problem,'Retry a saved question. Review attempts do not change first-attempt accuracy.');$('queue').append(b);}
  if(!queue.length)$('queue').textContent='Nothing to review yet.';
  $('review-button').disabled=!queue.length;
  renderRecent();renderLearningLog();refreshDayControls();refreshChapterControls();
  renderAdaptiveCoverage();
}
function renderAdaptiveCoverage(){
  const box=$('adaptive-coverage');box.replaceChildren();
  const rows=Adaptive.coverage(state,bank,scopedQuestions());
  for(const topic of [...new Set(rows.map(r=>r.topic))]){
    const group=document.createElement('div'),heading=document.createElement('h3');heading.textContent=topicName(topic);group.append(heading);
    for(const row of rows.filter(r=>r.topic===topic)){const p=document.createElement('p');p.className='small';p.textContent=`${Adaptive.skills[row.skill]}: ${row.status}${row.total?` · ${row.correct}/${row.total} recent correct`:''}`;group.append(p);}
    box.append(group);
  }
}
function setGenerationBusy(busy){
  for(const id of ['adaptive-create','next','skip']){
    const button=$(id);
    if(busy){
      button.dataset.generationLabel=button.textContent;
      button.dataset.generationDisabled=String(button.disabled);
      button.textContent='Generating question…';button.disabled=true;button.setAttribute('aria-busy','true');
    }else{
      if(button.dataset.generationLabel!==undefined){
        button.textContent=button.dataset.generationLabel;button.disabled=button.dataset.generationDisabled==='true';
        delete button.dataset.generationLabel;delete button.dataset.generationDisabled;
      }
      button.removeAttribute('aria-busy');
    }
  }
}
function cancelGeneration(){
  if(generationRequest){const request=generationRequest;generationRequest=null;request.controller.abort();clearTimeout(request.timer);}
  setGenerationBusy(false);
  $('adaptive-create').disabled=false;$('adaptive-cancel').hidden=true;$('adaptive-panel').removeAttribute('aria-busy');
}
function alwaysGenerate(){return $('adaptive-source').value==='ai';}
function adaptiveSourceHelp(){
  $('adaptive-source-help').textContent=alwaysGenerate()?'Every next question is newly created by AI using the selected textbook chapter/topic, a reference question, its diagrams and worked solution. Internet is required; suitable textbook questions are not substituted.':'Use a suitable unused textbook question first. If none matches the topic, skill and level, AI creates a new one using a textbook reference question, its diagrams and worked solution.';
}
function adaptiveReadyMessage(){return alwaysGenerate()?'Ready. Always AI is selected: each next question will be created using your selected textbook context. Your checked answers guide its skill and difficulty.':'Ready. Textbook questions come first; AI fills gaps. Your checked answers guide the next skill and difficulty.';}
adaptiveSourceHelp();
$('adaptive-source').onchange=()=>{
  cancelGeneration();
  try{localStorage.setItem('physicsUniAdaptiveSource',$('adaptive-source').value);}catch{}
  adaptiveSourceHelp();$('adaptive-status').textContent=adaptiveReadyMessage();
};
async function generateAdaptive(){
  if(generationRequest||live.role==='follower'||$('mode').value!=='coach')return;
  if(!student){showLogin();$('adaptive-status').textContent='Choose a student before creating a question.';return;}
  if(reviewRequest){$('adaptive-status').textContent='Finish or cancel the current answer check first.';return;}
  const plan=Adaptive.plan(state,bank,scopedQuestions());
  if(!plan){$('adaptive-status').textContent='Select at least one topic first.';return;}
  const requireAI=alwaysGenerate();
  const textbook=requireAI?null:Adaptive.chooseTextbook(plan,scopedQuestions(),state,[...coachPresented,current?.id]);
  if(textbook){
    coachPresented.add(textbook.id);show({...textbook,coachSkill:plan.skill},`${topicName(textbook.topic)} · ${Adaptive.skills[plan.skill]} · ${plan.reason} A matching textbook question is available.`);
    $('adaptive-status').textContent='Selected a suitable unused textbook question. AI creates a new question only when this topic, skill and difficulty have no suitable unused match.';return;
  }
  if(Object.keys(state.generated||{}).length>=5000){$('adaptive-status').textContent='This profile has reached its saved-question limit. Export progress and revisit saved questions or use textbook practice.';return;}
  if(navigator.onLine===false){$('adaptive-status').textContent=requireAI?'You are offline. Always AI needs an internet connection to create each new question. Reconnect and retry, or change Question source.':'You are offline. Revisit saved questions or use textbook practice, then retry when connected.';return;}
  const controller=new AbortController(),request={controller,student,problem:current};generationRequest=request;
  setGenerationBusy(true);$('adaptive-cancel').hidden=false;$('adaptive-panel').setAttribute('aria-busy','true');
  $('adaptive-status').textContent=`${requireAI?'Always AI · using textbook context.':'No suitable unused textbook question for this skill and level.'} Creating ${P.levels[plan.level-1].toLowerCase()} practice in ${Adaptive.skills[plan.skill]} · ${topicName(plan.topic)}…`;
  request.timer=setTimeout(()=>{request.timedOut=true;controller.abort();},60000);
  try{
    const message=Adaptive.prompt(plan,state,readableHTML(plan.anchor.html),readableHTML(plan.anchor.solution));
    const image=await questionAndWorkingImage(plan.anchor,[],controller.signal);
    if(controller.signal.aborted||generationRequest!==request)return;
    const result=await fetch(AI.endpoint,{method:'POST',mode:'cors',credentials:'omit',headers:{'Content-Type':'application/json'},signal:controller.signal,body:JSON.stringify({message,image:image.image,mime_type:image.mime_type,filename:image.filename})});
    if(!result.ok)throw Error('The question service returned HTTP '+result.status+'.');
    const data=await result.json();
    if(controller.signal.aborted||generationRequest!==request||student!==request.student||current!==request.problem||$('mode').value!=='coach')return;
    const p=Adaptive.parse(data,plan,bank,'gen-'+crypto.randomUUID());
    if(Object.values(state.generated||{}).some(d=>d.question.toLowerCase()===p.generatedData.question.toLowerCase()))throw Error('The service repeated a saved question. Please retry for a new one.');
    generationRequest=null;clearTimeout(request.timer);
    show(p,`${topicName(p.topic)} · ${Adaptive.skills[p.skill]} · ${plan.reason}`);
    save();renderAdaptiveCoverage();$('adaptive-status').textContent='New question ready. Answer it, check your work, then choose Next question to continue.';
    $('question-title').focus();
  }catch(error){
    if(generationRequest!==request)return;
    $('adaptive-status').textContent=(request.timedOut?'Creating the question timed out.':error.name==='AbortError'?'Question creation canceled.':error instanceof TypeError?'Could not reach the question service. Check your connection.':error.message)+' Your current question and progress are kept. '+(requireAI?'Retry or change Question source.':'Retry or use textbook practice.');
  }finally{if(generationRequest===request)cancelGeneration();}
}
$('adaptive-create').onclick=generateAdaptive;
$('adaptive-cancel').onclick=()=>{cancelGeneration();$('adaptive-status').textContent='Question creation canceled. Your current question and progress are kept.';};
$('adaptive-textbook').onclick=()=>{$('mode').value='adaptive';next(true);};
function flagButton(){const manual=current && state.items[current.id]?.manual;$('flag').textContent=manual?'★ Flagged for review':'☆ Flag for review';$('flag').setAttribute('aria-pressed',String(!!manual));}
function aiMarker(){const marker=document.createElement('span');marker.className='ai-marker';marker.textContent='AI';marker.setAttribute('aria-label','AI-generated question');marker.title='AI-generated question';return marker;}
function inkPreview(ink){
  const data=P.normalizeInk(ink);if(!data)return null;
  const ns='http://www.w3.org/2000/svg',svg=document.createElementNS(ns,'svg');svg.classList.add('saved-answer-ink');svg.setAttribute('viewBox',`0 0 ${data.width} ${data.height}`);svg.setAttribute('role','img');svg.setAttribute('aria-label','Your saved handwritten answer');
  for(const stroke of data.strokes){const dot=stroke.points.length===1,node=document.createElementNS(ns,dot?'circle':'polyline');
    if(dot){node.setAttribute('cx',stroke.points[0].x);node.setAttribute('cy',stroke.points[0].y);node.setAttribute('r',stroke.width/2);node.setAttribute('fill',stroke.color);}
    else{node.setAttribute('points',stroke.points.map(p=>`${p.x},${p.y}`).join(' '));node.setAttribute('fill','none');node.setAttribute('stroke',stroke.color);node.setAttribute('stroke-width',stroke.width);node.setAttribute('stroke-linecap','round');node.setAttribute('stroke-linejoin','round');}svg.append(node);
  }return svg;
}
function syncAnswerTools(){
  const input=$('response-input');if(input)input.readOnly=checked||revealed||!!reviewRequest;
}
function buildAnswerInput(problem){
  const box=$('choice-list');
  const label=document.createElement('label');label.id='response-label';label.htmlFor='response-input';label.textContent='Type your answer with units and direction, and/or write it in Show your steps below.';
  const input=document.createElement('textarea');input.id='response-input';input.rows=3;input.maxLength=12000;input.placeholder='Your answer and reasoning…';input.setAttribute('aria-label','Your written answer');
  input.oninput=()=>{selected=input.value;const dock=$('dock-response');if(dock&&dock.value!==input.value)dock.value=input.value;updatePhotoControls();};box.append(label,input);
  const previous=state.attempts.filter(a=>a.id===problem.id).at(-1);
  if(previous&&(previous.choice||previous.answerInk)){const details=document.createElement('details');details.className='previous-answer';details.id='previous-response';const summary=document.createElement('summary');summary.textContent='Your previous answer · '+(previous.assessment==='ai'?'AI checked · ':'self-rated · ')+(previous.correct?'correct':'needs practice');details.append(summary);if(previous.choice){const p=document.createElement('p');p.textContent=previous.choice;details.append(p);}const preview=inkPreview(previous.answerInk);if(preview)details.append(preview);box.append(details);}
  syncAnswerTools();
}
function show(p,reason,fromLive=false){
  resetFollowUp();cancelGeneration();
  if(live.role==='follower'&&!fromLive){p=followedQuestion;reason='Following live — your answers and progress are your own.';}
  if(p?.generatedData){state.generated=state.generated||{};state.generated[p.id]=p.generatedData;}
  $('adaptive-panel').hidden=$('mode').value!=='coach'||live.role==='follower';
  resetPhotoReview();submittedAnswer=null;current=p;selected=null;checked=false;revealed=false;started=Date.now();$('reason').textContent=reason;
  refreshChapterControls();
  $('feedback').hidden=true;$('self-rating').hidden=true;$('verify-retry').hidden=true;$('solution').hidden=true;$('solution').open=false;$('solution-body').replaceChildren();$('image-warning').hidden=true;
  $('check').hidden=!p;$('check').disabled=false;$('check').textContent='Show answer';$('next').hidden=true;$('skip').hidden=!p;$('choices').hidden=!p;$('flag').hidden=!p;$('share-question').hidden=!p;$('photo-section').hidden=!p;
  $('share-live').hidden=!p||live.role==='follower'||['host','ending'].includes(live.role);
  $('choice-list').replaceChildren();$('statement').replaceChildren();$('source').hidden=true;$('source').removeAttribute('href');live.publish(p).catch(()=>{});
  $('badge').classList.toggle('generated-badge',!!p?.generatedData);
  if(!p){const ready=$('mode').value==='coach'&&selectedTopics.size;$('badge').hidden=false;$('badge').textContent=ready?'Skill builder':'All clear';$('question-title').textContent=ready?'Ready for your next question':'No questions in this selection';$('question-meta').textContent=ready?'Choose Find my next question above to begin.':'Choose another topic or practice mode.';return;}
  if(p.generatedData)$('badge').replaceChildren(aiMarker(),document.createTextNode('Practice · '+Adaptive.skills[p.skill]));else $('badge').textContent=p.questionType;
  $('badge').hidden=false;$('question-title').textContent=p.title;
  $('question-meta').textContent=`Chapter ${p.chapterNumber}: ${p.chapterTitle} · ${p.topicTitle||p.topic} · ${P.levels[p.level-1]} (estimated)`;
  $('statement').innerHTML=p.html;$('source').href=p.url;$('source').hidden=false;$('source').textContent=p.generatedData?'Open related textbook collection ↗':'Open question collection ↗';flagButton();
  buildAnswerInput(p);$('photo-section').hidden=false;openDrawing();restoreFollowUp(p);
}
function next(reset=false,persistSelection=true){
  if(live.role==='follower')return;
  resetFollowUp();cancelGeneration();
  if(persistSelection)rememberPracticeSelection();
  const mode=$('mode').value;
  $('adaptive-panel').hidden=mode!=='coach';
  renderAdaptiveCoverage();
  const dayQuestions=refreshDayControls();
  const chapterQuestions=refreshChapterControls();
  if(!selectedTopics.size){show(null,'Select one or more topics, or check a whole chapter, to start practising.');return;}
  if(mode==='coach'){
    if(reset===true){show(null,'Choose Find my next question to start adaptive skill practice.');$('adaptive-status').textContent=adaptiveReadyMessage();}
    else generateAdaptive();
    return;
  }
  if(mode==='chapter'){
    const index=reset===true?-1:chapterQuestions.findIndex(p=>p.id===current?.id);
    showChapterQuestion(chapterQuestions.length?chapterQuestions[(index+1)%chapterQuestions.length]:null);return;
  }
  if(mode==='day'){
    const index=reset===true?-1:dayQuestions.findIndex(p=>p.id===current?.id);
    showDayQuestion(dayQuestions.length?dayQuestions[(index+1)%dayQuestions.length]:null,dayQuestions);return;
  }
  if(mode==='review'){
    const ids=new Set(scopedQuestions([...bank,...Adaptive.problems(state,bank)]).map(p=>p.id)),q=P.reviewQueue(state,'').filter(x=>ids.has(x.problem.id)), other=q.filter(x=>x.problem.id!==current?.id);
    const p=(other[0]||q[0])?.problem;
    show(p||null,p?'Review a missed or flagged question.':'Your review queue is clear for this chapter and topic.');return;
  }
  if(mode==='random'){
    const p=P.randomQuestion(scopedQuestions(),state,'',current?.id),seen=p&&state.attempts.some(a=>a.id===p.id);
    show(p,p?`Random textbook question. ${seen?'A repeat counts as review.':'This is an unseen question.'}`:'No questions match this topic.');return;
  }
  const p=P.chooseExam(scopedQuestions(),state,'',current?.id);
  show(p,p?`${topicName(p.topic)}: an unseen ${P.levels[p.level-1].toLowerCase()} question. Topics with lower recent accuracy receive more practice.`:'You have attempted every available textbook question in this selection. Review your misses or try random questions.');
}
$('check').onclick=()=>{
  if(!current||checked||revealed)return;
  resetFollowUp();cancelGeneration();
  cancelReview();stopCamera();drawing.finish();
  try{submittedAnswer=captureAnswer();}catch(error){$('feedback').hidden=false;$('feedback').className='wrong';$('feedback').textContent=error.message;return;}
  revealed=true;selected=submittedAnswer.choice;
  $('solution-body').innerHTML=current.solution;$('solution').hidden=false;$('solution').open=true;
  $('check').hidden=true;$('self-rating').hidden=true;$('feedback').hidden=false;$('feedback').className='';
  updatePhotoControls();
  if($('question-dock').hidden)$('solution').scrollIntoView({block:'start'});
  if(submittedAnswer.hasAnswer)verifyAnswer();
  else verificationFallback('No answer was submitted. The model solution is shown below. Self-check if you worked elsewhere.');
};
function captureWorking(){
  const answerInk=drawing.snapshot();
  if(answerInk&&!P.normalizeInk(answerInk))throw Error('This drawing is too large to save. Please shorten it or upload a photo of your work.');
  const work=[];
  if(answerInk){const image=encodePhoto(drawing.canvas,drawing.canvas.width,drawing.canvas.height);image.filename='drawn-answer-and-steps.jpg';work.push(image);}
  if(photo)work.push({...photo});
  return {answerInk,work,drawVersion:drawVersion};
}
function captureAnswer(){
  const choice=$('response-input').value,working=captureWorking();
  return {choice,...working,hasAnswer:!!(choice.trim()||working.work.length),seconds:Math.round((Date.now()-started)/1000)};
}
function verificationFallback(message){
  if(!current||checked||!revealed)return;
  $('feedback').hidden=false;$('feedback').className='';$('feedback').textContent=message+' You can compare your work and save a self-rating.';
  $('self-rating').hidden=false;$('verify-retry').hidden=!submittedAnswer?.hasAnswer;updatePhotoControls();
}
function recordSubmittedAnswer(correct,assessment='self',verification=null){
  const response=submittedAnswer;if(!current||checked||!revealed||!response)return false;
  cancelGeneration();
  try{P.record(state,current,response.choice,response.seconds,correct,{answerInk:response.answerInk,answerInputMode:'typed',assessment,answerVerification:verification,practiceSkill:current.coachSkill});}catch(error){verificationFallback(error.message);return false;}
  checked=true;activeAttempt=state.attempts[state.attempts.length-1];
  if(verification){activeAttempt.aiReview=verification;activeAttempt.aiReviewedAt=new Date().toISOString();state.items[current.id].aiConcern=AI.needsReview(verification);reviewedDrawVersion=response.drawVersion;}
  save();dashboard();$('response-input').readOnly=true;const dock=$('dock-response');if(dock)dock.readOnly=true;
  $('self-rating').hidden=true;$('feedback').hidden=false;$('feedback').className=correct?'':'wrong';
  const verdict=verification?{correct:'Correct',partly_correct:'Partly correct',incorrect:'Incorrect'}[verification.verdict]:'';
  $('feedback').textContent=(verification?'AI checked against the model answer: '+verdict+'. '+(verification.answer_check||verification.feedback).slice(0,400):correct?'Self-rated correct.':'Self-rated as needing practice.')+(correct?' Saved.':' Saved to your review queue.')+' Time spent: '+describeDuration(activeAttempt.seconds)+'.';
  $('next').hidden=false;$('skip').hidden=true;updatePhotoControls();
  if($('mode').value==='coach')$('adaptive-status').textContent='Answer saved. Choose Next question for practice based on this result.';
  if(!correct&&current.kind==='textbook'&&live.role!=='follower'&&$('followup-enabled').checked)startFollowUp(activeAttempt);
  return true;
}
function rateWork(correct){
  if(!current||checked||!revealed||reviewRequest)return;
  recordSubmittedAnswer(correct);
}
async function verifyAnswer(){
  if(!current||checked||!revealed||reviewRequest||!submittedAnswer?.hasAnswer)return;
  if(navigator.onLine===false){verificationFallback('Offline: automatic verification needs an internet connection. The model solution is available below.');return;}
  const problem=current,response=submittedAnswer,controller=new AbortController(),request={kind:'verify',problem,student,controller,started:Date.now(),timedOut:false};
  reviewRequest=request;$('self-rating').hidden=true;$('verify-retry').hidden=true;$('feedback').hidden=false;$('feedback').className='';
  const status=()=>{const text='Model answer is ready above. AI verification is running in the background… '+Math.round((Date.now()-request.started)/1000)+' seconds';$('feedback').textContent=text;$('ai-status').textContent=text;};
  status();request.ticker=setInterval(()=>{if(reviewRequest===request)status();},1000);
  request.timer=setTimeout(()=>{request.timedOut=true;controller.abort();},120000);updatePhotoControls();
  try{
    // Let the revealed solution paint before preparing images for the online check.
    // The timer also allows verification to continue in a background tab.
    await new Promise(resolve=>{const fallback=setTimeout(resolve,100);requestAnimationFrame(()=>requestAnimationFrame(()=>{clearTimeout(fallback);resolve();}));});
    if(controller.signal.aborted)throw new DOMException('Verification canceled.','AbortError');
    if(reviewRequest!==request||current!==problem||student!==request.student)return;
    const image=await questionAndWorkingImage(problem,response.work,controller.signal);
    if(controller.signal.aborted)throw new DOMException('Verification canceled.','AbortError');
    if(reviewRequest!==request||current!==problem||student!==request.student)return;
    const choice=response.choice+(response.work.length?'\n[Show your steps work attached under STUDENT WORK; combine it with the typed answer]':'');
    const message=AI.verificationPrompt(problem,choice,readableHTML(problem.html),readableHTML(problem.solution));
    const result=await fetch(AI.endpoint,{method:'POST',mode:'cors',credentials:'omit',headers:{'Content-Type':'application/json'},signal:controller.signal,body:JSON.stringify({message,image:image.image,mime_type:image.mime_type,filename:image.filename})});
    if(!result.ok)throw Error(result.status===413?'The submitted images are too large for verification.':'The verification service returned HTTP '+result.status+'.');
    const review=AI.parseResponse(await result.json());
    if(controller.signal.aborted||reviewRequest!==request||current!==problem||student!==request.student)return;
    if(AI.canVerify(review)){
      if(recordSubmittedAnswer(review.verdict==='correct','ai',review)){renderAIReview(review,$('ai-feedback'),'Answer verification against the model solution');$('ai-status').textContent='Answer verified and saved automatically.';}
    }else{
      renderAIReview(review,$('ai-feedback'),'Answer verification needs your review',true);
      verificationFallback(review.verdict==='unreadable'?'The submitted answer could not be read reliably.':'The service could not give a confident verdict.');
      $('ai-status').textContent='No automatic score was recorded.';
    }
  }catch(error){
    if(reviewRequest!==request||current!==problem||student!==request.student)return;
    verificationFallback(request.timedOut?'Answer verification timed out.':error.name==='AbortError'?'Answer verification was canceled.':error instanceof TypeError?'Could not reach the verification service. Check your internet connection and try again.':error.message);
    $('ai-status').textContent='Answer not automatically graded. Retry or self-check.';
  }finally{
    clearInterval(request.ticker);clearTimeout(request.timer);if(reviewRequest===request){reviewRequest=null;updatePhotoControls();}
  }
}
$('verify-retry').onclick=verifyAnswer;
$('rate-correct').onclick=()=>rateWork(true);$('rate-practice').onclick=()=>rateWork(false);
$('flag').onclick=()=>{if(!current)return;if(current.generatedData)state.generated={...state.generated,[current.id]:current.generatedData};const old=state.items[current.id]||{problem:current,missed:false,manual:false};old.manual=!old.manual;state.items[current.id]=old;save();flagButton();dashboard();};
$('next').onclick=()=>{next();$('question-title').focus();};$('skip').onclick=()=>{next();$('question-title').focus();};
$('mode').onchange=()=>{
  if($('mode').value==='chapter'&&!$('practice-chapter').value){
    const selectedChapters=chapters.filter(c=>bank.some(p=>p.chapter===c.chapter&&selectedTopics.has(p.topic)));
    const chapter=selectedChapters.length===1?selectedChapters[0]:null;
    if(chapter){$('practice-chapter').value=chapter.chapter;refreshTopicOptions();}
  }
  next(true);
};
$('topic-all').onclick=()=>{selectedTopics=new Set(availableTopics());syncTopicSelection();next(true);};
$('topic-clear').onclick=()=>{selectedTopics.clear();syncTopicSelection();next(true);};
document.addEventListener('click',e=>{if(!$('topic-picker').contains(e.target))$('topic-picker').open=false;});
$('topic-picker').addEventListener('keydown',e=>{if(e.key==='Escape'){$('topic-picker').open=false;$('topic-summary').focus();}});
$('practice-chapter').onchange=()=>{refreshTopicOptions();next(true);};
$('chapter-question').onchange=()=>{const p=selectedChapterQuestions().find(p=>p.id===$('chapter-question').value);if(p)showChapterQuestion(p);};
$('chapter-previous').onclick=()=>{const questions=selectedChapterQuestions(),index=questions.findIndex(p=>p.id===current?.id);if(index>0){showChapterQuestion(questions[index-1]);$('question-title').focus();}};
$('practice-day').onchange=()=>next(true);$('day-exclude-correct').onchange=()=>next(true);
$('day-question').onchange=()=>{const questions=selectedDayQuestions($('practice-day').value);const p=questions.find(p=>p.id===$('day-question').value);if(p)showDayQuestion(p,questions);};
$('review-button').onclick=()=>{$('mode').value='review';$('practice-chapter').value='';selectedTopics=new Set(P.topics);refreshTopicOptions();next();$('question-title').focus();};
$('export').onclick=()=>{const blob=new Blob([JSON.stringify(P.compact(state),null,2)],{type:'application/json'}),url=URL.createObjectURL(blob),a=document.createElement('a');a.href=url;a.download=`physicsUni-progress-${(student||'student').replace(/[^\w-]+/g,'_')}-${new Date().toISOString().slice(0,10)}.json`;a.click();setTimeout(()=>URL.revokeObjectURL(url),1000);};
$('import').onchange=async()=>{const file=$('import').files[0];if(!file)return;try{if(file.size>15000000)throw Error('too large');const s=JSON.parse(await file.text());if(!validState(s))throw Error('invalid');if(!window.confirm('Replace '+(student||'this student')+'’s progress with this backup?'))return;state=canonicalize(s);restorePracticeSelection();save();dashboard();next(true,false);}catch(e){$('storage-message').textContent='This file is not a valid University Physics practice backup. Your current progress has been kept.';}finally{$('import').value='';}};
// A formula image that cannot load is replaced by readable text, not raw LaTeX.
document.addEventListener('error',e=>{if(e.target.tagName==='IMG' && e.target.id!=='photo-preview'){const alt=e.target.alt||'',text=P.latexText(alt);const fallback=document.createElement('span');fallback.className='math-text';fallback.textContent=text||'[Diagram unavailable]';if(!text||/\[asy\]/i.test(alt))$('image-warning').hidden=false;e.target.replaceWith(fallback);}},true);
function readableHTML(html){
  const doc=new DOMParser().parseFromString(html||'','text/html');
  doc.querySelectorAll('img').forEach(img=>img.replaceWith(doc.createTextNode(' '+(P.latexText(img.alt)||'[Diagram]')+' ')));
  return doc.body.textContent.trim().slice(0,18000);
}
const hasWorking=()=>drawing.hasInk||!!photo;
// What the ✦ button does right now:
//  hint    – answer not checked yet: a nudge (reads any work so far) that never reveals the answer;
//  review  – answer checked and there is new work: check the steps (saved with the attempt);
//  explain – answer checked, nothing new to review: explain the question in the student's context.
function aiMode(){
  if(!checked)return revealed?'explain':'hint';
  const reviewedSame=!!activeAttempt?.aiReview&&reviewedDrawVersion===drawVersion&&!photo;
  return hasWorking()&&!reviewedSame?'review':'explain';
}
const AI_LABELS={hint:'AI hint (won’t give away the answer)',review:'AI check my steps',explain:'Ask AI to explain this question'};
function updatePhotoControls(){
  const busy=!!reviewRequest, cameraActive=cameraOpening||!!cameraStream, mode=aiMode();
  for(const id of ['rate-correct','rate-practice','verify-retry'])$(id).disabled=busy||checked;
  $('ai-check').disabled=!current||busy||cameraActive||!!drawing.active;
  {const label=mode==='review'&&activeAttempt?.aiReview?'AI check my steps again':AI_LABELS[mode];const b=$('ai-check');b.dataset.mode=mode;b.setAttribute('aria-label',label);b.title=label+'. Sends this question, your written answer and any drawing or photo to lakesideart.gochatus.org when you press this AI button.';b.classList.toggle('busy',busy);b.classList.remove('done');}
  for(const id of ['photo-camera','photo-file','photo-remove','drawing-open'])$(id).disabled=busy||cameraActive;
  drawing.enabled=!busy;
  for(const id of ['drawing-pen','drawing-eraser','drawing-close'])$(id).disabled=busy;
  document.querySelectorAll('[data-drawing-color]').forEach(button=>button.disabled=busy);
  $('drawing-undo').disabled=busy||!drawing.history.length||!!drawing.active;
  $('drawing-clear').disabled=busy||!drawing.hasInk||!!drawing.active;
  $('drawing-status').textContent=drawing.hasInk?'Your drawing is ready. Show answer verifies your submitted work, or press ✦ for optional AI help.':'Write your steps here. Answers stay hidden until you press Show answer.';
  $('ai-cancel').hidden=!busy;
  $('ai-cancel').setAttribute('aria-label',reviewRequest?.kind==='verify'?'Cancel answer verification':'Cancel review');$('ai-cancel').title=$('ai-cancel').getAttribute('aria-label');
  syncAnswerTools();
}
function cancelReview(){
  if(reviewRequest){const request=reviewRequest;reviewRequest=null;request.controller.abort();clearInterval(request.ticker);clearTimeout(request.timer);if(request.kind==='verify'&&current===request.problem)verificationFallback('Answer verification was canceled.');}
  updatePhotoControls();
}
function resetPhotoReview(){
  stopCamera();cancelReview();photoVersion++;photo=null;activeAttempt=null;drawingOpen=false;drawing.reset();reviewedDrawVersion=null;$('drawing-canvas').height=800;$('drawing-canvas').style.height='';drawing.render();requestAnimationFrame(()=>sizeCanvas());$('drawing-help').classList.remove('faded');
  $('drawing-panel').hidden=true;setDrawingLayout(false);setQuestionCollapsed(false);$('drawing-open').hidden=false;$('drawing-open').setAttribute('aria-expanded','false');drawingShift=false;syncDrawingTool();
  $('photo-section').hidden=true;$('photo-attachment').hidden=true;$('photo-preview').removeAttribute('src');
  $('photo-file').value='';$('ai-feedback').hidden=true;$('ai-feedback').replaceChildren();$('ai-status').textContent='';
}
async function preparePhoto(file){
  if(!file.type.startsWith('image/'))throw Error('Choose an image of your working (JPEG, PNG, or another browser-supported photo).');
  if(file.size>12*1024*1024)throw Error('Please choose a photo smaller than 12 MB.');
  const url=URL.createObjectURL(file),img=new Image();
  try{
    await new Promise((resolve,reject)=>{img.onload=resolve;img.onerror=()=>reject(Error('This photo could not be opened. Try a JPEG or PNG image.'));img.src=url;});
    if(!img.naturalWidth||!img.naturalHeight||img.naturalWidth*img.naturalHeight>60000000)throw Error('Please use a smaller photo.');
    return encodePhoto(img,img.naturalWidth,img.naturalHeight);
  }finally{URL.revokeObjectURL(url);}
}
function encodePhoto(source,width,height){
  const ratio=Math.min(1,1800/Math.max(width,height));
  const canvas=document.createElement('canvas');canvas.width=Math.round(width*ratio);canvas.height=Math.round(height*ratio);
  const ctx=canvas.getContext('2d');ctx.fillStyle='#fff';ctx.fillRect(0,0,canvas.width,canvas.height);ctx.drawImage(source,0,0,canvas.width,canvas.height);
  const dataURL=canvas.toDataURL('image/jpeg',.88);
  return {dataURL,image:dataURL.split(',')[1],mime_type:'image/jpeg',filename:'solution-steps.jpg'};
}
function stopCamera(){
  cameraVersion++;cameraOpening=false;
  if(cameraStream){cameraStream.getTracks().forEach(track=>track.stop());cameraStream=null;}
  const video=$('camera-video');video.pause();video.srcObject=null;
  $('camera-panel').hidden=true;$('camera-capture').disabled=true;$('photo-camera').setAttribute('aria-expanded','false');
  updatePhotoControls();
}
async function openCamera(){
  if(!current||reviewRequest||cameraOpening||cameraStream)return;
  if(!window.isSecureContext){$('ai-status').textContent='Camera access requires a secure page. Open this page over HTTPS or on localhost, or use Choose a photo.';return;}
  if(!navigator.mediaDevices?.getUserMedia){$('ai-status').textContent='This browser does not support live camera access. Open the page in a camera-enabled browser, or use Choose a photo.';return;}
  closeDrawing();const version=++cameraVersion;photoVersion++;cameraOpening=true;
  $('camera-panel').hidden=false;$('camera-capture').disabled=true;$('photo-camera').setAttribute('aria-expanded','true');
  $('camera-status').textContent='Allow camera access in your browser to see the live preview.';$('ai-status').textContent='';updatePhotoControls();
  try{
    const stream=await navigator.mediaDevices.getUserMedia({audio:false,video:{facingMode:{ideal:'environment'},width:{ideal:1920},height:{ideal:1080}}});
    if(version!==cameraVersion){stream.getTracks().forEach(track=>track.stop());return;}
    cameraStream=stream;cameraOpening=false;const video=$('camera-video');video.srcObject=stream;
    for(const track of stream.getVideoTracks())track.addEventListener('ended',()=>{
      if(cameraStream===stream){stopCamera();$('ai-status').textContent='The camera stopped. Click Take a photo to reopen it.';}
    });
    await video.play();
    if(version!==cameraVersion)return;
    cameraReady();updatePhotoControls();
  }catch(error){
    if(version!==cameraVersion)return;
    stopCamera();
    const messages={NotAllowedError:'Camera permission was blocked. Allow camera access for this page in your browser settings, then try again.',NotFoundError:'No camera was found. Connect a camera or use Choose a photo.',NotReadableError:'The camera could not start. Close other apps using it and try again.',SecurityError:'Your browser blocked camera access. Open this page directly over HTTPS and allow its camera permission.'};
    $('ai-status').textContent=messages[error.name]||'The camera could not start. Check your camera and browser permissions, or use Choose a photo.';
  }
}
function cameraReady(){
  const video=$('camera-video');
  if(!cameraStream||video.readyState<2||!video.videoWidth||!video.videoHeight)return;
  $('camera-capture').disabled=false;$('camera-status').textContent='Position your working in the frame, then click Capture photo.';
}
function capturePhoto(){
  const video=$('camera-video');if(!cameraStream||video.readyState<2||!video.videoWidth||!video.videoHeight)return;
  try{
    const captured=encodePhoto(video,video.videoWidth,video.videoHeight);photoVersion++;photo=captured;
    stopCamera();$('photo-file').value='';$('photo-preview').src=photo.dataURL;$('photo-attachment').hidden=false;
    $('ai-status').textContent='Photo captured. Click AI check my steps to send it for review.';updatePhotoControls();$('ai-check').focus();
  }catch(error){$('camera-status').textContent='Could not capture this frame. Please try again.';}
}
async function attachPhoto(event){
  const file=event.target.files[0];if(!file)return;
  closeDrawing();
  const version=++photoVersion;photo=null;$('photo-attachment').hidden=true;updatePhotoControls();$('ai-status').textContent='Preparing your photo…';
  try{const prepared=await preparePhoto(file);if(version!==photoVersion)return;photo=prepared;$('photo-preview').src=photo.dataURL;$('photo-attachment').hidden=false;$('ai-status').textContent='Photo ready. Click AI check my steps to send it for review.';}
  catch(error){if(version===photoVersion)$('ai-status').textContent=error.message;}
  finally{if(version===photoVersion)updatePhotoControls();}
}
function renderAIReview(review,container,heading='AI review of your steps',guidance=false){
  container.replaceChildren();container.hidden=false;
  const title=document.createElement('h3');title.textContent=heading;container.append(title);
  const labels={correct:'Reasoning looks correct',partly_correct:'Some steps need attention',incorrect:'Reasoning needs another look',unreadable:'A clearer photo is needed',unassessed:'Feedback without a structured assessment'};
  for(const content of [guidance?'':labels[review.verdict],review.answer_check,review.feedback]){if(content){const p=document.createElement('p');p.textContent=content;container.append(p);}}
  if(review.confidence==='low'&&!guidance){const p=document.createElement('p');p.className='small';p.textContent='The AI is uncertain. No weak points from this review were added to your learning log.';container.append(p);}
  if(review.steps.length){const list=document.createElement('ol');for(const step of review.steps){const li=document.createElement('li');li.textContent=[step.observation,step.correction].filter(Boolean).join(' — ');list.append(li);}container.append(list);}
  if(review.next_step){const p=document.createElement('p');p.textContent='Next step: '+review.next_step;container.append(p);}
}
function renderLearningLog(){
  const box=$('weak-points');box.replaceChildren();const weaknesses=AI.weaknesses(state);
  if(!weaknesses.length)box.textContent='Draw your steps or add a photo to start your learning log.';
  for(const weak of weaknesses){const row=document.createElement('div');row.className='weak-point';
    const title=document.createElement('strong');title.textContent=weak.skill;row.append(title);
    for(const content of [topicName(weak.topic)+' · observed in '+weak.count+' question'+(weak.count===1?'':'s'),weak.evidence,weak.practice]){const p=document.createElement('p');p.textContent=content;row.append(p);}
    const b=document.createElement('button');b.className='secondary';b.textContent='Practice '+topicName(weak.topic);b.onclick=()=>{$('mode').value='adaptive';$('practice-chapter').value=bank.find(p=>p.topic===weak.topic)?.chapter||'';selectedTopics=new Set([weak.topic]);refreshTopicOptions();next();$('question-title').focus();};row.append(b);box.append(row);
  }
  const history=$('ai-history-list');history.replaceChildren();
  const reviews=state.attempts.filter(a=>a.aiReview).slice().reverse();
  if(!reviews.length)history.textContent='No AI reviews saved yet.';
  for(const attempt of reviews){const details=document.createElement('details'),summary=document.createElement('summary');
    summary.textContent=attempt.title+' · '+new Date(attempt.aiReviewedAt||attempt.at).toLocaleDateString();details.append(summary);
    const body=document.createElement('div');renderAIReview(attempt.aiReview,body);details.append(body);history.append(details);
  }
}
// Original question crops accompany the combined typed answer, drawing and photo.
async function questionAndWorkingImage(problem,work,signal=null){
  const doc=new DOMParser().parseFromString(problem.html,'text/html');
  const solutionDoc=new DOMParser().parseFromString(problem.solution,'text/html');
  const references=[...doc.querySelectorAll('img')].map(img=>({src:img.getAttribute('src'),label:img.hasAttribute('data-context')?'QUESTION CONTEXT — original figures, tables and surrounding problems':'QUESTION — selected original textbook problem'}));
  references.push(...[...solutionDoc.querySelectorAll('img')].map(img=>({src:img.getAttribute('src'),label:'MODEL ANSWER — original reference solution, never student work'})));
  const sources=[...new Set(references.map(item=>item.src))];
  const decode=src=>new Promise((resolve,reject)=>{const img=new Image();
    const cleanup=()=>{img.onload=null;img.onerror=null;signal?.removeEventListener('abort',abort);};
    const abort=()=>{cleanup();img.src='';reject(new DOMException('Image preparation canceled.','AbortError'));};
    if(signal?.aborted){abort();return;}signal?.addEventListener('abort',abort,{once:true});
    img.onload=()=>{cleanup();resolve(img);};img.onerror=()=>{cleanup();reject(Error('Could not prepare the question images for AI.'));};img.src=src;
  });
  const decoded=new Map(await Promise.all(sources.map(async src=>[src,await decode(src)]))),images=references.map(item=>({...item,img:decoded.get(item.src)})),working=await Promise.all((work||[]).map(async item=>({img:await decode(item.dataURL),label:item.filename==='drawn-answer-and-steps.jpg'?'STUDENT WORK — handwritten answer and steps':'STUDENT WORK — uploaded photograph'})));
  const width=1400,padding=32,heights=images.map(({img})=>Math.round(img.height*Math.min(1,(width-padding*2)/img.width)));
  const blocks=working.map(block=>({...block,height:Math.round(block.img.height*Math.min(1,(width-padding*2)/block.img.width))}));
  const c=document.createElement('canvas');c.width=width;c.height=100+heights.reduce((a,b)=>a+b+90,0)+(blocks.length?blocks.reduce((total,b)=>total+90+b.height,0):60);
  const g=c.getContext('2d');g.fillStyle='#fff';g.fillRect(0,0,c.width,c.height);g.fillStyle='#183832';g.font='bold 26px sans-serif';g.fillText('QUESTION — original textbook diagrams and data',padding,45);
  let y=80;images.forEach(({img,label},i)=>{g.font='bold 20px sans-serif';g.fillText(label,padding,y+25);y+=50;const h=heights[i],w=Math.round(img.width*h/img.height);g.drawImage(img,padding,y,w,h);y+=h+40;});
  if(!blocks.length){g.fillStyle='#183832';g.font='bold 26px sans-serif';g.fillText('STUDENT WORK — no drawing or photo supplied',padding,y+35);}
  for(const block of blocks){g.fillStyle='#183832';g.font='bold 26px sans-serif';g.fillText(block.label,padding,y+35);y+=65;g.drawImage(block.img,padding,y,Math.round(block.img.width*block.height/block.img.height),block.height);y+=block.height+25;}
  // Preserve readable graph labels in long investigation composites.
  const dataURL=c.toDataURL('image/jpeg',.86);
  return {dataURL,image:dataURL.split(',')[1],mime_type:'image/jpeg',filename:'physics-question-and-working.jpg'};
}
async function askAI(){
  if(!current||reviewRequest||cameraOpening||cameraStream||drawing.active)return;
  const mode=aiMode(), problem=current, attempt=activeAttempt;
  let working;
  try{working=captureWorking();}catch(error){$('ai-status').textContent=error.message;return;}
  if(mode==='review'&&!working.work.length)return;
  if(mode==='review'&&!attempt)return;
  const sentDrawVersion=drawVersion,typedChoice=attempt?attempt.choice:$('response-input')?.value||'',choice=typedChoice+(working.work.length?'\n[Show your steps work attached under STUDENT WORK; combine it with the typed answer]':'');
  const statement=readableHTML(problem.html);
  const solution=readableHTML(problem.solution);
  const message=mode==='review'?AI.prompt(problem,choice,statement,solution):mode==='hint'?AI.hintPrompt(problem,choice,statement,solution,!!working.work.length):AI.explainPrompt({...problem,selfCorrect:attempt?.correct},choice,statement,solution,!!working.work.length);

  const busyText={hint:'Thinking of a hint…',review:'Reviewing your steps…',explain:'Preparing an explanation…'}[mode];
  const controller=new AbortController(),request={controller,started:Date.now(),timedOut:false};reviewRequest=request;
  request.ticker=setInterval(()=>{if(reviewRequest===request)$('ai-status').textContent=busyText+' '+Math.round((Date.now()-request.started)/1000)+' seconds';},1000);
  request.timer=setTimeout(()=>{request.timedOut=true;controller.abort();},120000);
  $('ai-status').textContent=busyText;updatePhotoControls();
  try{
    const image=await questionAndWorkingImage(problem,working.work,controller.signal);
    if(controller.signal.aborted||current!==problem)return;
    const response=await fetch(AI.endpoint,{method:'POST',mode:'cors',credentials:'omit',headers:{'Content-Type':'application/json'},signal:controller.signal,
      body:JSON.stringify({message,image:image.image,mime_type:image.mime_type,filename:image.filename})});
    if(!response.ok)throw Error(response.status===413?'The photo is too large for the grading service. Try a smaller photo.':'The AI service could not complete the request (HTTP '+response.status+'). You can retry.');
    const review=AI.parseResponse(await response.json());
    if(reviewRequest!==request||current!==problem)return;
    if(mode==='review'){
      if(!state.attempts.includes(attempt))return;
      attempt.aiReview=review;attempt.aiReviewedAt=new Date().toISOString();reviewedDrawVersion=sentDrawVersion;
      const item=state.items[problem.id];if(review.confidence!=='low'&&['correct','partly_correct','incorrect'].includes(review.verdict))item.aiConcern=AI.needsReview(review);
      save();dashboard();renderAIReview(review,$('ai-feedback'));
      $('ai-status').textContent='AI review saved. Your recorded answer result is unchanged. Edit your working and check again anytime.';
      photo=null;$('photo-attachment').hidden=true;$('photo-preview').removeAttribute('src');$('photo-file').value='';
    }else{
      // Hints and explanations are guidance only: shown, not saved, never added to the learning log.
      renderAIReview({...review,verdict:'unassessed',weak_points:[],answer_check:mode==='hint'?'':review.answer_check},$('ai-feedback'),mode==='hint'?'AI hint':'AI explanation',true);
      $('ai-status').textContent=mode==='hint'?'Here’s a hint. It won’t give away the answer.':'Explanation ready below the pad.';
    }
  }catch(error){
    if(reviewRequest!==request)return;
    $('ai-status').textContent=request.timedOut?'The AI request timed out. Your progress is unchanged; you can retry.':error.name==='AbortError'?'Request canceled. Your progress is unchanged.':error instanceof TypeError?'Could not reach the AI service. Check your connection or the site’s cross-origin settings, then retry. Your progress is unchanged.':error.message;
  }finally{
    clearInterval(request.ticker);clearTimeout(request.timer);if(reviewRequest===request){reviewRequest=null;updatePhotoControls();}
  }
}
function syncDrawingTool(){
  document.querySelectorAll('[data-drawing-color]').forEach(button=>button.setAttribute('aria-pressed',String(button.dataset.drawingColor===drawing.color)));
  const erasing=drawingShift||drawing.tool==='eraser';
  $('drawing-pen').setAttribute('aria-pressed',String(!erasing));$('drawing-eraser').setAttribute('aria-pressed',String(erasing));
  $('drawing-canvas').classList.toggle('erasing',erasing);
}
// While drawing, the question narrows to one third so the pad gets the remaining two thirds.
function setDrawingLayout(on){document.querySelector('.question-card').classList.toggle('drawing-active',on);}
// The question can be folded away while the answer field stays visible.
function setQuestionCollapsed(collapsed){document.querySelector('.question-card').classList.toggle('question-collapsed',collapsed);const t=$('question-toggle');t.setAttribute('aria-expanded',String(!collapsed));t.querySelector('.question-toggle-label').textContent=collapsed?'Show question':'Hide question';t.querySelector('.question-toggle-title').textContent=collapsed?$('question-title').textContent:'';t.querySelector('.question-toggle-icon').textContent=collapsed?'▸':'▾';t.title=collapsed?'Show the question text':'Fold the question text away';}
$('question-toggle').onclick=()=>setQuestionCollapsed($('question-toggle').getAttribute('aria-expanded')==='true');
function closeDrawing(){
  drawing.finish();drawingOpen=false;drawingShift=false;syncDrawingTool();$('drawing-panel').hidden=true;setDrawingLayout(false);$('drawing-open').hidden=false;$('drawing-open').setAttribute('aria-expanded','false');$('photo-attachment').hidden=!photo;updatePhotoControls();
}
function openDrawing(focus=false){
  if(reviewRequest)return;
  stopCamera();photoVersion++;drawingOpen=true;$('drawing-panel').hidden=false;setDrawingLayout(true);$('drawing-open').hidden=true;$('drawing-open').setAttribute('aria-expanded','true');$('photo-attachment').hidden=true;
  $('ai-status').textContent='';updatePhotoControls();if(focus)$('drawing-canvas').focus({preventScroll:true});
}
$('drawing-open').onclick=()=>openDrawing(true);
$('drawing-close').onclick=()=>{closeDrawing();$('ai-status').textContent=photo?'Photo selected for AI review. Your drawing is kept in the pad.':'Drawing kept for Show answer. Reopen it with the pencil button to continue.';$('drawing-open').focus();};
$('drawing-pen').onclick=()=>{drawing.tool='pen';syncDrawingTool();};$('drawing-eraser').onclick=()=>{drawing.tool='eraser';syncDrawingTool();};
document.querySelectorAll('[data-drawing-color]').forEach(button=>{button.onclick=()=>{drawing.color=button.dataset.drawingColor;drawing.tool='pen';syncDrawingTool();};});
document.addEventListener('keydown',event=>{if(event.key==='Shift'&&drawingOpen){drawingShift=true;syncDrawingTool();}});
document.addEventListener('keyup',event=>{if(event.key==='Shift'){drawingShift=false;syncDrawingTool();}});
window.addEventListener('blur',()=>{drawingShift=false;syncDrawingTool();});
for(const type of ['pointerdown','pointermove'])$('drawing-canvas').addEventListener(type,event=>{drawingShift=!!event.shiftKey;syncDrawingTool();});
$('drawing-undo').onclick=()=>drawing.undo();$('drawing-clear').onclick=()=>drawing.clear();
$('photo-file').onchange=attachPhoto;$('photo-camera').onclick=openCamera;
$('camera-video').addEventListener('loadeddata',cameraReady);$('camera-video').addEventListener('canplay',cameraReady);
$('camera-capture').onclick=capturePhoto;
$('camera-close').onclick=()=>{stopCamera();$('ai-status').textContent='Camera closed.';$('photo-camera').focus();};
window.addEventListener('pagehide',stopCamera);
document.addEventListener('visibilitychange',()=>{if(document.hidden)stopCamera();});
document.addEventListener('keydown',event=>{if(event.key==='Escape'&&!$('camera-panel').hidden){stopCamera();$('photo-camera').focus();}});
$('photo-remove').onclick=()=>{photoVersion++;photo=null;$('photo-attachment').hidden=true;$('photo-preview').removeAttribute('src');$('photo-file').value='';$('ai-status').textContent='Photo removed.';updatePhotoControls();};
$('ai-check').onclick=askAI;
$('ai-cancel').onclick=()=>{const verifying=reviewRequest?.kind==='verify';cancelReview();$('ai-status').textContent=verifying?'Answer verification canceled. Retry or self-check; no automatic score was recorded.':'Review canceled. Your progress is unchanged; the working can be retried.';};
function setSidebar(open){$('layout').classList.toggle('sidebar-collapsed',!open);$('sidebar-body').hidden=!open;$('sidebar-toggle').setAttribute('aria-expanded',String(open));$('sidebar-toggle').querySelector('.sidebar-toggle-icon').textContent=open?'›':'‹';$('sidebar-toggle').title=open?'Hide progress panel':'Show progress panel';}
$('sidebar-toggle').onclick=()=>setSidebar($('sidebar-body').hidden);setSidebar(false);
// Browser full screen (hides tabs and toolbars); Esc or the button exits.
(()=>{const b=$('fullscreen'),root=document.documentElement;if(!root.requestFullscreen||!document.fullscreenEnabled)return;b.hidden=false;
const sync=()=>{const on=!!document.fullscreenElement;b.textContent=on?'Exit full screen':'⛶ Full screen';b.setAttribute('aria-pressed',String(on));};
b.onclick=()=>{(document.fullscreenElement?document.exitFullscreen():root.requestFullscreen()).catch(()=>{});};document.addEventListener('fullscreenchange',sync);sync();})();
// iPad defaults to Apple Pencil only (palm-safe, fingers scroll); the hand button allows finger drawing. Remembered per browser.
(()=>{const ua=navigator.userAgent,touch=navigator.maxTouchPoints>0,iPad=/iPad/.test(ua)||(/Macintosh/.test(ua)&&navigator.maxTouchPoints>1);
if(!touch)return;const btn=$('drawing-finger'),canvas=$('drawing-canvas');btn.hidden=false;
let finger=!iPad;try{const saved=localStorage.getItem('physicsUni-finger-drawing');if(saved!==null)finger=saved==='1';}catch(e){}
const apply=()=>{drawing.pencilOnly=!finger;btn.setAttribute('aria-pressed',String(finger));btn.title=finger?'Finger drawing on (tap for Apple Pencil only)':'Apple Pencil only (tap to draw with finger)';canvas.classList.toggle('pencil-only',!finger);};
btn.onclick=()=>{finger=!finger;try{localStorage.setItem('physicsUni-finger-drawing',finger?'1':'0');}catch(e){}apply();$('drawing-status').textContent=finger?'Finger drawing is on.':'Apple Pencil only. Fingers scroll the page.';};
drawing.onTouchIgnored=()=>{$('drawing-status').textContent='Apple Pencil only. Tap the hand button to draw with your finger.';};apply();})();
// Two-finger tap on the pad swaps between Pen and Object eraser (touch screens, mainly iPad).
(()=>{if(!(navigator.maxTouchPoints>0))return;const canvas=$('drawing-canvas');let tap=null;
canvas.addEventListener('touchstart',e=>{const fingers=[...e.touches].filter(t=>t.touchType!=='stylus');
  if(fingers.length===2&&e.touches.length===2){if(drawing.active)drawing.cancel();tap={at:performance.now(),pts:fingers.map(t=>({id:t.identifier,x:t.clientX,y:t.clientY}))};}
  else if(e.touches.length>2)tap=null;},{passive:true});
canvas.addEventListener('touchmove',e=>{if(!tap)return;for(const t of e.touches){const p=tap.pts.find(q=>q.id===t.identifier);if(p&&Math.hypot(t.clientX-p.x,t.clientY-p.y)>18){tap=null;return;}}},{passive:true});
canvas.addEventListener('touchcancel',()=>{tap=null;});
canvas.addEventListener('touchend',e=>{if(!tap||e.touches.length)return;const quick=performance.now()-tap.at<350;tap=null;if(!quick||!drawing.enabled||$('drawing-pen').disabled)return;
  drawing.tool=drawing.tool==='eraser'?'pen':'eraser';syncDrawingTool();$('drawing-status').textContent=drawing.tool==='eraser'?'Object eraser selected (two-finger tap for Pen).':'Pen selected (two-finger tap for Object eraser).';});})();
// Pinned controls mirror the written response and self-rating.
(()=>{const box=$('dock-choices');
  const syncResponse=()=>{const real=$('response-input');if(!real){box.replaceChildren();return;}
    let d=$('dock-response');if(!d){d=document.createElement('textarea');d.id='dock-response';d.rows=2;d.maxLength=12000;d.placeholder='Your answer…';d.setAttribute('aria-label','Your written answer (pinned)');d.oninput=()=>{const r=$('response-input');if(r){r.value=d.value;r.dispatchEvent(new Event('input'));}};
      box.replaceChildren(d);
    }
    d.value=real.value;d.readOnly=real.readOnly;

  };
const syncButtons=()=>{for(const id of ['check','next','skip','verify-retry']){const r=$(id),d=$('dock-'+id);d.hidden=r.hidden;d.disabled=r.disabled;d.textContent=r.textContent;if(r.hasAttribute('aria-busy'))d.setAttribute('aria-busy',r.getAttribute('aria-busy'));else d.removeAttribute('aria-busy');}
    for(const id of ['rate-correct','rate-practice'])$('dock-'+id).disabled=$(id).disabled;
    $('dock-self-rating').hidden=$('self-rating').hidden;
    const f=$('feedback'),df=$('dock-feedback');df.hidden=f.hidden;df.className='dock-feedback'+(f.classList.contains('wrong')?' wrong':'');df.textContent=f.textContent;};
  for(const id of ['check','next','skip','rate-correct','rate-practice','verify-retry'])$('dock-'+id).onclick=()=>$(id).click();
  new MutationObserver(syncResponse).observe($('choice-list'),{childList:true,subtree:true,attributes:true,attributeFilter:['readonly']});
  const mo=new MutationObserver(syncButtons);for(const id of ['check','next','skip','self-rating','rate-correct','rate-practice','verify-retry'])mo.observe($(id),{attributes:true,childList:true});
  mo.observe($('feedback'),{attributes:true,childList:true,subtree:true,characterData:true});syncResponse();syncButtons();
})();
// The pinned copy mirrors "Understand the solution": same content, opened when the main one opens after a check.
(()=>{const real=$('solution'),copy=$('dock-solution');
const sync=()=>{copy.hidden=real.hidden;if(real.hidden){copy.open=false;$('dock-solution-body').replaceChildren();return;}
  const body=$('solution-body').cloneNode(true);body.querySelectorAll('[id]').forEach(n=>n.removeAttribute('id'));$('dock-solution-body').replaceChildren(...body.childNodes);};
let wasHidden=real.hidden;
new MutationObserver(()=>{sync();if(wasHidden&&!real.hidden){copy.open=real.open;if(copy.open)requestAnimationFrame(()=>copy.scrollIntoView({block:'nearest'}));}wasHidden=real.hidden;})
  .observe(real,{attributes:true,attributeFilter:['hidden','open'],childList:true,subtree:true,characterData:true});sync();})();
// AI status shows as a short-lived toast (stays up while a review is running).
(()=>{const el=$('ai-status');let timer=null;new MutationObserver(()=>{clearTimeout(timer);el.classList.remove('faded');if(el.textContent&&!/^Reviewing/.test(el.textContent))timer=setTimeout(()=>el.classList.add('faded'),6000);}).observe(el,{childList:true,characterData:true,subtree:true});})();
// Keep the whole pinned copy (and its answer buttons) inside the viewport, even before it reaches its sticky position.
(()=>{const dock=$('question-dock');let raf=0;
const fit=()=>{raf=0;if(dock.hidden)return;const top=Math.max(12,dock.getBoundingClientRect().top);dock.style.maxHeight=Math.max(220,innerHeight-top-12)+'px';};
const queue=()=>{if(!raf)raf=requestAnimationFrame(fit);};
addEventListener('scroll',queue,{passive:true});addEventListener('resize',queue);
new MutationObserver(queue).observe(dock,{attributes:true,attributeFilter:['hidden']});})();
// While the question is pinned at the left, the pad grows as tall as the screen allows (never shorter than 3:2).
// The canvas keeps 1200 drawing units across and gains units downward, so strokes never move or stretch; it also
// never shrinks below the lowest stroke, so nothing drawn is ever hidden.
function sizeCanvas(){
  const c=$('drawing-canvas');if(drawing.active||!c.clientWidth)return;
  const w=c.clientWidth,docked=$('steps-wrap').classList.contains('docked');
  const head=document.querySelector('.steps-head').offsetHeight+60; // row + pad padding/borders + small margins
  const target=docked?Math.max(w*2/3,innerHeight-head-24):w*2/3;
  const lowest=drawing.strokes.reduce((m,s)=>Math.max(m,...s.points.map(p=>p.y+s.width)),0);
  const units=Math.max(800,Math.round(1200*target/w),Math.ceil(lowest+10));
  c.style.height=(w*units/1200)+'px';
  if(c.height!==units){c.height=units;drawing.render();}
}
{let raf=0;const q=()=>{if(!raf)raf=requestAnimationFrame(()=>{raf=0;sizeCanvas();});};
 new MutationObserver(q).observe($('steps-wrap'),{attributes:true,attributeFilter:['class']});
 new MutationObserver(q).observe($('drawing-panel'),{attributes:true,attributeFilter:['hidden']});
 addEventListener('resize',q);}
// Pin a compact copy of the question beside the pad once the real one scrolls above the viewport.
(()=>{const wrap=$('steps-wrap'),dock=$('question-dock'),area=$('question-area');let above=false;
const refresh=()=>{$('question-dock-title').replaceChildren(...(current?.generatedData?[aiMarker(),document.createTextNode(' ')]:[]),document.createTextNode($('question-title').textContent));const body=$('statement').cloneNode(true);body.querySelectorAll('[id]').forEach(n=>n.removeAttribute('id'));$('question-dock-body').replaceChildren(...body.childNodes);};
const update=()=>{const b=area.getBoundingClientRect().bottom;above=area.offsetParent!==null&&(dock.hidden?b<=0:b<=60);const on=above&&document.querySelector('.question-card').classList.contains('drawing-active')&&!document.querySelector('.question-card').classList.contains('question-collapsed');if(on===!dock.hidden)return;if(on){refresh();wrap.style.minHeight=wrap.offsetHeight+'px';}else wrap.style.minHeight='';dock.hidden=!on;wrap.classList.toggle('docked',on);};
{let r=0;addEventListener('scroll',()=>{if(!r)r=requestAnimationFrame(()=>{r=0;update();});},{passive:true});}
if('IntersectionObserver' in window)new IntersectionObserver(([e])=>{above=!e.isIntersecting&&e.boundingClientRect.bottom<=0;update();}).observe(area);
new MutationObserver(()=>{if(!dock.hidden)refresh();}).observe($('statement'),{childList:true,subtree:true});
new MutationObserver(update).observe(document.querySelector('.question-card'),{attributes:true,attributeFilter:['class']});
$('question-dock-top').onclick=()=>{document.querySelector('.question-card').scrollIntoView({behavior:'smooth',block:'start'});};})();
// FOLLOWUP_CONTROLS
dashboard();if(!followRequested)next();else show(null,'Connecting to the live session…',true);
if(followRequested){
  const id=liveParams.get('follow'),key=new URLSearchParams(location.hash.slice(1)).get('liveKey')||students.getApiKey();
  if(window.LivePractice.validId(id))live.follow(id,key).catch(()=>{});
  else{live.role='follower';setLiveStatus('invalid');}
}
if(students.current())useStudent(students.current());else if(!followRequested)showLogin();
