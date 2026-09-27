/* Accueil : manifeste, image expansive, réalisations horizontales */
(function(){
  const reduce=matchMedia('(prefers-reduced-motion: reduce)').matches;

  /* ── Manifeste : les mots s'allument au fil du scroll ── */
  const mani=document.getElementById('mani');
  let words=[];
  if(mani){
    const wrapWords=node=>{
      [...node.childNodes].forEach(n=>{
        if(n.nodeType===3){
          const frag=document.createDocumentFragment();
          n.textContent.split(/(\s+)/).forEach(p=>{
            if(!p) return;
            if(/^\s+$/.test(p)){frag.appendChild(document.createTextNode(' '));return;}
            const s=document.createElement('span');s.className='mw';s.textContent=p;frag.appendChild(s);
          });
          n.replaceWith(frag);
        } else if(n.nodeType===1) wrapWords(n);
      });
    };
    wrapWords(mani);
    words=[...mani.querySelectorAll('.mw')];
    if(reduce) words.forEach(w=>w.classList.add('lit'));
  }
  function maniTick(){
    if(!words.length||reduce) return;
    const r=mani.getBoundingClientRect();
    const p=Math.min(1,Math.max(0,(innerHeight*.85-r.top)/(r.height+innerHeight*.35)));
    const n=Math.round(p*words.length*1.15);
    words.forEach((w,i)=>w.classList.toggle('lit',i<n));
  }

  /* ── Image expansive (Photo & Vidéo) ── */
  const se=document.getElementById('se-hero');
  const frame=document.getElementById('seFrame');
  const title=document.getElementById('seTitle');
  const sub=se&&se.querySelector('.se-sub');
  const cue=document.getElementById('seCue');
  const small=()=>matchMedia('(max-width:768px)').matches;
  function seTick(){
    if(!se) return;
    const run=se.offsetHeight-innerHeight;
    const y=Math.min(run,Math.max(0,-se.getBoundingClientRect().top));
    const e=run>0?y/run:0;
    const k=1-Math.pow(1-e,2);
    const w0=small()?86:46,h0=small()?54:64;
    frame.style.width=(w0+(100-w0)*k).toFixed(2)+'vw';
    frame.style.height=(h0+(100-h0)*k).toFixed(2)+'vh';
    frame.style.borderRadius=(22*(1-k)).toFixed(1)+'px';
    const fw=frame.getBoundingClientRect().width;
    const cur=parseFloat(getComputedStyle(title).fontSize)||64;
    const per=(title.offsetWidth||1)/cur;
    title.style.fontSize=Math.max(30,Math.min(220,(fw*.6)/per)).toFixed(1)+'px';
    const sp=Math.max(0,Math.min(1,(e-.45)/.45));
    sub.style.opacity=sp.toFixed(2);
    sub.style.transform=`translateY(${(14*(1-sp)).toFixed(1)}px)`;
    if(cue) cue.style.opacity=Math.max(0,1-e*3).toFixed(2);
  }

  /* ── Réalisations : défilement horizontal piloté par le scroll ── */
  const work=document.querySelector('.work');
  const track=document.getElementById('wTrack');
  const prog=document.getElementById('wProg');
  const cnt=document.getElementById('wcN');
  const desktop=()=>matchMedia('(min-width:1081px)').matches;
  let dist=0;
  function sizeWork(){
    if(!work) return;
    if(!desktop()){work.style.height='';track.style.transform='';return;}
    dist=Math.max(0,track.scrollWidth-innerWidth);
    work.style.height=(innerHeight+dist)+'px';
  }
  function workTick(){
    if(!work||!desktop()) return;
    const r=work.getBoundingClientRect();
    const p=dist>0?Math.min(1,Math.max(0,-r.top/dist)):0;
    track.style.transform=`translate3d(${(-p*dist).toFixed(1)}px,0,0)`;
    prog.style.transform=`scaleX(${p.toFixed(3)})`;
    const cards=track.querySelectorAll('.case');
    let n=1;
    cards.forEach((c,i)=>{ if(c.getBoundingClientRect().left<innerWidth*.45) n=i+1; });
    cnt.textContent=String(n).padStart(2,'0');
  }

  function tick(){ maniTick(); seTick(); workTick(); }
  addEventListener('scroll',tick,{passive:true});
  addEventListener('resize',()=>{sizeWork();tick();});
  addEventListener('load',()=>{sizeWork();tick();});
  sizeWork(); tick();
  if(document.fonts&&document.fonts.ready) document.fonts.ready.then(()=>{sizeWork();tick();});
})();
