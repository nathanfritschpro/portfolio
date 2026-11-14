/* Page projet : galerie en colonnes (sans recadrage) + visionneuse plein écran */
(() => {
  const d = document, root = d.documentElement;
  const gal = d.getElementById('gal'), raw = d.getElementById('gal-data');
  if (!gal || !raw) return;

  const data = JSON.parse(raw.textContent);            // [fichier, largeur, hauteur]
  const sub = gal.dataset.base.slice('photos'.length);  // "" ou "/dossier"
  const P = 'photos' + sub + '/', T = 'thumbs' + sub + '/';
  const title = gal.dataset.title || '';
  const portrait = parseFloat(gal.dataset.portrait || '.5');
  const more = d.getElementById('more');
  const BATCH = 24;
  let shown = 0, n = 0, cols = [], heights = [];

  // nombre de colonnes selon la largeur et l'orientation dominante des photos
  const colCount = () => {
    const w = gal.clientWidth;
    if (w < 600) return portrait < .25 ? 1 : 2;
    if (w < 1000) return portrait < .25 ? 2 : 3;
    return portrait > .6 ? 4 : 3;
  };

  function add(count) {
    const end = Math.min(data.length, shown + count);
    for (let i = shown; i < end; i++) {
      const [f, w, h] = data[i];
      let k = 0;
      for (let j = 1; j < n; j++) if (heights[j] < heights[k] - 1e-6) k = j;   // colonne la moins haute
      heights[k] += h / w;
      const b = d.createElement('button');
      b.type = 'button';
      b.className = 'ph-item';
      b.dataset.i = i;
      b.style.aspectRatio = `${w} / ${h}`;
      b.setAttribute('aria-label', `Agrandir la photo ${i + 1}`);
      const im = new Image();
      im.alt = `${title}, photo ${i + 1}`;
      im.loading = 'lazy';
      im.decoding = 'async';
      im.width = w;
      im.height = h;
      im.onload = () => im.classList.add('ld');
      im.src = T + f;
      if (im.complete) im.classList.add('ld');
      b.appendChild(im);
      cols[k].appendChild(b);
    }
    shown = end;
    if (more) {
      const left = data.length - shown;
      more.hidden = left <= 0;
      if (left > 0) more.textContent = `Afficher plus de photos (${left})`;
    }
  }

  function build() {
    const keep = shown || (data.length <= BATCH + 8 ? data.length : BATCH);
    n = colCount();
    gal.textContent = '';
    cols = [];
    heights = [];
    for (let i = 0; i < n; i++) {
      const c = d.createElement('div');
      c.className = 'col';
      gal.appendChild(c);
      cols.push(c);
      heights.push(0);
    }
    shown = 0;
    add(keep);
  }

  if (more) more.addEventListener('click', () => add(BATCH));
  let rt;
  addEventListener('resize', () => { clearTimeout(rt); rt = setTimeout(() => { if (colCount() !== n) build(); }, 150); });
  build();

  /* ── Visionneuse ── */
  const ICON_X = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" aria-hidden="true"><path d="M6 6l12 12M18 6 6 18"/></svg>';
  const ICON_AR = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M5 12h14M13 6l6 6-6 6"/></svg>';
  let lb = null, img = null, count = null, cur = 0, token = 0;
  const at = i => data[(i + data.length) % data.length];

  function fit() {
    const [, w, h] = data[cur];
    const s = Math.min((innerWidth * .94) / w, (innerHeight * .84) / h);
    img.style.width = Math.round(w * s) + 'px';
    img.style.height = Math.round(h * s) + 'px';
  }

  function show(i) {
    cur = (i + data.length) % data.length;
    const my = ++token, f = data[cur][0];
    img.src = T + f;                                   // vignette tout de suite…
    img.alt = `${title}, photo ${cur + 1}`;
    fit();
    count.textContent = `${cur + 1} / ${data.length}`;
    const full = new Image();                          // …puis la photo en pleine définition
    full.onload = () => {
      if (my !== token || !lb || lb.hidden) return;
      img.src = P + f;
      new Image().src = P + at(cur + 1)[0];
    };
    full.src = P + f;
    new Image().src = T + at(cur + 1)[0];
    new Image().src = T + at(cur - 1)[0];
  }

  function close(fromPop) {
    if (!lb || lb.hidden) return;
    lb.hidden = true;
    token++;
    root.classList.remove('lock');
    if (!fromPop && history.state && history.state.overlay) history.back();
  }

  function open(i) {
    if (!lb) {
      lb = d.createElement('div');
      lb.className = 'lb';
      lb.setAttribute('role', 'dialog');
      lb.setAttribute('aria-label', 'Photo en grand');
      lb.innerHTML = `<button type="button" class="lb-x" aria-label="Fermer">${ICON_X}</button>` +
        `<button type="button" class="lb-nav lb-prev" aria-label="Photo précédente">${ICON_AR}</button>` +
        `<img alt=""><button type="button" class="lb-nav lb-next" aria-label="Photo suivante">${ICON_AR}</button>` +
        '<div class="lb-count" aria-live="polite"></div>';
      d.body.appendChild(lb);
      img = lb.querySelector('img');
      count = lb.querySelector('.lb-count');
      lb.addEventListener('click', e => {
        if (e.target.closest('.lb-prev')) show(cur - 1);
        else if (e.target.closest('.lb-next') || e.target === img) show(cur + 1);
        else close();
      });
      // glisser : gauche/droite pour changer de photo, vers le bas pour fermer
      let x0 = null, y0 = 0;
      lb.addEventListener('touchstart', e => { x0 = e.touches[0].clientX; y0 = e.touches[0].clientY; }, { passive: true });
      lb.addEventListener('touchend', e => {
        if (x0 === null) return;
        const dx = e.changedTouches[0].clientX - x0, dy = e.changedTouches[0].clientY - y0;
        x0 = null;
        if (Math.abs(dx) > 45 && Math.abs(dx) > Math.abs(dy)) { e.preventDefault(); show(cur + (dx < 0 ? 1 : -1)); }
        else if (dy > 90 && dy > Math.abs(dx)) { e.preventDefault(); close(); }
      });
    }
    lb.hidden = false;
    root.classList.add('lock');
    show(i);
    history.pushState({ overlay: 1 }, '');
  }

  gal.addEventListener('click', e => { const b = e.target.closest('.ph-item'); if (b) open(+b.dataset.i); });
  addEventListener('popstate', () => close(true));
  addEventListener('keydown', e => {
    if (!lb || lb.hidden) return;
    if (e.key === 'Escape') close();
    else if (e.key === 'ArrowRight') show(cur + 1);
    else if (e.key === 'ArrowLeft') show(cur - 1);
  });
  addEventListener('resize', () => { if (lb && !lb.hidden) fit(); });
})();
