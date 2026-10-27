/* Read-only activity page; no student login and no history writes. */
(()=>{
  'use strict';
  const $=id=>document.getElementById(id),A=window.ActivityMonitor;
  const params=new URLSearchParams(location.search),fragment=new URLSearchParams(location.hash.slice(1));
  let key=fragment.get('apiKey')||params.get('apiKey')||'',off=null,state=null,updated='',name='';
  try{key=key||localStorage.getItem('physicsUniFirebaseApiKey')||'';}catch{}
  const goal=Number(params.get('goal')||10);
  $('activity-student').value=params.get('student')||'Bruce';$('activity-goal').value=Number.isInteger(goal)&&goal>=1&&goal<=1000?goal:10;
  $('activity-period').value=params.get('period')==='week'?'week':'cycle';
  const excluded=params.has('exclude')?params.get('exclude').split(',').filter(Boolean).map(Number):[3,6];
  const inputs=[...$('activity-filter').querySelectorAll('input')];for(const input of inputs)input.checked=excluded.includes(Number(input.value));
  $('monitor-key').value=key?'••••••••':'';
  function render(){
    const excluded=inputs.filter(i=>i.checked).map(i=>Number(i.value)),cycle=$('activity-period').value==='cycle';
    $('activity-period-label').textContent=cycle?'Between tutoring days':'Today and the preceding six days';
    const list=$('activity-days');list.replaceChildren();if(!state)return;
    const goal=Number($('activity-goal').value),days=cycle?A.cycleDays(state.attempts,new Date(),excluded):A.days(state.attempts,new Date(),excluded);
    if(!days.length){list.textContent='All days in this window are excluded.';return;}
    for(const day of days){
      const row=document.createElement('div');row.className='activity-day';
      const labels=document.createElement('div'),label=document.createElement('span'),count=document.createElement('span');
      label.textContent=day.label+(day.upcoming?' · Upcoming':'')+(day.tutoring?' · Tutoring':'');count.textContent=day.tutoring?'No practice goal':`${day.total} / ${goal} answers`;labels.append(label,count);row.append(labels);
      if(!day.tutoring){const bar=document.createElement('progress');bar.max=goal;bar.value=Math.min(goal,day.total);bar.setAttribute('aria-label',`${name}: ${day.total} answers, goal ${goal}`);row.append(bar);}
      const detail=document.createElement('p');detail.className='small';detail.textContent=day.tutoring?'End of this practice interval.':day.upcoming?`Planned practice · goal ${goal} answers`:`${day.correct} correct · ${day.retries} retries · ${Math.round(day.seconds/60)} minutes recorded`;row.append(detail);list.append(row);
    }
    $('activity-updated').textContent=updated?'History last updated: '+new Date(updated).toLocaleString('en-CA',{timeZone:'America/Vancouver'})+' (Vancouver)':'';
  }
  function loadLocal(){
    try{const id=encodeURIComponent(name.trim().replace(/\s+/g,' ').toLowerCase()).slice(0,200),data=JSON.parse(localStorage.getItem('physicsUniPractice.v1:'+id)||'null');state=A.readPayload(data);updated=data?.updatedAt||'';}catch{state=null;updated='';}
    $('activity-status').textContent=state?'Showing history saved on this device. Configure sync to monitor another device.':'No saved history for this student on this device. Configure sync to monitor another device.';render();
  }
  function view(){
    if(!$('activity-form').reportValidity())return;
    name=$('activity-student').value.trim();$('activity-title').textContent=name+'’s activity';if(off)off();off=null;state=null;updated='';
    if(!key){loadLocal();return;}
    off=A.watch(name,key,{onData:data=>{state=A.readPayload(data);updated=data?.updatedAt||'';render();},onStatus:(kind,error)=>{
      $('activity-status').textContent={connecting:'Connecting to synced history…',cached:'Showing cached history; reconnecting…',synced:state?'Connected · live updates enabled.':'No synced history found. Enable sync on the student’s device.',error:error?.code==='permission-denied'?'Firebase denied access to this history.':'Could not connect. Check the key and connection.'}[kind]||'Enter a Firebase API key to monitor synced history.';
    }});
  }
  $('activity-form').onsubmit=e=>{e.preventDefault();view();};$('activity-period').onchange=render;$('activity-filter').onchange=render;$('activity-goal').oninput=()=>{if($('activity-goal').checkValidity())render();};
  $('monitor-connect').onclick=()=>{const value=$('monitor-key').value.trim();if(value&&!/^•+$/.test(value))key=value;view();};
  $('activity-share').onclick=async()=>{const url=A.shareURL(location.href,{student:$('activity-student').value.trim(),goal:Number($('activity-goal').value),excluded:inputs.filter(i=>i.checked).map(i=>Number(i.value)),period:$('activity-period').value,key});try{await navigator.clipboard.writeText(url);$('activity-share-status').textContent='Monitoring link copied.';}catch{window.prompt('Copy this monitoring link:',url);}};
  addEventListener('storage',()=>{if(!key)loadLocal();});setInterval(render,60000);view();
})();
