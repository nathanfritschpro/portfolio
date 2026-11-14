# Nathan Fritsch — site portfolio

Site de Nathan Fritsch, photographe et vidéaste à Bordeaux : <https://www.nathanfritsch.com>

Site statique (HTML, CSS, JavaScript sans dépendance). Les pages sont **générées**
par un script Python : on ne modifie pas les fichiers `.html` à la main.

## Pages

- `index.html` — accueil (hero vidéo, derniers projets, services, à propos, formulaire de devis)
- `realisations.html` — tous les projets, filtrables par secteur (`?cat=sport`…)
- `evenementiel.html`, `sport.html`, `immobilier.html`, `entreprises.html` — pages secteur
- `one-fitness.html`, `french-kiss.html`, `lacanau-pro.html`… — une page par projet
- `contact.html` — formulaire de devis (Formspree), appel Calendly, Instagram, email
- `mentions-legales.html`, `confidentialite.html`, `404.html`

## Modifier le site

Tout le contenu (textes, projets, ordre, vidéos) est dans `bin/build.py`.

```bash
python3 bin/build.py        # régénère toutes les pages, le sitemap et les images de partage
python3 serve.py 8080       # aperçu local sur http://localhost:8080
```

### Ajouter ou changer des photos / vidéos

1. Déposer les originaux dans `~/Desktop/photos/<dossier>` et `~/Desktop/videos/<dossier>`.
2. Déclarer le dossier dans `bin/media.py` (`NEW_PHOTO_SETS`, `FILMS`).
3. Lancer `python3 bin/media.py` : photos ramenées à 2048 px, vignettes de 720 px
   dans `thumbs/`, films encodés en 1080p, boucles d'aperçu, affiches dans `posters/`.
4. Ajouter le projet dans `bin/photos.json` (ordre des photos) et dans `bin/build.py` (`PROJECTS`).
5. Lancer `python3 bin/build.py`.

### Vidéo de présentation (section « À propos »)

Déposer le fichier dans `assets/video/presentation.mp4` puis relancer `python3 bin/build.py` :
la vidéo remplace automatiquement le portrait.

## Fichiers

- `assets/site.css`, `assets/site.js` — design et interactions communs
- `assets/gallery.js` — galerie et visionneuse des pages projet
- `assets/contact.js` — formulaire de devis
- `bin/legal/` — texte des pages légales
- `photos/` (2048 px), `thumbs/` (720 px), `videos/`, `posters/`

## Déploiement

Vercel déploie automatiquement à chaque push sur `main` (aperçu pour les autres branches).
Les fichiers de plus de 100 Mo sont refusés par GitHub : ne jamais en commiter.
