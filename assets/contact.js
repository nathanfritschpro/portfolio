/* Contact : formulaire de devis en 4 étapes */
(function(){
  const form=document.getElementById('qf');
  if(!form) return;
  const steps=[...form.querySelectorAll('.fs')];
  const bar=document.getElementById('pBar');
  const txt=document.getElementById('pTxt');
  const done=document.getElementById('done');
  const recap=document.getElementById('recap');
  const EMAIL='nathan.fritsch.pro@gmail.com';
  let cur=0;

  // Pré-sélection depuis une page service (?type=immobilier)
  const pre=new URLSearchParams(location.search).get('type');
  if(pre){ const r=form.querySelector(`input[data-k="${pre}"]`); if(r) r.checked=true; }

  const val=n=>{ const el=form.elements[n]; if(!el) return ''; if(el instanceof RadioNodeList) return el.value; return (el.value||'').trim(); };

  function check(i){
    const err=steps[i].querySelector('.err');
    let msg='';
    if(i===0&&!val('type_projet')) msg='Choisissez le type de projet pour continuer.';
    if(i===1&&!val('besoin')) msg='Indiquez si vous souhaitez de la photo, de la vidéo ou les deux.';
    if(i===2&&val('message').length<10) msg='Décrivez votre projet en quelques mots.';
    if(i===3){
      if(!val('nom')) msg='Indiquez votre nom.';
      else if(!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(val('email'))) msg='Indiquez une adresse email valide.';
    }
    err.textContent=msg;
    return !msg;
  }

  function show(i){
    steps[cur].classList.remove('on');
    cur=i;
    steps[cur].classList.add('on');
    bar.style.width=((cur+1)/steps.length*100)+'%';
    txt.textContent=`${cur+1} / ${steps.length}`;
    if(cur===3){
      const esc=s=>s.replace(/[&<>"]/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]));
      const bits=[val('besoin'),val('date'),val('lieu')].filter(Boolean).map(esc).join(' · ');
      recap.innerHTML=`<b>${esc(val('type_projet'))}</b> · ${bits}${val('budget')?'<br>Budget : '+esc(val('budget')):''}`;
    }
    const top=form.closest('.ct-r').getBoundingClientRect().top+scrollY-20;
    if(scrollY>top) (window.__lenis?window.__lenis.scrollTo(top):scrollTo({top,behavior:'smooth'}));
    const f=steps[cur].querySelector('input:not([type=hidden]),textarea');
    if(f&&cur>0) setTimeout(()=>f.focus({preventScroll:true}),350);
  }

  form.addEventListener('click',e=>{
    if(e.target.closest('.nx')){ if(check(cur)) show(cur+1); }
    if(e.target.closest('.back')) show(cur-1);
  });
  // Avancer automatiquement après le choix du type de projet
  form.querySelectorAll('input[name="type_projet"]').forEach(r=>r.addEventListener('change',()=>{ steps[0].querySelector('.err').textContent=''; setTimeout(()=>{ if(cur===0) show(1); },280); }));
  form.addEventListener('keydown',e=>{
    if(e.key==='Enter'&&e.target.tagName==='INPUT'&&cur<steps.length-1){ e.preventDefault(); if(check(cur)) show(cur+1); }
  });

  form.addEventListener('submit',async e=>{
    e.preventDefault();
    if(!check(3)) return;
    document.getElementById('subj').value=`Demande de devis · ${val('type_projet')} · ${val('nom')}`;
    const btn=document.getElementById('sendBtn');
    const err=steps[3].querySelector('.err');

    // Tant que l'ID Formspree n'est pas configuré : ouverture d'un email prérempli
    if(form.action.includes('VOTRE_ID')){
      const body=[...new FormData(form)].filter(([k,v])=>v&&!k.startsWith('_')).map(([k,v])=>`${k} : ${v}`).join('\n');
      location.href=`mailto:${EMAIL}?subject=${encodeURIComponent(document.getElementById('subj').value)}&body=${encodeURIComponent(body)}`;
      return;
    }
    btn.disabled=true; btn.style.opacity=.6;
    try{
      const r=await fetch(form.action,{method:'POST',body:new FormData(form),headers:{Accept:'application/json'}});
      if(!r.ok) throw 0;
      form.style.display='none';
      document.querySelector('.prog').style.display='none';
      document.querySelector('.ct-top').style.display='none';
      done.classList.add('on');
    }catch(_){
      err.innerHTML=`L'envoi n'a pas fonctionné. Écrivez-moi directement à <a href="mailto:${EMAIL}">${EMAIL}</a>.`;
      btn.disabled=false; btn.style.opacity='';
    }
  });
})();
