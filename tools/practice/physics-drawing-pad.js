/* Fixed drawing coordinates preserve ink when the page resizes or rotates. */
(function(root){
'use strict';
function pointSegmentDistance2(p,a,b){
  const dx=b.x-a.x,dy=b.y-a.y,length=dx*dx+dy*dy;
  const t=length?Math.max(0,Math.min(1,((p.x-a.x)*dx+(p.y-a.y)*dy)/length)):0;
  return (p.x-a.x-t*dx)**2+(p.y-a.y-t*dy)**2;
}
function segmentDistance2(a,b,c,d){
  const cross=(p,q,r)=>(q.x-p.x)*(r.y-p.y)-(q.y-p.y)*(r.x-p.x);
  const overlaps=Math.max(Math.min(a.x,b.x),Math.min(c.x,d.x))<=Math.min(Math.max(a.x,b.x),Math.max(c.x,d.x)) && Math.max(Math.min(a.y,b.y),Math.min(c.y,d.y))<=Math.min(Math.max(a.y,b.y),Math.max(c.y,d.y));
  if(overlaps&&cross(a,b,c)*cross(a,b,d)<=0&&cross(c,d,a)*cross(c,d,b)<=0)return 0;
  return Math.min(pointSegmentDistance2(a,c,d),pointSegmentDistance2(b,c,d),pointSegmentDistance2(c,a,b),pointSegmentDistance2(d,a,b));
}
class DrawingPad {
  constructor(canvas,onChange){
    this.canvas=canvas;this.ctx=canvas.getContext('2d');this.onChange=onChange;
    this.strokes=[];this.history=[];this.beforeGesture=null;this.active=null;this.tool='pen';this.color='#222223';this.gesture=0;this.enabled=true;this.hasInk=false;this.pencilOnly=false;
    canvas.addEventListener('pointerdown',event=>this.start(event));
    // Pencil-only mode (iPad default): fingers and palms never draw and can scroll the page; stylus touches never scroll.
    const stylusGuard=event=>{if(this.pencilOnly&&[...event.changedTouches].some(t=>t.touchType==='stylus'))event.preventDefault();};
    canvas.addEventListener('touchstart',stylusGuard,{passive:false});canvas.addEventListener('touchmove',stylusGuard,{passive:false});
    canvas.addEventListener('pointermove',event=>this.move(event));
    for(const type of ['pointerup','pointercancel','lostpointercapture'])canvas.addEventListener(type,event=>{if(this.active?.pointerId===event.pointerId)this.finish();});
    this.render();
  }
  point(event){const r=this.canvas.getBoundingClientRect();return {x:Math.max(0,Math.min(this.canvas.width,(event.clientX-r.left)*this.canvas.width/r.width)),y:Math.max(0,Math.min(this.canvas.height,(event.clientY-r.top)*this.canvas.height/r.height))};}
  start(event){
    if(this.pencilOnly&&event.pointerType==='touch'){this.onTouchIgnored?.();return;}
    if(!this.enabled||this.active||event.button!==0||!event.isPrimary)return;
    event.preventDefault();this.canvas.setPointerCapture(event.pointerId);
    this.beforeGesture=this.strokes.slice();
    this.active=this.segment(event,this.point(event),++this.gesture);
    if(this.active.tool==='eraser')this.erase(this.active.points[0],this.active.points[0]);else this.draw(this.active);
    this.onChange();
  }
  segment(event,point,gesture){
    const tool=event.shiftKey?'eraser':this.tool;
    return {pointerId:event.pointerId,gesture,tool,width:tool==='eraser'?40:4,color:this.color,points:[point]};
  }
  move(event){
    if(!this.enabled||this.active?.pointerId!==event.pointerId)return;
    event.preventDefault();
    const tool=event.shiftKey?'eraser':this.tool;
    if(tool!==this.active.tool){
      const prior=this.active;if(prior.tool==='pen')this.strokes.push(prior);
      this.active=this.segment(event,prior.points[prior.points.length-1],prior.gesture);
    }
    const points=event.getCoalescedEvents?.()||[event];
    for(const e of points.length?points:[event]){
      const last=this.active.points[this.active.points.length-1],point=this.point(e);this.active.points.push(point);
      if(this.active.tool==='eraser')this.erase(last,point);else this.draw({...this.active,points:[last,point]});
    }
  }
  erase(from,to){
    // Hit-test the entire swept path, so fast movement cannot jump over a stroke.
    const kept=this.strokes.filter(stroke=>{
      const radius=20+stroke.width/2,points=stroke.points;
      for(let i=0;i<points.length;i++)if(segmentDistance2(from,to,points[i],points[Math.min(i+1,points.length-1)])<=radius*radius)return false;
      return true;
    });
    if(kept.length!==this.strokes.length){this.strokes=kept;this.render();}
  }
  finish(){
    if(!this.active)return;
    const stroke=this.active;this.active=null;if(stroke.tool==='pen')this.strokes.push(stroke);
    const before=this.beforeGesture;this.beforeGesture=null;
    if(before&&(before.length!==this.strokes.length||before.some((s,i)=>s!==this.strokes[i])))this.history.push(before);
    if(this.canvas.hasPointerCapture(stroke.pointerId))this.canvas.releasePointerCapture(stroke.pointerId);
    this.render();this.onChange();
  }
  draw(stroke){
    const ctx=this.ctx;ctx.strokeStyle=ctx.fillStyle=stroke.color;ctx.lineWidth=stroke.width;ctx.lineCap='round';ctx.lineJoin='round';
    const first=stroke.points[0];ctx.beginPath();ctx.arc(first.x,first.y,stroke.width/2,0,Math.PI*2);ctx.fill();
    if(stroke.points.length>1){ctx.beginPath();ctx.moveTo(first.x,first.y);for(const point of stroke.points.slice(1))ctx.lineTo(point.x,point.y);ctx.stroke();}
  }
  render(){this.ctx.fillStyle='#fff';this.ctx.fillRect(0,0,this.canvas.width,this.canvas.height);for(const stroke of this.strokes)this.draw(stroke);this.inspectInk();}
  inspectInk(){const pixels=this.ctx.getImageData(0,0,this.canvas.width,this.canvas.height).data;this.hasInk=false;for(let i=0;i<pixels.length;i+=4){if(pixels[i]<240||pixels[i+1]<240||pixels[i+2]<240){this.hasInk=true;break;}}}
  // Drop the in-progress stroke without saving it (e.g. the first finger of a two-finger tap).
  cancel(){const active=this.active;if(!active)return;this.active=null;if(this.canvas.hasPointerCapture(active.pointerId))this.canvas.releasePointerCapture(active.pointerId);if(this.beforeGesture)this.strokes=this.beforeGesture;this.beforeGesture=null;this.render();this.onChange();}
  undo(){if(!this.enabled)return;this.finish();if(this.history.length)this.strokes=this.history.pop();this.render();this.onChange();}
  clear(){if(!this.enabled)return;this.finish();if(this.strokes.length)this.history.push(this.strokes.slice());this.strokes=[];this.render();this.onChange();}
  reset(){const active=this.active;this.active=null;if(active&&this.canvas.hasPointerCapture(active.pointerId))this.canvas.releasePointerCapture(active.pointerId);this.strokes=[];this.history=[];this.beforeGesture=null;this.tool='pen';this.color='#222223';this.gesture=0;this.enabled=true;this.render();}
  snapshot(){
    this.finish();
    if(!this.strokes.length)return null;
    return {width:this.canvas.width,height:this.canvas.height,strokes:this.strokes.map(stroke=>({tool:'pen',width:stroke.width,color:stroke.color,points:stroke.points.map(p=>({x:Math.round(p.x*10)/10,y:Math.round(p.y*10)/10})).filter((p,i,points)=>!i||p.x!==points[i-1].x||p.y!==points[i-1].y)}))};
  }
}
root.DrawingPad=DrawingPad;
})(window);
