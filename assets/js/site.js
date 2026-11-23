/* Shared site behaviour: mobile menu, auto-playing screen playlists, flip-book init, sheet stack. No dependencies. */
(function(){
  // mobile menu
  var nav=document.querySelector('.nav'), mb=document.querySelector('.menu-btn');
  if(nav&&mb){mb.addEventListener('click',function(){var o=nav.classList.toggle('open');mb.setAttribute('aria-expanded',o?'true':'false');mb.querySelector('span').textContent=o?'Close':'Menu';});}

  // playlists: <div class="scr" data-interval="3200"><div class="scr-in"><img class="on">…</div> .scr-n  .scr-prog i</div>
  var reduce=window.matchMedia&&matchMedia('(prefers-reduced-motion: reduce)').matches;
  document.querySelectorAll('.scr').forEach(function(s,k){
    var im=s.querySelectorAll('.scr-in img'), n=s.querySelector('.scr-n'), p=s.querySelector('.scr-prog i'), i=0, T=+(s.dataset.interval||3200), timer=null, paused=false;
    if(im.length<2) return;
    function pad(x){return (x<10?'0':'')+x}
    function bar(){if(!p)return;p.style.transition='none';p.style.width='0';void p.offsetWidth;p.style.transition='width '+T+'ms linear';p.style.width='100%'}
    function show(j){im[i].classList.remove('on');i=(j+im.length)%im.length;im[i].classList.add('on');if(n)n.textContent=pad(i+1)+' / '+pad(im.length);bar()}
    function start(){if(reduce||timer)return;bar();timer=setInterval(function(){if(!paused)show(i+1)},T)}
    s.addEventListener('mouseenter',function(){paused=true;if(p){p.style.transition='none';}});
    s.addEventListener('mouseleave',function(){paused=false;bar()});
    var prev=s.querySelector('.scr-prev'), next=s.querySelector('.scr-next');
    if(prev)prev.addEventListener('click',function(e){e.preventDefault();show(i-1)}); if(next)next.addEventListener('click',function(e){e.preventDefault();show(i+1)});
    setTimeout(start,k*600);
  });

  // flip-book (Nomad): needs assets/js/page-flip.browser.js loaded first
  var el=document.getElementById('fb-book');
  if(el&&window.St){
    var PW=+el.getAttribute('data-w')||1100, PH=+el.getAttribute('data-h')||850;   // page size; Pacific Center = portrait 850x1100
    var pf=new St.PageFlip(el,{width:PW,height:PH,size:'stretch',minWidth:260,maxWidth:PW,minHeight:200,maxHeight:PH,
      showCover:true,usePortrait:true,maxShadowOpacity:0.45,flippingTime:900,mobileScrollSupport:false,drawShadow:true,autoSize:true});
    pf.loadFromHTML(el.querySelectorAll('.fb-page'));
    window.pageFlip=pf;
    var PG=el.getAttribute('data-total')?[].map.call(el.querySelectorAll('.fb-page'),function(x){return x.getAttribute('data-pg')}):null, PT=el.getAttribute('data-total');
    var total=pf.getPageCount(), c=document.getElementById('fb-counter'), pv=document.getElementById('fb-prev'), nx=document.getElementById('fb-next');
    function pad2(x){return (x<10?'0':'')+x}
    function upd(){
      var i=pf.getCurrentPageIndex(), o=pf.getOrientation(), t;
      if(i===0) t='Cover'; else if(i===total-1) t='End';
      else if(PG){var a=(o==='landscape')?((i%2===0)?i-1:i):i;   // printed page numbers from data-pg (Pacific Center)
        t=(o==='landscape'&&a+1<total-1)?'Pages '+PG[a]+'–'+PG[a+1]+' / '+PT:'Page '+PG[a]+' / '+PT;}
      else if(o==='landscape'){var a=(i%2===0)?i-1:i; t='Pages '+pad2(a)+'–'+pad2(Math.min(a+1,total-2))+' / '+pad2(total-2);}
      else t='Page '+pad2(i)+' / '+pad2(total-2);
      el.classList.toggle('portrait',o==='portrait');
      c.textContent=t; pv.disabled=(i===0); nx.disabled=(i>=total-1);
    }
    pf.on('flip',upd); pf.on('changeOrientation',upd); pf.on('init',upd); upd();
    pv.onclick=function(){pf.flipPrev()}; nx.onclick=function(){pf.flipNext()};
    function inView(){var r=el.getBoundingClientRect();return r.bottom>0&&r.top<innerHeight}
    document.addEventListener('keydown',function(e){var t=e.target&&e.target.tagName;if(t==='INPUT'||t==='TEXTAREA'||!inView())return;
      if(e.key==='ArrowRight'){pf.flipNext();e.preventDefault()} if(e.key==='ArrowLeft'){pf.flipPrev();e.preventDefault()}});
  }

  // sheet stack (flyers): <div class="ss"><figure class="ss-sheet">… + .ss-prev/.ss-next/.ss-counter inside the same .ss-stage
  document.querySelectorAll('.ss-stage').forEach(function(st){
    var box=st.querySelector('.ss'), sh=[].slice.call(box.querySelectorAll('.ss-sheet')), N=sh.length, order=sh.map(function(_,i){return i}), busy=false;
    var cnt=st.querySelector('.ss-counter'), pv=st.querySelector('.ss-prev'), nx=st.querySelector('.ss-next'), T=reduce?220:720;
    function pad(x){return (x<10?'0':'')+x}
    function paint(){order.forEach(function(k,pos){sh[k].style.zIndex=N-pos;sh[k].classList.toggle('top',pos===0);sh[k].setAttribute('aria-hidden',pos===0?'false':'true')});
      if(cnt)cnt.textContent='Sheet '+pad(order[0]+1)+' / '+pad(N)}
    function next(dir){if(busy||N<2)return;busy=true;var t=sh[order[0]];t.classList.remove('drag');t.style.transform='';
      t.classList.add(dir<0?'out-l':'out');
      setTimeout(function(){order.push(order.shift());paint();t.classList.remove('out','out-l');setTimeout(function(){busy=false},T*.6)},T*.75)}
    function prev(){if(busy||N<2)return;busy=true;var k=order.pop(),t=sh[k];t.classList.add('now','out-l');order.unshift(k);paint();void t.offsetWidth;
      t.classList.remove('now');setTimeout(function(){t.classList.remove('out-l');setTimeout(function(){busy=false},T)},20)}
    pv.addEventListener('click',prev); nx.addEventListener('click',function(){next(1)});
    // drag / swipe the top sheet; a plain click advances
    var x0=null,y0=0,dx=0,moved=false,cur=null;
    box.addEventListener('pointerdown',function(e){if(busy)return;cur=sh[order[0]];x0=e.clientX;y0=e.clientY;dx=0;moved=false;cur.classList.add('drag');box.setPointerCapture&&box.setPointerCapture(e.pointerId)});
    box.addEventListener('pointermove',function(e){if(x0===null)return;dx=e.clientX-x0;var dy=e.clientY-y0;if(Math.abs(dx)>6)moved=true;
      if(moved)cur.style.transform='translate('+dx+'px,'+dy*.2+'px) rotate('+dx/40+'deg)'});
    function end(){if(x0===null)return;var w=box.clientWidth;x0=null;
      if(!moved){cur.classList.remove('drag');cur.style.transform='';next(1);return}
      if(Math.abs(dx)>w*.18){if(dx>0)next(1);else next(-1)}else{cur.classList.remove('drag');cur.style.transform=''}}
    box.addEventListener('pointerup',end); box.addEventListener('pointercancel',end);
    function inView(){var r=box.getBoundingClientRect();return r.bottom>0&&r.top<innerHeight}
    document.addEventListener('keydown',function(e){var g=e.target&&e.target.tagName;if(g==='INPUT'||g==='TEXTAREA'||!inView()||document.getElementById('fb-book'))return;
      if(e.key==='ArrowRight'){next(1);e.preventDefault()} if(e.key==='ArrowLeft'){prev();e.preventDefault()}});
    window.sheetStack=window.sheetStack||[]; window.sheetStack.push({next:next,prev:prev,order:order});
    paint();
  });

  // iPad viewer (digital brochures): .tab-stage > .tab-screen > .tab-track > .tab-page; swipe/drag, edge click, arrows, ← → keys
  document.querySelectorAll('.tab-stage').forEach(function(st){
    var scr=st.querySelector('.tab-screen'), tr=st.querySelector('.tab-track'), pg=[].slice.call(st.querySelectorAll('.tab-page')), N=pg.length, i=0;
    var cnt=st.querySelector('.tab-counter'), pv=st.querySelector('.tab-prev'), nx=st.querySelector('.tab-next'), dots=[].slice.call(st.querySelectorAll('.tab-dots i'));
    if(reduce) scr.classList.add('fade');
    function pad(x){return (x<10?'0':'')+x}
    function load(k){var im=pg[k]&&pg[k].querySelector('img[data-src]'); if(im){im.src=im.getAttribute('data-src');im.removeAttribute('data-src')}}
    function go(k,instant){
      i=Math.max(0,Math.min(N-1,k));
      if(instant) tr.style.transition='none';
      tr.style.transform='translate3d('+(-100*i)+'%,0,0)';
      if(instant){void tr.offsetWidth; tr.style.transition=''}
      pg.forEach(function(p,j){p.classList.toggle('cur',j===i); if(j===i)p.removeAttribute('aria-hidden'); else p.setAttribute('aria-hidden','true')});
      dots.forEach(function(d,j){d.classList.toggle('on',j===i)});
      cnt.textContent='Page '+pad(i+1)+' / '+pad(N); pv.disabled=(i===0); nx.disabled=(i===N-1);
      load(i);load(i+1);load(i-1);
    }
    pv.addEventListener('click',function(){go(i-1)}); nx.addEventListener('click',function(){go(i+1)});
    // drag / swipe with the finger; a plain click on the left or right part of the screen turns the page
    var x0=null,y0=0,dx=0,moved=false,t0=0,W=1,horiz=null;
    scr.addEventListener('pointerdown',function(e){if(e.button>0)return;x0=e.clientX;y0=e.clientY;dx=0;moved=false;horiz=null;t0=Date.now();W=scr.clientWidth;
      if(e.pointerType==='mouse'){scr.setPointerCapture&&scr.setPointerCapture(e.pointerId)}});
    scr.addEventListener('pointermove',function(e){if(x0===null)return;dx=e.clientX-x0;var dy=e.clientY-y0;
      if(horiz===null&&(Math.abs(dx)>6||Math.abs(dy)>6)){horiz=Math.abs(dx)>Math.abs(dy); if(horiz){scr.setPointerCapture&&scr.setPointerCapture(e.pointerId)}}
      if(!horiz)return; moved=true; if(reduce)return; scr.classList.add('drag');
      var edge=(i===0&&dx>0)||(i===N-1&&dx<0), d=edge?dx/3:dx;   // rubber band at the ends
      tr.style.transform='translate3d(calc('+(-100*i)+'% + '+d+'px),0,0)'});
    function end(e){if(x0===null)return;var r=scr.getBoundingClientRect(),cx=(e&&e.clientX!=null?e.clientX:x0)-r.left;x0=null;scr.classList.remove('drag');
      if(!moved){if(horiz===null&&e&&e.type==='pointerup'){go(cx>r.width*0.5?i+1:i-1)}return}
      var v=Math.abs(dx)/Math.max(1,Date.now()-t0);
      if(dx<-W*0.16||(dx<-24&&v>0.45))go(i+1); else if(dx>W*0.16||(dx>24&&v>0.45))go(i-1); else go(i)}
    scr.addEventListener('dragstart',function(e){e.preventDefault()});   // no native image drag (it cancels the pointer stream)
    scr.addEventListener('pointerup',end); scr.addEventListener('pointercancel',function(){x0=null;scr.classList.remove('drag');go(i)});
    function inView(){var r=scr.getBoundingClientRect();return r.bottom>60&&r.top<innerHeight-60}
    document.addEventListener('keydown',function(e){var g=e.target&&e.target.tagName;if(g==='INPUT'||g==='TEXTAREA'||!inView())return;
      if(e.key==='ArrowRight'){go(i+1);e.preventDefault()} if(e.key==='ArrowLeft'){go(i-1);e.preventDefault()}});
    window.addEventListener('resize',function(){go(i,true)});
    // preload the next pages once the viewer comes close to the viewport
    if('IntersectionObserver' in window){var io=new IntersectionObserver(function(es){if(es[0].isIntersecting){load(1);load(2);io.disconnect()}},{rootMargin:'600px'});io.observe(scr)}
    window.tabViewer=window.tabViewer||[]; window.tabViewer.push({go:go,get:function(){return i}});
    go(0,true);
  });
})();
