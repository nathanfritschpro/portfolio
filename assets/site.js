/* Nathan Fritsch · V3 · interactions communes à toutes les pages */
(() => {
  const d = document, root = d.documentElement, body = d.body;
  const $ = (s, c = d) => c.querySelector(s);
  const $$ = (s, c = d) => [...c.querySelectorAll(s)];
  const reduce = matchMedia('(prefers-reduced-motion: reduce)').matches;
  const fine = matchMedia('(hover:hover) and (pointer:fine)').matches;
  const clamp = (v, a, b) => Math.min(b, Math.max(a, v));
  const ICON_X = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" aria-hidden="true"><path d="M6 6l12 12M18 6 6 18"/></svg>';

  /* ── En-tête : fond au défilement, se cache en descendant ── */
  const hd = $('.hd'), mcta = $('.mcta');
  let lastY = scrollY, nearEnd = false;
  function onScroll() {
    const y = scrollY;
    hd.classList.toggle('solid', y > 30);
    if (!body.classList.contains('menu-open')) hd.classList.toggle('hide', y > lastY && y > 480);
    if (mcta) mcta.classList.toggle('show', y > innerHeight * .7 && !nearEnd);
    lastY = y;
  }
  addEventListener('scroll', onScroll, { passive: true });
  onScroll();
  // le bouton devis collé en bas (mobile) s'efface quand un formulaire ou le pied de page est à l'écran
  if (mcta && 'IntersectionObserver' in window) {
    const seen = new Set();
    const io = new IntersectionObserver(es => {
      es.forEach(x => (x.isIntersecting ? seen.add(x.target) : seen.delete(x.target)));
      nearEnd = seen.size > 0;
      onScroll();
    }, { rootMargin: '0px 0px -8% 0px' });
    $$('#contact, .cta-band, .ft').forEach(el => io.observe(el));
    // version sombre du bouton quand il passe au-dessus d'une section claire
    const lit = new Set();
    const lio = new IntersectionObserver(es => {
      es.forEach(x => (x.isIntersecting ? lit.add(x.target) : lit.delete(x.target)));
      mcta.classList.toggle('on-light', lit.size > 0);
    }, { rootMargin: '-86% 0px -4% 0px' });
    $$('.light').forEach(el => lio.observe(el));
  }

  /* ── Menu mobile : sous-menus repliés, un seul ouvert à la fois ── */
  const burger = $('.burger');
  const closeSubs = () => $$('.mm-g.open').forEach(g => { g.classList.remove('open'); $('.mm-t', g).setAttribute('aria-expanded', 'false'); });
  function setMenu(open) {
    body.classList.toggle('menu-open', open);
    root.classList.toggle('lock', open);
    burger.setAttribute('aria-expanded', open);
    if (open) hd.classList.remove('hide'); else closeSubs();
  }
  burger.addEventListener('click', () => setMenu(!body.classList.contains('menu-open')));
  $$('.mm-g button.mm-t').forEach(b => b.addEventListener('click', () => {
    const g = b.closest('.mm-g'), open = !g.classList.contains('open');
    closeSubs();
    g.classList.toggle('open', open);
    b.setAttribute('aria-expanded', open);
  }));
  matchMedia('(min-width:1081px)').addEventListener('change', e => { if (e.matches) setMenu(false); });
  addEventListener('pageshow', e => { if (e.persisted) setMenu(false); });

  /* ── Liens vers une section de la page courante : simple défilement ── */
  function goTo(el) {
    const top = Math.max(0, el.getBoundingClientRect().top + scrollY - 72), y0 = scrollY;
    scrollTo({ top, behavior: reduce ? 'auto' : 'smooth' });
    // filet de sécurité : si le défilement doux ne démarre pas, on saute directement à la section
    setTimeout(() => { if (Math.abs(scrollY - y0) < 2 && Math.abs(top - y0) > 2) scrollTo({ top, behavior: 'instant' }); }, 500);
  }
  const norm = p => p.replace(/\/index(\.html)?$/, '/').replace(/\.html$/, '');
  d.addEventListener('click', e => {
    const a = e.target.closest('a[href]');
    if (!a || a.target === '_blank' || e.metaKey || e.ctrlKey || e.shiftKey) return;
    let u;
    try { u = new URL(a.getAttribute('href'), location.href); } catch (_) { return; }
    if (u.origin !== location.origin || !u.hash || norm(u.pathname) !== norm(location.pathname)) return;
    const el = $(u.hash);
    if (!el) return;
    e.preventDefault();
    setMenu(false);
    goTo(el);
    history.replaceState(history.state, '', u.hash);
  });

  /* ── Titres découpés en mots (apparition ligne à ligne) ── */
  $$('.split').forEach(el => {
    let i = 0;
    const walk = node => [...node.childNodes].forEach(n => {
      if (n.nodeType === 3) {
        const frag = d.createDocumentFragment();
        n.textContent.split(/(\s+)/).forEach(part => {
          if (!part) return;
          if (/^\s+$/.test(part)) { frag.appendChild(d.createTextNode(' ')); return; }
          const w = d.createElement('span'), s = d.createElement('span');
          w.className = 'w';
          s.textContent = part;
          s.style.setProperty('--i', i++);
          w.appendChild(s);
          frag.appendChild(w);
        });
        n.replaceWith(frag);
      } else if (n.nodeType === 1 && n.tagName !== 'BR') walk(n);
    });
    walk(el);
  });

  /* ── Apparitions au défilement ── */
  const rv = $$('[data-rv], .split');
  const show = el => el.classList.add('in');
  if (reduce || !('IntersectionObserver' in window)) rv.forEach(show);
  else {
    const io = new IntersectionObserver(es => es.forEach(x => { if (x.isIntersecting) { show(x.target); io.unobserve(x.target); } }),
      { threshold: .1, rootMargin: '0px 0px -5% 0px' });
    rv.forEach(el => io.observe(el));
    // filet de sécurité : rien ne doit rester invisible si l'observateur ne se déclenche pas
    let last = 0;
    const check = () => {
      const now = Date.now();
      if (now - last < 120) return;
      last = now;
      rv.forEach(el => {
        if (el.classList.contains('in')) return;
        const r = el.getBoundingClientRect();
        if (r.top < innerHeight * .94 && r.bottom > 0) show(el);
      });
    };
    [80, 500, 1500].forEach(t => setTimeout(() => { last = 0; check(); }, t));
    addEventListener('scroll', check, { passive: true });
    addEventListener('load', check);
    addEventListener('pageshow', check);
  }

  /* ── Vidéos d'aperçu : chargées et lues seulement quand elles sont à l'écran ── */
  const loops = $$('video[data-src]');
  const conn = navigator.connection || {};
  const saver = conn.saveData || /(^|-)2g$/.test(conn.effectiveType || '');
  if (loops.length && !reduce && !saver && 'IntersectionObserver' in window) {
    const vio = new IntersectionObserver(es => es.forEach(x => {
      const v = x.target;
      if (x.isIntersecting) {
        if (!v.getAttribute('src')) v.src = v.dataset.src;
        const p = v.play();
        if (p) p.catch(() => {});
      } else if (!v.paused) v.pause();
    }), { rootMargin: '150px 0px', threshold: .1 });
    const start = () => loops.forEach(v => vio.observe(v));
    if (d.readyState === 'complete') start(); else addEventListener('load', start);
  }

  /* ── Film en plein écran avec le son (éléments data-film) ── */
  let fm = null;
  function closeFilm(fromPop) {
    if (!fm) return;
    const v = $('video', fm);
    v.pause();
    v.removeAttribute('src');
    v.load();
    fm.remove();
    fm = null;
    root.classList.remove('lock');
    if (!fromPop && history.state && history.state.overlay) history.back();
  }
  function openFilm(src, ratio, poster) {
    closeFilm(true);
    fm = d.createElement('div');
    fm.className = 'fm';
    fm.setAttribute('role', 'dialog');
    fm.setAttribute('aria-label', 'Lecture de la vidéo');
    fm.innerHTML = `<button type="button" class="lb-x" aria-label="Fermer la vidéo">${ICON_X}</button>` +
      `<div class="fm-box ${ratio === '9/16' ? 'v' : 'h'}"><video controls autoplay playsinline${poster ? ` poster="${poster}"` : ''} src="${src}"></video></div>`;
    body.appendChild(fm);
    root.classList.add('lock');
    history.pushState({ overlay: 1 }, '');
    fm.addEventListener('click', e => { if (e.target === fm || e.target.closest('.lb-x')) closeFilm(); });
    const p = $('video', fm).play();
    if (p) p.catch(() => {});
  }
  d.addEventListener('click', e => {
    const b = e.target.closest('[data-film]');
    if (!b) return;
    e.preventDefault();
    openFilm(b.dataset.film, b.dataset.ratio, b.dataset.poster);
  });
  addEventListener('popstate', () => closeFilm(true));

  /* ── Lecteur intégré (page projet) : l'affiche devient la vidéo au clic ── */
  function startPlayer(p) {
    if (p.classList.contains('on')) return;
    $$('.player.on video').forEach(v => v.pause());
    const v = d.createElement('video'), im = $('img', p);
    v.controls = true;
    v.playsInline = true;
    v.setAttribute('playsinline', '');
    if (im) v.poster = im.currentSrc || im.src;
    v.src = p.dataset.src;
    p.appendChild(v);
    p.classList.add('on');
    p.removeAttribute('role');
    p.removeAttribute('tabindex');
    const pr = v.play();
    if (pr) pr.catch(() => {});
  }
  d.addEventListener('click', e => { const p = e.target.closest('.player'); if (p) startPlayer(p); });

  /* ── Clavier : Échap ferme, Entrée/Espace lance un lecteur ── */
  addEventListener('keydown', e => {
    if (e.key === 'Escape') { closeFilm(); setMenu(false); }
    const t = e.target;
    if ((e.key === 'Enter' || e.key === ' ') && t.classList && t.classList.contains('player') && !t.classList.contains('on')) {
      e.preventDefault();
      startPlayer(t);
    }
  });

  /* ── Effets liés au défilement : bandeau qui s'élargit, léger décalage des vidéos du hero ── */
  const band = $('[data-grow]'), reels = $$('.hero .reel');
  function fx() {
    if (band) {
      const r = band.getBoundingClientRect();
      band.style.setProperty('--g', clamp((innerHeight - r.top) / (innerHeight * .8), 0, 1).toFixed(3));
    }
    if (fine && reels.length && scrollY < innerHeight * 1.3) {
      reels.forEach((el, i) => el.style.setProperty('--py', (scrollY * (i ? -.11 : -.04)).toFixed(1) + 'px'));
    }
  }
  if (reduce) { if (band) band.style.setProperty('--g', 1); }
  else if (band || reels.length) {
    addEventListener('scroll', fx, { passive: true });
    addEventListener('resize', fx);
    fx();
  }

  /* ── Filtres de la page Réalisations ── */
  const filters = $('#filters'), grid = $('#grid');
  if (filters && grid) {
    const chips = $$('.chip', filters), cards = $$('.card', grid);
    const alias = { evenement: 'evenementiel', entreprise: 'entreprises' };
    const apply = (cat, save) => {
      cat = alias[cat] || cat;
      if (!chips.some(c => c.dataset.cat === cat)) cat = 'all';
      chips.forEach(c => { const on = c.dataset.cat === cat; c.classList.toggle('on', on); c.setAttribute('aria-pressed', on); });
      cards.forEach(c => {
        c.classList.toggle('off', cat !== 'all' && !c.dataset.cats.split(' ').includes(cat));
        c.classList.add('in');
      });
      if (save) history.replaceState(history.state, '', cat === 'all' ? location.pathname : `${location.pathname}?cat=${cat}`);
    };
    filters.addEventListener('click', e => { const c = e.target.closest('.chip'); if (c) apply(c.dataset.cat, true); });
    apply(new URLSearchParams(location.search).get('cat') || 'all', false);
  }

  /* ── Curseur personnalisé (souris uniquement) ── */
  if (fine && !reduce) {
    const cx = d.createElement('div');
    cx.id = 'cx';
    cx.innerHTML = '<div class="c-ring"><span>Voir</span></div><div class="c-dot"></div>';
    body.appendChild(cx);
    const ring = $('.c-ring', cx), dot = $('.c-dot', cx), lbl = $('span', ring);
    let mx = -100, my = -100, rx = -100, ry = -100, moved = false;
    addEventListener('mousemove', e => {
      mx = e.clientX; my = e.clientY;
      if (!moved) { moved = true; rx = mx; ry = my; }
      dot.style.transform = `translate(${mx}px,${my}px) translate(-50%,-50%)`;
    }, { passive: true });
    (function loop() {
      rx += (mx - rx) * .18; ry += (my - ry) * .18;
      ring.style.transform = `translate(${rx}px,${ry}px) translate(-50%,-50%)`;
      requestAnimationFrame(loop);
    })();
    d.addEventListener('mouseover', e => {
      const t = e.target;
      if (!t.closest) return;
      const v = t.closest('[data-cursor]');
      const l = t.closest('a,button,summary,label,input,select,textarea,.player');
      body.classList.toggle('c-view', !!v && !(v.classList.contains('player') && v.classList.contains('on')));
      body.classList.toggle('c-link', !v && !!l);
      if (v) lbl.textContent = v.dataset.cursor || 'Voir';
      body.classList.toggle('c-light', !!t.closest('.light'));
    });
  }

  /* ── Année du pied de page ── */
  $$('[data-year]').forEach(el => { el.textContent = new Date().getFullYear(); });
})();
