/* NATHAN FRITSCH · V2 shared interactions */
(function(){
  const root=document.documentElement;
  const body=document.body;
  const reduce=matchMedia('(prefers-reduced-motion: reduce)').matches;
  const fine=matchMedia('(hover:hover) and (pointer:fine)').matches;
  const lite=body.hasAttribute('data-lite'); // portfolio : garde son curseur et ses transitions

  /* ── Smooth scroll (Lenis if available) ── */
  let lenis=null;
  if(window.Lenis&&!reduce&&!lite){
    lenis=new Lenis({duration:1.15,easing:t=>Math.min(1,1.001-Math.pow(2,-10*t)),smoothWheel:true});
    (function raf(t){lenis.raf(t);requestAnimationFrame(raf);})(0);
    window.__lenis=lenis;
  }
  document.querySelectorAll('a[href^="#"]').forEach(a=>a.addEventListener('click',e=>{
    const id=a.getAttribute('href');
    if(id.length<2) return;
    const el=document.querySelector(id);
    if(!el) return;
    e.preventDefault();
    closeMenu();
    lenis?lenis.scrollTo(el,{offset:-40}):el.scrollIntoView({behavior:'smooth'});
  }));

  /* ── Intro curtain, first visit of the session only ── */
  const intro=document.querySelector('.intro');
  function startPage(){ body.classList.add('ready'); }
  if(intro){
    let seen=false;
    try{seen=sessionStorage.getItem('nf-intro')==='1';}catch(e){}
    if(seen||reduce){ intro.remove(); startPage(); }
    else{
      try{sessionStorage.setItem('nf-intro','1');}catch(e){}
      lenis&&lenis.stop();
      setTimeout(()=>{ intro.classList.add('out'); startPage(); lenis&&lenis.start(); },1650);
      setTimeout(()=>intro.remove(),2900);
    }
  } else startPage();

  /* ── Page transition ── */
  const pt=document.createElement('div');
  if(lite) pt.style.display='none';
  pt.className='pt';
  body.appendChild(pt);
  let arrived=false;
  try{arrived=sessionStorage.getItem('nf-pt')==='1';sessionStorage.removeItem('nf-pt');}catch(e){}
  if(arrived&&!reduce){
    pt.classList.add('leave');
    requestAnimationFrame(()=>requestAnimationFrame(()=>pt.classList.add('done')));
    setTimeout(()=>pt.className='pt',950);
  }
  document.addEventListener('click',e=>{
    const a=e.target.closest('a');
    if(!a||reduce||lite) return;
    const href=a.getAttribute('href');
    if(!href||a.target==='_blank'||e.metaKey||e.ctrlKey||e.shiftKey||href.startsWith('#')||href.startsWith('mailto:')||href.startsWith('tel:')||/^https?:/.test(href)) return;
    if(href.split('#')[0]===location.pathname.split('/').pop()&&href.includes('#')) return;
    e.preventDefault();
    try{sessionStorage.setItem('nf-pt','1');}catch(err){}
    pt.className='pt go';
    setTimeout(()=>{location.href=href;},650);
  });
  addEventListener('pageshow',e=>{ if(e.persisted) pt.className='pt'; });

  /* ── Header: solid after scroll, hides on scroll down ── */
  const hd=document.querySelector('.hd');
  const mcta=document.querySelector('.mcta');
  let lastY=0;
  function onScroll(){
    const y=scrollY;
    if(hd){
      hd.classList.toggle('solid',y>40);
      if(!body.classList.contains('menu-open')) hd.classList.toggle('hide',y>lastY&&y>500);
    }
    if(mcta) mcta.classList.toggle('show',y>innerHeight*.6&&(innerHeight+y)<document.body.scrollHeight-280);
    lastY=y;
  }
  addEventListener('scroll',onScroll,{passive:true});
  onScroll();

  /* ── Mobile menu ── */
  const burger=document.querySelector('.hd-burger');
  function closeMenu(){ body.classList.remove('menu-open'); document.querySelectorAll('.mm-g.open').forEach(x=>{x.classList.remove('open');x.querySelector('.mm-t').setAttribute('aria-expanded','false');}); burger&&burger.setAttribute('aria-expanded','false'); lenis&&lenis.start(); }
  burger&&burger.addEventListener('click',()=>{
    const on=!body.classList.contains('menu-open');
    body.classList.toggle('menu-open',on);
    burger.setAttribute('aria-expanded',on);
    hd.classList.remove('hide');
    on?(lenis&&lenis.stop()):(lenis&&lenis.start());
  });
  addEventListener('keydown',e=>{ if(e.key==='Escape') closeMenu(); });
  // Menu mobile : sous-menus repliés, un seul ouvert à la fois
  document.querySelectorAll('.mm-g button.mm-t').forEach(b=>b.addEventListener('click',()=>{
    const g=b.closest('.mm-g'), open=!g.classList.contains('open');
    document.querySelectorAll('.mm-g.open').forEach(x=>{x.classList.remove('open');x.querySelector('.mm-t').setAttribute('aria-expanded','false');});
    g.classList.toggle('open',open); b.setAttribute('aria-expanded',open);
  }));

  /* ── Split headings into words ── */
  document.querySelectorAll('.split').forEach(el=>{
    let i=0;
    const walk=node=>{
      [...node.childNodes].forEach(n=>{
        if(n.nodeType===3){
          const frag=document.createDocumentFragment();
          n.textContent.split(/(\s+)/).forEach(part=>{
            if(!part) return;
            if(/^\s+$/.test(part)){ frag.appendChild(document.createTextNode(' ')); return; }
            const w=document.createElement('span'); w.className='w';
            const s=document.createElement('span'); s.textContent=part; s.style.setProperty('--i',i++);
            w.appendChild(s); frag.appendChild(w);
          });
          n.replaceWith(frag);
        } else if(n.nodeType===1&&n.tagName!=='BR') walk(n);
      });
    };
    walk(el);
  });

  /* ── Reveal on view ── */
  const io=new IntersectionObserver(es=>es.forEach(x=>{ if(x.isIntersecting){ x.target.classList.add('in'); io.unobserve(x.target);} }),{threshold:.14,rootMargin:'0px 0px -6% 0px'});
  function arm(){
    const els=[...document.querySelectorAll('[data-rv],.split,.imgrv')];
    els.forEach(el=>io.observe(el));
    // filet de sécurité : ce qui est déjà à l'écran apparaît tout de suite
    requestAnimationFrame(()=>els.forEach(el=>{ const r=el.getBoundingClientRect(); if(r.top<innerHeight*.94&&r.bottom>0) el.classList.add('in'); }));
  }
  if(body.classList.contains('ready')) arm(); else { const t=setInterval(()=>{ if(body.classList.contains('ready')){clearInterval(t);arm();} },50); }
  window.__armHold=el=>el.querySelectorAll('[data-rv],.split,.imgrv').forEach(n=>n.classList.add('in'));

  /* ── Parallax ([data-px]="speed") ── */
  const px=[...document.querySelectorAll('[data-px]')];
  if(px.length&&!reduce){
    const tick=()=>{
      px.forEach(el=>{
        const r=el.parentElement.getBoundingClientRect();
        if(r.bottom<-200||r.top>innerHeight+200) return;
        const s=parseFloat(el.dataset.px)||.15;
        el.style.transform=`translate3d(0,${((r.top+r.height/2-innerHeight/2)*-s).toFixed(1)}px,0)`;
      });
      requestAnimationFrame(tick);
    };
    requestAnimationFrame(tick);
  }

  /* ── Magnetic buttons ── */
  if(fine) document.querySelectorAll('.btn:not(.no-mag)').forEach(b=>{
    b.addEventListener('mousemove',e=>{
      const r=b.getBoundingClientRect();
      b.style.transform=`translate(${(e.clientX-r.left-r.width/2)*.18}px,${(e.clientY-r.top-r.height/2)*.28}px)`;
    });
    b.addEventListener('mouseleave',()=>b.style.transform='');
  });

  /* ── Custom cursor ── */
  if(fine&&!reduce&&!lite){
    const cx=document.createElement('div');
    cx.id='cx';
    cx.innerHTML='<div class="c-ring"><span>Voir</span></div><div class="c-dot"></div>';
    body.appendChild(cx);
    const ring=cx.querySelector('.c-ring'),dot=cx.querySelector('.c-dot'),lbl=ring.querySelector('span');
    let mx=-100,my=-100,rx=-100,ry=-100;
    addEventListener('mousemove',e=>{mx=e.clientX;my=e.clientY;dot.style.transform=`translate(${mx}px,${my}px) translate(-50%,-50%)`;},{passive:true});
    (function loop(){ rx+=(mx-rx)*.16; ry+=(my-ry)*.16; ring.style.transform=`translate(${rx}px,${ry}px) translate(-50%,-50%)`; requestAnimationFrame(loop); })();
    document.addEventListener('mouseover',e=>{
      const v=e.target.closest('[data-cursor]');
      const l=e.target.closest('a,button,summary,label,input,select,textarea');
      body.classList.toggle('c-view',!!v);
      body.classList.toggle('c-link',!v&&!!l);
      if(v) lbl.textContent=v.dataset.cursor||'Voir';
      body.classList.toggle('c-dark',!!e.target.closest('.on-dark,.cta-end,.hero'));
    });
  }

  /* ── Year ── */
  document.querySelectorAll('[data-year]').forEach(el=>el.textContent=new Date().getFullYear());
})();
