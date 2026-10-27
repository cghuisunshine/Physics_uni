// Follow-up practice belongs to a missed textbook attempt, separate from its score.
const FQ=window.PhysicsFollowUp,followUpSetting='physicsUniPracticeFollowUp';
let followUpRequest=null,followUpSource=null,followUpQuestion=null,followUpChoice=null,followUpChecked=false,followUpRevealed=false;
try{$('followup-enabled').checked=localStorage.getItem(followUpSetting)!=='false';}catch{}
function setFollowUpBusy(busy){
  $('followup').setAttribute('aria-busy',String(busy));$('followup-cancel').hidden=!busy;
}
function resetFollowUp(){
  if(followUpRequest){const request=followUpRequest;followUpRequest=null;clearTimeout(request.timer);request.controller.abort();}
  followUpSource=null;followUpQuestion=null;followUpChoice=null;followUpChecked=false;followUpRevealed=false;
  $('followup').hidden=true;$('followup-content').hidden=true;$('followup-status').textContent='';
  $('followup-statement').textContent='';$('followup-choices').replaceChildren();$('followup-feedback').textContent='';$('followup-solution').textContent='';$('followup-solution').hidden=true;
  for(const id of ['followup-check','followup-retry','followup-reveal'])$(id).hidden=true;
  setFollowUpBusy(false);
}
function followUpRecord(){return followUpSource&&state.attempts.includes(followUpSource)&&followUpSource.id===current?.id?followUpSource.followUp:null;}
function renderFollowUpChoices(){
  $('followup-choices').replaceChildren();
  followUpQuestion.choices.forEach((value,i)=>{
    const letter='ABCDE'[i],button=document.createElement('button');button.type='button';button.className='followup-choice';button.textContent=letter+'. '+value;
    button.setAttribute('aria-pressed',String(followUpChoice===letter));button.disabled=followUpChecked||followUpRevealed;
    button.classList.toggle('selected',followUpChoice===letter);
    if(followUpChecked&&followUpChoice===letter)button.classList.add(letter===followUpQuestion.answer?'correct':'incorrect');
    button.onclick=()=>{followUpChoice=letter;renderFollowUpChoices();$('followup-check').disabled=false;};$('followup-choices').append(button);
  });
}
function renderFollowUp(record){
  followUpQuestion=record.question;followUpRevealed=record.revealed;
  const last=record.answers.at(-1);followUpChoice=last?.choice||null;followUpChecked=!!last;
  $('followup').hidden=false;$('followup-content').hidden=false;$('followup-statement').textContent=followUpQuestion.text;
  $('followup-status').textContent='AI practice question · Apply the same method to a new situation.';
  $('followup-feedback').textContent=last?(last.correct?'Correct! You applied the method to a new problem.':'Not quite. Compare your steps with the original solution, then try again.'):'';
  $('followup-check').hidden=!!last||record.revealed;$('followup-check').disabled=!followUpChoice;
  $('followup-retry').hidden=!!last?.correct&&!record.revealed;
  // An unanswered new question needs no retry action yet.
  if(!last&&!record.revealed)$('followup-retry').hidden=true;
  $('followup-retry').textContent=record.revealed?'Try another similar question':'Try again';
  $('followup-reveal').hidden=!last||last.correct||record.revealed;
  const showSolution=record.revealed||last?.correct;
  $('followup-solution').hidden=!showSolution;
  $('followup-solution').textContent=showSolution?'Answer '+followUpQuestion.answer+'. '+followUpQuestion.explanation:'';
  renderFollowUpChoices();
}
function restoreFollowUp(problem){
  if(!problem||problem.kind!=='textbook'||!$('followup-enabled').checked||live.role==='follower')return false;
  const attempt=state.attempts.filter(a=>a.id===problem.id).at(-1),record=!attempt?.correct&&FQ.normalizeRecord(attempt?.followUp);
  if(!record)return false;
  attempt.followUp=record;followUpSource=attempt;renderFollowUp(record);return true;
}
async function startFollowUp(attempt=followUpSource||activeAttempt){
  const problem=current,owner=student,previous=followUpQuestion?.text||attempt?.followUp?.question?.text||'';
  resetFollowUp();
  if(!owner||!problem||problem.kind!=='textbook'||!attempt||attempt.id!==problem.id||attempt.correct!==false||!state.attempts.includes(attempt)||!$('followup-enabled').checked||live.role==='follower')return;
  followUpSource=attempt;$('followup').hidden=false;
  if(navigator.onLine===false){$('followup-status').textContent='You are offline. Reconnect, then retry creating a similar question. Your textbook answer is saved.';$('followup-retry').hidden=false;$('followup-retry').textContent='Retry creating question';return;}
  $('followup-status').textContent='Creating a similar question using the same solution method…';setFollowUpBusy(true);
  const controller=new AbortController(),request={controller,timedOut:false};followUpRequest=request;
  request.timer=setTimeout(()=>{request.timedOut=true;controller.abort();},120000);
  const stillCurrent=()=>followUpRequest===request&&current===problem&&student===owner&&followUpSource===attempt&&$('followup-enabled').checked&&live.role!=='follower';
  try{
    const image=await questionAndWorkingImage(problem,[],controller.signal);
    if(controller.signal.aborted)throw new DOMException('Question creation canceled.','AbortError');
    if(!stillCurrent())return;
    const response=await fetch(AI.endpoint,{method:'POST',mode:'cors',credentials:'omit',headers:{'Content-Type':'application/json'},signal:controller.signal,
      body:JSON.stringify({message:FQ.prompt(problem,attempt,readableHTML(problem.html),readableHTML(problem.solution),previous),image:image.image,mime_type:image.mime_type,filename:image.filename})});
    if(!response.ok)throw Error('Could not create the similar question (HTTP '+response.status+'). Please retry.');
    const question=FQ.parseResponse(await response.json(),previous);
    if(controller.signal.aborted)throw new DOMException('Question creation canceled.','AbortError');
    if(!stillCurrent())return;
    attempt.followUp={question,answers:[],revealed:false};save();renderFollowUp(attempt.followUp);
  }catch(error){
    if(!stillCurrent())return;
    $('followup-status').textContent=request.timedOut?'Creating the question timed out. Please retry.':error.name==='AbortError'?'Question creation canceled.':error instanceof TypeError?'Could not reach the AI tutor. Check your connection and retry.':error.message;
    $('followup-retry').hidden=false;$('followup-retry').textContent='Retry creating question';
  }finally{clearTimeout(request.timer);if(followUpRequest===request){followUpRequest=null;setFollowUpBusy(false);}}
}
$('followup-enabled').onchange=()=>{
  try{localStorage.setItem(followUpSetting,String($('followup-enabled').checked));}catch{}
  resetFollowUp();
  if($('followup-enabled').checked&&!restoreFollowUp(current)&&checked&&activeAttempt?.correct===false)startFollowUp(activeAttempt);
};
$('followup-cancel').onclick=()=>{
  const attempt=followUpSource;resetFollowUp();followUpSource=attempt;$('followup').hidden=false;
  $('followup-status').textContent='Question creation canceled. Your textbook answer is saved.';$('followup-retry').hidden=false;$('followup-retry').textContent='Retry creating question';
};
$('followup-check').onclick=()=>{
  const record=followUpRecord();if(!student||!record||!followUpQuestion||!followUpChoice||followUpChecked||followUpRevealed)return;
  if(record.answers.length>=100){$('followup-reveal').hidden=false;$('followup-check').hidden=true;$('followup-feedback').textContent='This question has reached its saved retry limit. Reveal the solution to practise another similar question.';return;}
  record.answers.push({choice:followUpChoice,correct:followUpChoice===followUpQuestion.answer,at:new Date().toISOString()});save();renderFollowUp(record);
};
$('followup-retry').onclick=()=>{
  if(!followUpQuestion||followUpRevealed){startFollowUp();return;}
  followUpChoice=null;followUpChecked=false;renderFollowUpChoices();$('followup-feedback').textContent='';
  $('followup-check').hidden=false;$('followup-check').disabled=true;$('followup-retry').hidden=true;$('followup-reveal').hidden=true;
};
$('followup-reveal').onclick=()=>{
  const record=followUpRecord();if(!record)return;
  record.revealed=true;save();renderFollowUp(record);
};
