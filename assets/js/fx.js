/* Premium effects v2 (t115u): preloader end, headline + image reveals, circle cursor over cards, page fades.
   No scroll hijacking, no scroll listeners. Active only when <html> has class "fx" (never with reduced motion). */
(function(){
  var d=document.documentElement; if(!d.classList.contains('fx'))return;
  var pre=d.classList.contains('fx-pre'), t0=pre?650:0;
  if(pre) setTimeout(function(){d.classList.remove('fx-pre');var o=document.querySelector('.fx-pre-o');o&&o.remove()},1000);
  var io='IntersectionObserver' in window;
  function watch(els,cb){ if(!io){els.forEach(cb);return}
    var ob=new IntersectionObserver(function(es){es.forEach(function(x){if(x.isIntersecting){ob.unobserve(x.target);cb(x.target)}})},{rootMargin:'0px 0px -6% 0px'});
    els.forEach(function(e){ob.observe(e)}); }
  function later(f){ var w=t0-performance.now(); w>0?setTimeout(f,w):f(); }
  /* headlines: split text into words once, delay by line (layout read once, before observing) */
  var hs=[].slice.call(document.querySelectorAll('main h1, main h2.xl, main h2.l, main .cn-title'));
  hs.forEach(function(h){
    var walk=document.createTreeWalker(h,NodeFilter.SHOW_TEXT,null),nodes=[],n; while(n=walk.nextNode())nodes.push(n);
    nodes.forEach(function(t){ var parts=t.nodeValue.split(/(\s+)/),f=document.createDocumentFragment();
      parts.forEach(function(p){ if(!p)return; if(/^\s+$/.test(p)){f.appendChild(document.createTextNode(p));return}
        var o=document.createElement('span');o.className='fw';var i=document.createElement('span');i.textContent=p;o.appendChild(i);f.appendChild(o); });
      t.parentNode.replaceChild(f,t); });
    h.classList.add('fx-h');
  });
  hs.forEach(function(h){ var top=null,line=-1; [].forEach.call(h.querySelectorAll('.fw'),function(w){var y=w.offsetTop; if(top===null||Math.abs(y-top)>4){line++;top=y} w.firstChild.style.transitionDelay=(line*.08)+'s'}); });
  /* images: cards, case hero, gallery pictures (not the page viewers); will-change only while animating */
  var im=[].slice.call(document.querySelectorAll('.card .ph, .case-hero, figure.pic'));
  im.forEach(function(e){e.classList.add('fx-i')});
  function show(e){ e.classList.add('go'); requestAnimationFrame(function(){e.classList.add('in')}); setTimeout(function(){e.classList.remove('go')},1000); }
  later(function(){ watch(hs,function(e){e.classList.add('in')}); watch(im,show); });
  /* circle cursor over project cards (fine pointers only; native pointer stays) */
  if(matchMedia('(hover:hover) and (pointer:fine)').matches){
    var c=document.createElement('div');c.className='fx-cur';c.textContent='View project';c.setAttribute('aria-hidden','true');document.body.appendChild(c);
    var mx=-200,my=-200,cx=-200,cy=-200,s=.2,ts=.2,on=false,raf=0;
    function tick(){ cx+=(mx-cx)*.28;cy+=(my-cy)*.28;s+=(ts-s)*.22;
      c.style.transform='translate3d('+cx+'px,'+cy+'px,0) scale('+s.toFixed(3)+')';
      raf=(Math.abs(mx-cx)+Math.abs(my-cy)>.2||Math.abs(ts-s)>.005)?requestAnimationFrame(tick):0; if(!raf&&!on)c.classList.remove('on'); }
    function kick(){ if(!raf)raf=requestAnimationFrame(tick) }
    document.addEventListener('pointerover',function(e){ var a=e.target.closest&&e.target.closest('a.card'); if(!!a===on)return; on=!!a;
      if(on){ if(ts<.5){cx=mx;cy=my} ts=1;c.classList.add('on') } else ts=.2; kick(); },{passive:true});
    document.addEventListener('pointermove',function(e){mx=e.clientX;my=e.clientY;if(on)kick()},{passive:true});
    document.documentElement.addEventListener('pointerleave',function(){on=false;ts=.2;kick()});
  }
  /* page transitions: quick fade out before internal navigation */
  document.addEventListener('click',function(e){ var a=e.target.closest&&e.target.closest('a[href]'); if(!a||e.defaultPrevented||e.button||e.metaKey||e.ctrlKey||e.shiftKey||e.altKey)return;
    if(a.target==='_blank'||a.hasAttribute('download'))return; var u=new URL(a.href,location.href);
    if(u.origin!==location.origin||!/\.html$|\/$/.test(u.pathname)||(u.pathname===location.pathname&&u.hash))return;
    e.preventDefault(); d.classList.add('fx-out'); setTimeout(function(){location.href=a.href},160); });
  addEventListener('pageshow',function(e){if(e.persisted)d.classList.remove('fx-out')});
})();
