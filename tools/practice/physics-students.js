/* Per-student persistence, modelled on family_todo_login.html:
   - the student name is a simple login kept in localStorage (no password);
   - each student's history is saved locally first (works offline);
   - optional Firebase Firestore sync across devices, enabled by an API key
     from the settings box or a shared link (?apiKey=...), stored under the same
     "physicsUniFirebaseApiKey" localStorage key the todo page uses. */
(function(root){
'use strict';
const FIREBASE_CONFIG={authDomain:"homeinventory-4718c.firebaseapp.com",projectId:"homeinventory-4718c",storageBucket:"homeinventory-4718c.firebasestorage.app",messagingSenderId:"719884896213",appId:"1:719884896213:web:e93d5dffc79dec10995f5c"};
const FIREBASE_COLLECTION="physicsUniPracticeStudents";
const FIREBASE_API_KEY_KEY="physicsUniFirebaseApiKey", LOGIN_KEY="physicsUniPracticeStudent", KNOWN_KEY="physicsUniPracticeKnownStudents", LOCAL_PREFIX="physicsUniPractice.v1:", LEGACY_KEY="physicsUniPractice.v1";
const store={};
const ls={get:k=>{try{return localStorage.getItem(k);}catch(e){return null;}},set:(k,v)=>{try{localStorage.setItem(k,v);return true;}catch(e){return false;}},del:k=>{try{localStorage.removeItem(k);}catch(e){}}};
// Names are matched case-insensitively; the id is safe as a Firestore document id.
store.idFor=name=>encodeURIComponent(String(name).trim().replace(/\s+/g,' ').toLowerCase()).slice(0,200);
store.current=()=>ls.get(LOGIN_KEY)||'';
store.known=()=>{try{const v=JSON.parse(ls.get(KNOWN_KEY)||'[]');return Array.isArray(v)?v.filter(n=>typeof n==='string'):[];}catch(e){return [];}};
// Names are case-insensitive: "amy", "AMY" and "Amy" are the same student, shown with the first spelling used.
store.login=name=>{name=String(name).trim().replace(/\s+/g,' ');const same=store.known().find(n=>store.idFor(n)===store.idFor(name));if(same)name=same;ls.set(LOGIN_KEY,name);const known=store.known().filter(n=>store.idFor(n)!==store.idFor(name));known.unshift(name);ls.set(KNOWN_KEY,JSON.stringify(known.slice(0,20)));return name;};
store.forget=name=>{ls.set(KNOWN_KEY,JSON.stringify(store.known().filter(n=>store.idFor(n)!==store.idFor(name))));};
store.loadLocal=name=>{try{const raw=ls.get(LOCAL_PREFIX+store.idFor(name));return raw?JSON.parse(raw):null;}catch(e){return null;}};
store.saveLocal=(name,payload)=>ls.set(LOCAL_PREFIX+store.idFor(name),JSON.stringify(payload));
// Progress saved before student logins existed goes to the first student who signs in on this device.
store.takeLegacy=()=>{const raw=ls.get(LEGACY_KEY);if(!raw)return null;ls.del(LEGACY_KEY);try{return JSON.parse(raw);}catch(e){return null;}};

// ---- Firebase (optional) ----
let db=null, activeKey='', unsubscribe=null, docRef=null, onRemote=null, onStatus=()=>{};
let lastRemoteUpdatedAt='', pendingLocalUpdatedAt='', getLocal=()=>null;
// Accept a key or a pasted sync/live link, including older nested sharing links.
// Parse only known URL parameters so unrelated URLs cannot become API keys.
store.normalizeApiKey=value=>{
  value=String(value||'').trim();
  for(let depth=0;depth<8&&value;depth++){
    if(/^AIza[A-Za-z0-9_-]{35}$/.test(value))return value;
    try{
      const url=new URL(value);if(!['https:','http:'].includes(url.protocol))return '';
      const fragment=new URLSearchParams(url.hash.slice(1));
      value=(fragment.get('liveKey')||fragment.get('apiKey')||url.searchParams.get('apiKey')||'').trim();
    }catch(e){return '';}
  }
  return '';
};
store.getApiKey=()=>{
  let fromUrl='';try{fromUrl=new URLSearchParams(location.search).get('apiKey')||'';}catch(e){}
  const saved=ls.get(FIREBASE_API_KEY_KEY)||'',key=store.normalizeApiKey(fromUrl)||store.normalizeApiKey(saved);
  if(key&&key!==saved)ls.set(FIREBASE_API_KEY_KEY,key);
  return key;
};
store.setApiKey=value=>{
  if(!String(value||'').trim()){ls.del(FIREBASE_API_KEY_KEY);return true;}
  const key=store.normalizeApiKey(value);if(!key)return false;
  ls.set(FIREBASE_API_KEY_KEY,key);return true;
};
store.syncing=()=>!!docRef;
store.shareLink=()=>{const key=store.getApiKey();if(!key)return '';const u=new URL(location.href);u.search='';u.hash='';u.searchParams.set('apiKey',key);return u.toString();};
// The SDK is only downloaded once sync is on, so the page starts instantly offline or on slow networks.
const SDK=['https://www.gstatic.com/firebasejs/9.23.0/firebase-app-compat.js','https://www.gstatic.com/firebasejs/9.23.0/firebase-firestore-compat.js'];
let sdkLoading=null;
function loadSdk(){
  if(root.firebase&&root.firebase.firestore)return Promise.resolve();
  if(!sdkLoading)sdkLoading=SDK.reduce((p,src)=>p.then(()=>new Promise((ok,fail)=>{const s=document.createElement('script');s.src=src;s.onload=ok;s.onerror=()=>fail(Error('firebase-sdk-unavailable'));document.head.append(s);})),Promise.resolve()).catch(e=>{sdkLoading=null;throw e;});
  return sdkLoading;
}
async function ensureFirebase(apiKey){
  if(!apiKey)throw Error('missing-firebase-api-key');
  apiKey=store.normalizeApiKey(apiKey);
  if(!apiKey)throw Error('invalid-firebase-api-key');
  await loadSdk();
  if(!root.firebase)throw Error('firebase-sdk-unavailable');
  if(activeKey&&activeKey!==apiKey){store.stop();if(firebase.apps.length&&firebase.app().delete)await firebase.app().delete();}
  if(!firebase.apps.some(app=>app.name==='[DEFAULT]'))firebase.initializeApp({...FIREBASE_CONFIG,apiKey});
  activeKey=apiKey;db=firebase.firestore();
}
store.stop=()=>{if(unsubscribe){unsubscribe();unsubscribe=null;}docRef=null;lastRemoteUpdatedAt='';pendingLocalUpdatedAt='';};
// Start syncing one student's document. Same last-write-wins rule as the todo page, by updatedAt.
store.start=async(name,handlers)=>{
  store.stop();onRemote=handlers.onRemote;onStatus=handlers.onStatus||onStatus;getLocal=handlers.getLocal;
  const apiKey=store.getApiKey();if(!apiKey){onStatus('local');return false;}
  try{await ensureFirebase(apiKey);}catch(e){onStatus('error',e);return false;}
  const ref=db.collection(FIREBASE_COLLECTION).doc(store.idFor(name));docRef=ref;onStatus('connecting');
  unsubscribe=ref.onSnapshot(snapshot=>{
    if(docRef!==ref)return;
    if(snapshot.metadata&&snapshot.metadata.hasPendingWrites)return;
    const data=snapshot.exists?snapshot.data():null, local=getLocal(), localAt=local&&local.updatedAt||'';
    const remoteAt=data&&data.updatedAt||'';
    if(lastRemoteUpdatedAt&&remoteAt&&remoteAt<lastRemoteUpdatedAt)return;
    if(pendingLocalUpdatedAt&&remoteAt&&remoteAt<pendingLocalUpdatedAt)return;
    if(localAt&&(!remoteAt||localAt>remoteAt)){pendingLocalUpdatedAt=localAt;ref.set(local).then(()=>{lastRemoteUpdatedAt=localAt;onStatus('synced');}).catch(e=>onStatus('error',e));return;}
    if(!data){onStatus('synced');return;}
    lastRemoteUpdatedAt=remoteAt;
    if(remoteAt!==localAt)onRemote(data);
    onStatus('synced');
  },error=>{if(docRef===ref){onStatus('error',error);store.stop();}});
  return true;
};
store.push=async payload=>{
  if(!docRef)return false;const ref=docRef;pendingLocalUpdatedAt=payload.updatedAt;
  try{await ref.set(payload);if(docRef===ref)lastRemoteUpdatedAt=payload.updatedAt;onStatus('synced');return true;}catch(e){onStatus('error',e);return false;}
};
// Live sessions use separate, random documents and never include student state.
store.liveRef=async(id,key)=>{
  if(!root.LivePractice.validId(id))throw Error('invalid-live-session');
  await ensureFirebase(key||store.getApiKey());
  return db.collection(FIREBASE_COLLECTION).doc('live-'+id);
};
// The monitor uses an independent read-only connection.
store.watchActivity=(name,handlers)=>root.ActivityMonitor.watch(name,store.getApiKey(),handlers);
root.StudentStore=store;
})(window);
