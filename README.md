# Nathan Fritsch — Portfolio

Site portfolio de Nathan Fritsch, photographe & vidéaste basé à Bordeaux
(événementiel · sport · immobilier · drone).

Site statique HTML / CSS / JavaScript vanilla — pas de build, pas de dépendance.

## Structure

- `index.html` — page d'accueil
- `portfolio.html` — portfolio (Photos et Vidéos, `?type=photo|video`)
- `contact.html` — page contact + formulaire
- `serve.py` — petit serveur local (Range HTTP pour la lecture vidéo)
- `photos/` — photos du site (**à ajouter après compression**)
- `videos/` — vidéos du site (**à ajouter après compression**)

## Développement local

Depuis ce dossier :

```bash
python3 serve.py
```

Le site est ensuite servi sur <http://localhost:8080>.

`serve.py` gère les requêtes HTTP Range (contrairement à
`python3 -m http.server`), indispensable pour naviguer dans les vidéos et
afficher leurs previews.

## Déploiement

Site déployé automatiquement par **Vercel** à chaque push sur la branche `main`.

- Hébergement : Vercel
- HTTPS : automatique
- Domaine : (à configurer)

## Notes techniques

- Les médias (photos et vidéos) sont volumineux — ils doivent être compressés
  avant push (photos ≤ 2560 px / 82 %, vidéos H.264 1080p ≤ 15 Mo par fichier).
- Les fichiers `> 100 Mo` sont refusés par GitHub : à ne jamais commiter.
- En dev local, `photos/` et `videos-src/` peuvent être des symlinks vers le
  disque de travail — ils sont gitignorés.
