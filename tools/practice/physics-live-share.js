/* Live question navigation. Student history and working are never session data. */
(function(root){
  'use strict';
  const validId=id=>typeof id==='string'&&/^[a-f0-9]{48}$/.test(id);
  function pack(problem){return problem?{q:problem.id,...(problem.generatedData?{generated:problem.generatedData}:{})}:null;}
  function unpack(data,bank){return data&&typeof data.q==='string'?(bank.find(p=>p.id===data.q)||(data.generated?.id===data.q&&root.AdaptivePractice?.problem(data.generated,bank))||null):null;}
  function sessionId(){
    const bytes=new Uint8Array(24);root.crypto.getRandomValues(bytes);
    return Array.from(bytes,b=>b.toString(16).padStart(2,'0')).join('');
  }
  function shareURL(base,id,key){
    if(!validId(id))throw Error('invalid-live-session');
    if(typeof key!=='string'||!/^AIza[A-Za-z0-9_-]{35}$/.test(key))throw Error('invalid-firebase-api-key');
    const u=new URL(base);u.search='';u.hash='';u.searchParams.set('follow',id);
    // Firebase's web configuration stays in the fragment, out of request URLs.
    u.hash=new URLSearchParams({liveKey:key}).toString();return u.toString();
  }
  class Session {
    constructor({openDoc,onStatus=()=>{},onQuestion=()=>{},now=()=>Date.now(),makeId=sessionId}){
      Object.assign(this,{openDoc,onStatus,onQuestion,now,makeId});this.role='idle';this.epoch=0;this.ref=null;this.unsubscribe=null;this.queue=Promise.resolve();this.revision=0;this.signature='';
    }
    record(question,active=true){return {kind:'physicsUni-live',version:1,active,revision:++this.revision,question,updatedAt:new Date(this.now()).toISOString(),expiresAt:this.now()+8*60*60*1000};}
    async startHost(problem){
      if(this.role!=='idle')throw Error('live-session-already-active');
      const epoch=++this.epoch;this.role='starting';this.onStatus('starting');
      const id=this.makeId();if(!validId(id)){this.leave();throw Error('invalid-live-session');}
      try{
        const ref=await this.openDoc(id);
        if(epoch!==this.epoch)return null;
        const question=pack(problem);this.revision=0;
        await ref.set(this.record(question));
        if(epoch!==this.epoch)return null;
        this.id=id;this.ref=ref;this.role='host';this.signature=JSON.stringify(question);this.queue=Promise.resolve();this.onStatus('hosting');return id;
      }catch(error){if(epoch===this.epoch){this.leave();this.onStatus('error',error);}throw error;}
    }
    publish(problem){
      if(this.role!=='host')return Promise.resolve();
      const question=pack(problem),signature=JSON.stringify(question);
      if(signature===this.signature)return this.queue;
      this.signature=signature;
      const ref=this.ref,epoch=this.epoch,data=this.record(question);
      this.onStatus('publishing');
      this.queue=this.queue.catch(()=>{}).then(()=>epoch===this.epoch?ref.set(data):undefined);
      this.queue.then(()=>{if(epoch===this.epoch&&this.role==='host'&&data.revision===this.revision)this.onStatus('hosting');},error=>{
        if(epoch===this.epoch){this.signature='';this.onStatus('publish-error',error);}
      });return this.queue;
    }
    async stopHost(){
      if(this.role!=='host')return;
      this.role='ending';this.onStatus('ending');const epoch=this.epoch,ref=this.ref;
      try{await this.queue.catch(()=>{});await ref.set(this.record(null,false));if(epoch===this.epoch){this.leave();this.onStatus('idle');}}
      catch(error){if(epoch===this.epoch){this.role='host';this.onStatus('stop-error',error);}throw error;}
    }
    async follow(id,key){
      if(!validId(id))throw Error('invalid-live-session');
      this.leave();this.id=id;this.role='follower';const epoch=this.epoch;let revision=-1;this.onStatus('connecting');
      try{
        const ref=await this.openDoc(id,key);if(epoch!==this.epoch)return;
        this.ref=ref;
        this.unsubscribe=ref.onSnapshot({includeMetadataChanges:true},snapshot=>{
          if(epoch!==this.epoch)return;
          if(!snapshot.exists){this.onStatus(snapshot.metadata?.fromCache?'connecting':'unavailable');return;}
          const data=snapshot.data();
          if(data.kind!=='physicsUni-live'||data.version!==1||!Number.isInteger(data.revision)||!Number.isFinite(data.expiresAt)){this.onStatus('invalid');return;}
          if(data.revision<revision)return;
          if(!data.active||data.expiresAt<=this.now()){this.onStatus('ended');return;}
          this.onStatus(snapshot.metadata?.fromCache?'reconnecting':'following');
          if(data.revision>revision){revision=data.revision;this.onQuestion(data.question);}
        },error=>{if(epoch===this.epoch)this.onStatus('error',error);});
      }catch(error){if(epoch===this.epoch)this.onStatus('error',error);throw error;}
    }
    leave(){
      ++this.epoch;if(this.unsubscribe)this.unsubscribe();this.unsubscribe=null;this.ref=null;this.id='';this.role='idle';this.signature='';
    }
  }
  const api={Session,pack,unpack,validId,shareURL};
  if(typeof module!=='undefined')module.exports=api;root.LivePractice=api;
})(typeof window!=='undefined'?window:globalThis);
