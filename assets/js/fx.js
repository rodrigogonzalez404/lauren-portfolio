/* Premium effects (t113u/t114u): preloader end, smooth wheel scrolling, headline + image reveals, card cursor label,
   page-fade transitions. Active only when <html> has class "fx" (set in <head>; never with prefers-reduced-motion). */
(function(){
  var d=document.documentElement; if(!d.classList.contains('fx'))return;
  var pre=d.classList.contains('fx-pre'), t0=pre?1150:0;
  if(pre) setTimeout(function(){d.classList.remove('fx-pre');var o=document.querySelector('.fx-pre-o');o&&o.remove()},1700);
  var fine=matchMedia('(hover:hover) and (pointer:fine)').matches;
  var io='IntersectionObserver' in window;
  function watch(els,cb){ if(!io){els.forEach(function(e){e.classList.add('in')});return}
    var ob=new IntersectionObserver(function(es){es.forEach(function(x){if(x.isIntersecting){ob.unobserve(x.target);cb(x.target)}})},{rootMargin:'0px 0px -8% 0px',threshold:.01});
    els.forEach(function(e){ob.observe(e)}); }
  function later(f){ var w=t0-performance.now(); w>0?setTimeout(f,w):f(); }
  /* headlines: split text into words, delay by line */
  var hs=[].slice.call(document.querySelectorAll('main h1, main h2.xl, main h2.l, main .cn-title'));
  hs.forEach(function(h){
    var walk=document.createTreeWalker(h,NodeFilter.SHOW_TEXT,null),nodes=[],n; while(n=walk.nextNode())nodes.push(n);
    nodes.forEach(function(t){ var parts=t.nodeValue.split(/(\s+)/),f=document.createDocumentFragment();
      parts.forEach(function(p){ if(!p)return; if(/^\s+$/.test(p)){f.appendChild(document.createTextNode(p));return}
        var o=document.createElement('span');o.className='fw';var i=document.createElement('span');i.textContent=p;o.appendChild(i);f.appendChild(o); });
      t.parentNode.replaceChild(f,t); });
    var ws=h.querySelectorAll('.fw'),top=null,line=-1;
    [].forEach.call(ws,function(w){var y=w.offsetTop; if(top===null||Math.abs(y-top)>4){line++;top=y} w.firstChild.style.setProperty('--d',(line*.09)+'s')});
    h.classList.add('fx-h');
  });
  /* images: cards, case hero, gallery pictures (not the page viewers) */
  var im=[].slice.call(document.querySelectorAll('.card .ph, .case-hero, figure.pic'));
  im.forEach(function(e){e.classList.add('fx-i')});
  requestAnimationFrame(function(){ later(function(){ watch(hs,function(e){e.classList.add('in')}); var par=im.map(function(e){var w=e.parentElement;w.__fx=(w.__fx||[]).concat(e);return w}).filter(function(w,i,a){return a.indexOf(w)===i}); watch(par,function(w){w.__fx.forEach(function(e){e.classList.add('in')})});   /* observe the unclipped parent: a fully clipped element never intersects */ }); });
  /* cursor label over project cards */
  if(fine){ var c=document.createElement('div');c.className='fx-cur';c.textContent='View project';c.setAttribute('aria-hidden','true');document.body.appendChild(c);
    var mx=0,my=0,cx=0,cy=0,run=false;
    function tick(){cx+=(mx-cx)*.2;cy+=(my-cy)*.2;c.style.transform='translate('+(cx+14)+'px,'+(cy+14)+'px)'; if(Math.abs(mx-cx)+Math.abs(my-cy)>.3)requestAnimationFrame(tick);else run=false}
    document.addEventListener('pointermove',function(e){mx=e.clientX;my=e.clientY;var on=!!(e.target.closest&&e.target.closest('a.card'));
      if(on&&!c.classList.contains('on')){cx=mx;cy=my} c.classList.toggle('on',on); if(!run){run=true;requestAnimationFrame(tick)}},{passive:true});
    document.addEventListener('pointerleave',function(){c.classList.remove('on')}); }
  /* smooth wheel scrolling with light inertia (wheel only: keyboard, anchors, touch and the viewers stay native) */
  if(fine){ var tgt=scrollY,cur=scrollY,anim=false;
    function max(){return d.scrollHeight-innerHeight}
    function step(){cur+=(tgt-cur)*.14; if(Math.abs(tgt-cur)<.5){cur=tgt;anim=false} scrollTo(0,cur); if(anim)requestAnimationFrame(step)}
    addEventListener('wheel',function(e){ if(e.ctrlKey||e.defaultPrevented||Math.abs(e.deltaX)>Math.abs(e.deltaY))return;
      var t=e.target; if(t.closest&&t.closest('.tab-dev,.tab-screen,#fb-book,.ipad,.laptop,[data-noscroll]'))return;
      for(var p=t;p&&p!==document.body&&p.nodeType===1;p=p.parentNode){var s=getComputedStyle(p).overflowY;if((s==='auto'||s==='scroll')&&p.scrollHeight>p.clientHeight)return}
      e.preventDefault(); if(!anim){tgt=cur=scrollY} var dy=e.deltaY*(e.deltaMode===1?40:e.deltaMode===2?innerHeight:1);
      tgt=Math.max(0,Math.min(max(),tgt+dy)); if(!anim){anim=true;requestAnimationFrame(step)} },{passive:false});
    addEventListener('scroll',function(){if(!anim){tgt=cur=scrollY}},{passive:true}); }
  /* page transitions: quick fade out before internal navigation */
  document.addEventListener('click',function(e){ var a=e.target.closest&&e.target.closest('a[href]'); if(!a||e.defaultPrevented||e.button||e.metaKey||e.ctrlKey||e.shiftKey||e.altKey)return;
    if(a.target==='_blank'||a.hasAttribute('download'))return; var u=new URL(a.href,location.href);
    if(u.origin!==location.origin||!/\.html$|\/$/.test(u.pathname)||(u.pathname===location.pathname&&u.hash))return;
    e.preventDefault(); d.classList.add('fx-out'); setTimeout(function(){location.href=a.href},230); });
  addEventListener('pageshow',function(e){if(e.persisted)d.classList.remove('fx-out')});
})();
