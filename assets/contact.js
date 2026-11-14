/* Formulaire de devis (accueil et page contact) */
(() => {
  const form = document.getElementById('devis');
  if (!form) return;
  const err = form.querySelector('.err');
  const done = form.parentElement.querySelector('.done');
  const EMAIL = 'nathan.fritsch.pro@gmail.com';
  const val = n => {
    const el = form.elements[n];
    if (!el) return '';
    return el instanceof RadioNodeList ? el.value : (el.value || '').trim();
  };

  // Pré-sélection depuis une page secteur ou projet (?type=immobilier)
  const pre = new URLSearchParams(location.search).get('type');
  if (pre) {
    const r = form.querySelector(`input[data-k="${pre.replace(/[^a-z]/g, '')}"]`);
    if (r) r.checked = true;
  }

  form.addEventListener('input', () => {
    form.querySelectorAll('.bad').forEach(x => x.classList.remove('bad'));
    err.textContent = '';
  });

  form.addEventListener('submit', async e => {
    e.preventDefault();
    const missing = [];
    if (!val('nom')) missing.push(['nom', 'votre nom']);
    if (!/^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/.test(val('email'))) missing.push(['email', 'une adresse email valide']);
    if (val('message').length < 5) missing.push(['message', 'quelques mots sur votre projet']);
    if (missing.length) {
      missing.forEach(([n]) => form.elements[n].classList.add('bad'));
      err.textContent = 'Il manque ' + missing.map(m => m[1]).join(', ') + '.';
      form.elements[missing[0][0]].focus();
      return;
    }
    err.textContent = '';
    form.elements._subject.value = `Demande de devis · ${val('type_projet') || 'Projet'} · ${val('nom')}`;
    form.classList.add('busy');
    try {
      const r = await fetch(form.action, { method: 'POST', body: new FormData(form), headers: { Accept: 'application/json' } });
      if (!r.ok) throw new Error(String(r.status));
      form.hidden = true;
      done.hidden = false;
      done.scrollIntoView({ block: 'center' });
    } catch (_) {
      err.innerHTML = `L'envoi n'a pas fonctionné. Écrivez-moi directement à <a href="mailto:${EMAIL}">${EMAIL}</a>.`;
    } finally {
      form.classList.remove('busy');
    }
  });
})();
