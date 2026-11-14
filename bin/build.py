#!/usr/bin/env python3
"""Génère le site (V3) : accueil, réalisations, pages secteur, pages projet, contact, pages légales.

Usage (depuis la racine du site) :
    python3 bin/media.py     # seulement si des photos ou vidéos ont changé
    python3 bin/build.py

Tout le contenu (textes, projets, ordre) est défini dans ce fichier.
"""
from __future__ import annotations

import hashlib
import html
import json
import re
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SITE = "https://www.nathanfritsch.com"
EMAIL = "nathan.fritsch.pro@gmail.com"
IG_HANDLE = "nathanfrt_visuals"
IG = f"https://www.instagram.com/{IG_HANDLE}"
CAL = "https://calendly.com/nathan-fritsch-pro/30min"
FORM = "https://formspree.io/f/xljdopkj"

INDEX = json.loads((ROOT / "bin/media-index.json").read_text(encoding="utf-8"))
DIMS: dict[str, list[int]] = INDEX["photos"]
VIDEOS: dict[str, dict] = INDEX["videos"]
PHOTOS: dict[str, list[str]] = json.loads((ROOT / "bin/photos.json").read_text(encoding="utf-8"))
ABOUT_PHOTO = "photos/about-8148.jpg"
AVATAR = "assets/avatar.jpg"
BAND_PHOTO = "photos/triatlon-lacnau/dimanche-M/IMG_1419.jpg"
# Vidéo de présentation : déposer le fichier ici, elle remplacera le portrait dans « À propos »
ABOUT_VIDEO = "assets/video/presentation.mp4"

# ───────────────────────────── Icônes ─────────────────────────────
def svg(body: str, vb: str = "0 0 24 24", extra: str = "") -> str:
    return f'<svg viewBox="{vb}" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"{extra}>{body}</svg>'

I_ARROW = svg('<path d="M2 10 10 2M4 2h6v6"/>', "0 0 12 12")
I_RIGHT = svg('<path d="M1 6h10M7 2l4 4-4 4"/>', "0 0 12 12")
I_CHEV = svg('<path d="m2 3.5 3 3 3-3"/>', "0 0 10 10", ' class="chev"')
I_PLAY = '<svg viewBox="0 0 12 12" fill="currentColor" aria-hidden="true"><path d="M2.5 1.2v9.6L10.6 6z"/></svg>'
I_CAM = svg('<path d="M4 8h3l1.6-2.5h6.8L17 8h3a1 1 0 0 1 1 1v9a1 1 0 0 1-1 1H4a1 1 0 0 1-1-1V9a1 1 0 0 1 1-1z"/><circle cx="12" cy="13.2" r="3.4"/>')
I_VID = svg('<rect x="3" y="6" width="12.5" height="12" rx="2.2"/><path d="m15.5 10.4 5.5-3v9.2l-5.5-3z"/>')
I_DUO = svg('<rect x="3" y="5" width="13" height="10" rx="2"/><path d="M8 19h11a2 2 0 0 0 2-2V9"/>')
I_CHECK = svg('<path d="m5 12.5 4.5 4.5L19 7.5"/>')
I_IG = svg('<rect x="3" y="3" width="18" height="18" rx="5"/><circle cx="12" cy="12" r="4"/><circle cx="17.4" cy="6.6" r="1" fill="currentColor" stroke="none"/>')
I_MAIL = svg('<rect x="3" y="5" width="18" height="14" rx="2.2"/><path d="m3.5 7.5 8.5 6 8.5-6"/>')
I_CAL = svg('<rect x="3.5" y="5" width="17" height="15.5" rx="2.2"/><path d="M3.5 10h17M8 3v4M16 3v4"/>')
I_X = svg('<path d="M6 6l12 12M18 6 6 18"/>')
I_BACK = svg('<path d="M11 6H1M5 2 1 6l4 4"/>', "0 0 12 12")


def e(s: str) -> str:
    return html.escape(s, quote=True)


# ───────────────────────────── Médias ─────────────────────────────
_hash_cache: dict[str, str] = {}


def ver(path: str) -> str:
    """URL + empreinte courte : évite qu'un navigateur garde une ancienne version d'une vidéo ou d'une affiche."""
    if path not in _hash_cache:
        f = ROOT / path
        h = hashlib.md5()
        with f.open("rb") as fh:
            h.update(fh.read(262144))
        h.update(str(f.stat().st_size).encode())
        _hash_cache[path] = h.hexdigest()[:8]
    return f"{path}?v={_hash_cache[path]}"


def thumb(path: str) -> str:
    return "thumbs/" + path[len("photos/"):]


def img(path: str, alt: str = "", sizes: str = "(max-width:900px) 46vw, 30vw", lazy: bool = True, cls: str = "") -> str:
    w, h = DIMS[path]
    tw = min(720, w)
    attrs = f'src="{thumb(path)}" srcset="{thumb(path)} {tw}w, {path} {w}w" sizes="{sizes}" width="{w}" height="{h}" alt="{e(alt)}"'
    attrs += ' loading="lazy" decoding="async"' if lazy else ' fetchpriority="high" decoding="async"'
    if cls:
        attrs += f' class="{cls}"'
    return f"<img {attrs}>"


def poster_of(video: str) -> str:
    return "posters/" + video[len("videos/"):].replace("/", "-").rsplit(".", 1)[0] + ".jpg"


def dur(video: str) -> str:
    d = round(VIDEOS[video]["d"])
    return f"{d}&nbsp;s" if d < 60 else f"{d // 60}&nbsp;min&nbsp;{d % 60:02d}"


def ratio(video: str) -> str:
    v = VIDEOS[video]
    return "9/16" if v["h"] > v["w"] else "16/9"


def ph(slug: str, name: str) -> str:
    """Chemin d'une photo d'un projet à partir de son nom (sans extension)."""
    for p in PHOTOS[slug]:
        if p.rsplit("/", 1)[1].rsplit(".", 1)[0] == name:
            return p
    raise KeyError(f"{slug}: {name}")


def ar(path: str) -> float:
    w, h = DIMS[path]
    return w / h


# ───────────────────────────── Contenu ─────────────────────────────
SECTORS = [
    dict(slug="evenementiel", name="Événementiel", short="Soirées, séminaires, ouvertures", form="evenement",
         hook="Votre événement se vit une fois. Les images restent.",
         offers=["Reportage photo", "Aftermovie", "Photos express pour les réseaux", "Ouvertures et inaugurations", "Mariages et célébrations privées"]),
    dict(slug="sport", name="Sport", short="Compétitions, clubs, athlètes", form="sport",
         hook="L'intensité d'un geste, figée pour de bon.",
         offers=["Couverture de compétition", "Contenus pour les partenaires", "Portraits d'athlètes", "Aftermovie et vidéos récap", "Clubs et associations"]),
    dict(slug="immobilier", name="Immobilier et conciergeries", nav="Immobilier", short="Vendre et louer plus vite", form="immobilier",
         hook="Des biens qui se démarquent dans les annonces.",
         offers=["Photographie HDR", "Vidéo de visite", "Annonces Airbnb et Booking", "Formats verticaux pour les réseaux", "Détails et ambiance"]),
    dict(slug="entreprises", name="Entreprises et marques", short="Commerces, restaurants, marques", form="entreprise",
         hook="Des images qui donnent envie de vous choisir.",
         offers=["Photos pour votre site et vos réseaux", "Vidéos verticales pour Instagram et TikTok", "Film de présentation", "Portraits d'équipe", "Ouvertures et inaugurations"]),
]
SECTOR = {s["slug"]: s for s in SECTORS}

OF_FILM = "videos/one-fitness/ouverture.mp4"
FK_FILM = "videos/french-kiss/brunch.mp4"
LP_FILM = "videos/evenement/lacanau-pro-2026.mp4"
MAHI_FILM = "videos/le-mahi-mahi-n1.mp4"

PROJECTS = [
    dict(slug="one-fitness", title="One Fitness Club", kind="Ouverture d'une salle de sport", place="Bordeaux",
         sectors=["entreprises", "evenementiel"], cover="IMG_3147",
         pitch="Le jour de l'ouverture, j'ai tout capté&nbsp;: la foule, le ruban coupé, les premiers entraînements.",
         mission="Mettre en images l'ouverture du One Fitness Club&nbsp;: l'attente devant les portes, le ruban coupé, la découverte des espaces et les premiers entraînements. Des contenus pensés pour les réseaux du club.",
         delivered=[("vid", "Un film vertical de {d0}", "L'ouverture racontée en moins d'une minute, au format Instagram et TikTok."),
                    ("cam", "Un reportage photo", "La foule, les équipes, les espaces et les premiers entraînements.")],
         films=[(OF_FILM, "Film de l'ouverture")], loop="videos/one-fitness/ouverture-loop-2.mp4", hero_loop="videos/one-fitness/ouverture-loop.mp4",
         mosaic=["IMG_2824", "IMG_3393"], og=("IMG_3393", .43)),
    dict(slug="french-kiss", title="French Kiss", kind="Restaurant", place="Bordeaux",
         sectors=["entreprises"], cover="IMG_2543",
         pitch="Un brunch en famille, filmé et photographié pour donner envie de réserver.",
         mission="Mettre en images le brunch du French Kiss&nbsp;: le buffet, les cocktails, l'ambiance du lieu et les familles attablées. Des contenus pensés pour donner envie de réserver.",
         delivered=[("vid", "Un film vertical de {d0}", "Le brunch comme si vous y étiez, au format Instagram et TikTok."),
                    ("cam", "Un reportage photo", "Le lieu, le buffet, les assiettes et les moments en famille.")],
         films=[(FK_FILM, "Film du brunch")], loop="videos/french-kiss/brunch-loop-2.mp4", hero_loop="videos/french-kiss/brunch-loop.mp4",
         mosaic=["IMG_2543", "IMG_2500"], og=("IMG_2543", .77)),
    dict(slug="lacanau-pro", title="Lacanau Pro", kind="Compétition de surf", place="Lacanau",
         sectors=["evenementiel", "sport"], cover="IMG_3564",
         pitch="Plusieurs jours au cœur d'un grand rendez-vous du surf, en photo et en vidéo.",
         mission="Plusieurs jours au cœur du Lacanau Pro 2026, l'un des grands rendez-vous du surf&nbsp;: l'action dans l'eau, l'ambiance sur le sable, les riders et le public.",
         delivered=[("vid", "Un film de {d0}", "L'aftermovie de la compétition&nbsp;: surf, village, concerts et podiums."),
                    ("cam", "Un reportage photo", "L'action dans l'eau, les riders, le public et les remises de prix.")],
         films=[(LP_FILM, "Aftermovie")], mosaic=["IMG_2373", "IMG_4439"], og=("IMG_4439", .5)),
    dict(slug="le-mahi-mahi", title="Le Mahi Mahi", kind="Base nautique", place="Lac de Lacanau",
         sectors=["entreprises"], cover="IMG_6451",
         pitch="Des images pour la communication d'une base nautique et de ses excursions sur le lac.",
         mission="Des images pour la communication du Mahi Mahi, base nautique sur le lac de Lacanau, et pour promouvoir ses excursions sur le lac.",
         delivered=[("vid", "Un film d'ambiance de {d0}", "Une sortie sur le lac, pour donner envie d'embarquer."),
                    ("cam", "Un reportage photo", "Portraits, navigation et instants de vie à bord.")],
         films=[(MAHI_FILM, "Film d'ambiance")], mosaic=["IMG_6163", "IMG_6625"], og=("IMG_6163", .5)),
    dict(slug="triathlon-lacanau", title="Triathlon de Lacanau", kind="Compétition sur deux jours", place="Lacanau",
         sectors=["evenementiel", "sport"], cover="IMG_0365",
         pitch="Départs, transitions, arrivées&nbsp;: toute la course, jusque sur la moto des photographes.",
         mission="Deux jours de course à couvrir, des départs natation aux arrivées. Sur le circuit vélo, j'ai suivi les coureurs depuis une moto dédiée aux photographes, au plus près de l'action.",
         delivered=[("cam", "Un reportage photo sur deux jours", "Natation, vélo, course à pied, arrivées et podiums.")],
         films=[], mosaic=["IMG_6496", "IMG_6232"], og=("IMG_6496", .5)),
    dict(slug="school-cup", title="School Cup", kind="Événement sportif étudiant", place="Bordeaux",
         sectors=["evenementiel", "sport"], cover="IMG_9873",
         pitch="Une journée de matchs, de tribunes en feu et de coupes soulevées.",
         mission="Une journée de compétitions étudiantes suivie d'un bout à l'autre&nbsp;: les matchs, les tribunes, les cérémonies et les moments d'émotion.",
         delivered=[("cam", "Un reportage photo", "Les matchs, les supporters, les célébrations et la remise des coupes.")],
         films=[], mosaic=["IMG_9333", "IMG_8011"], og=("IMG_9040", .5)),
    dict(slug="villas", title="Villas et biens", kind="Villas à vendre et à louer", place="Gironde",
         sectors=["immobilier"], cover="DJI_0032",
         pitch="Photos HDR et vidéos de présentation, pour vendre ou louer plus vite.",
         mission="Des photos HDR et des vidéos de présentation réalisées pour des agents immobiliers et des propriétaires, pour mettre un bien en valeur et donner envie de le visiter.",
         delivered=[("vid", "Des vidéos de présentation", "Des visites filmées pour la vente et la location saisonnière."),
                    ("cam", "Des photos HDR", "Intérieurs lumineux, extérieurs et piscines sous leur meilleur angle.")],
         films=[("videos/immo/maison-bertrand/immo-bertrand.mp4", "Villa à vendre"),
                ("videos/immo/copy_467875FE-2541-41B5-A76C-6958B0EF4574.mp4", "Villa à louer"),
                ("videos/immo/maison-huga.mp4", "Maison Huga"),
                ("videos/immo/copy_11AB6017-150B-4928-8CD5-D4D2920269E2.mp4", "Extérieurs d'une maison"),
                ("videos/immo/DJI_0170.mp4", "Environnement d'un bien")],
         mosaic=["IMG_4788-HDR", "IMG_5253-HDR"], og=("IMG_4800-HDR", .5)),
    dict(slug="surf", title="Surf à Lacanau", kind="Sessions de surf", place="Lacanau Océan",
         sectors=["sport"], cover="_MG_6116",
         pitch="Du plein jour au coucher du soleil, au plus près des vagues.",
         mission="Des sessions à Lacanau Océan, du plein jour au coucher du soleil. J'aime le surf autant que photographier ceux qui le vivent.",
         delivered=[("vid", "Deux films courts", "Une session au coucher du soleil et une session au plus près des vagues."),
                    ("cam", "Une série photo", "Action, silhouettes et lumières de fin de journée.")],
         films=[("videos/surf/sunset-cine.mp4", "Sunset"), ("videos/surf/copy_62B93BBF-DF05-4655-B6B2-0E1BD0E6ED0D.mp4", "Session")],
         mosaic=["IMG_1432", "IMG_5743"], og=("IMG_5743", .5)),
    dict(slug="ski", title="Ski", kind="Sessions en montagne", place="",
         sectors=["sport"], cover="IMG_4075",
         pitch="Descentes, poudreuse et grands décors.",
         mission="Des sessions en montagne&nbsp;: descentes, poudreuse et ambiance de station, au plus près de l'action comme dans les grands décors.",
         delivered=[("vid", "Un film court de {d0}", "Une session en montagne, montée au rythme de la glisse."),
                    ("cam", "Une série photo", "Descentes, portraits et grands décors.")],
         films=[("videos/ski/ski-mael.mp4", "Session")], mosaic=["IMG_5523", "IMG_4698"], og=("IMG_5523", .5)),
    dict(slug="golf", title="Golf", kind="Une journée sur le parcours", place="Bordeaux",
         sectors=["sport"], cover="IMG_4959",
         pitch="Les swings, la concentration et le calme du green.",
         mission="Une journée sur le parcours&nbsp;: les swings, la concentration et le calme du green.",
         delivered=[("vid", "Un film de {d0}", "Swings, concentration et ambiance de parcours."),
                    ("cam", "Une série photo", "Le geste et le décor, d'un trou à l'autre.")],
         films=[("videos/golf/golf-jerome.mp4", "Film")], mosaic=["IMG_4959", "IMG_5045"], og=("IMG_4959", .5)),
]
BY_SLUG = {p["slug"]: p for p in PROJECTS}
for _p in PROJECTS:
    _p["cover"] = ph(_p["slug"], _p["cover"])
    _p["mosaic"] = [ph(_p["slug"], n) for n in _p["mosaic"]]
    _p["og"] = (ph(_p["slug"], _p["og"][0]), _p["og"][1])
    _p["has_photo"] = True
    _p["has_video"] = bool(_p["films"])


def sub(p: dict) -> str:
    return f'{p["kind"]} · {p["place"]}' if p["place"] else p["kind"]


def badges(p: dict) -> str:
    out = '<span class="badge">' + I_CAM + "Photo</span>"
    if p["has_video"]:
        out += '<span class="badge">' + I_VID + "Vidéo</span>"
    return f'<div class="badges">{out}</div>'


def delivered(p: dict, long: bool) -> str:
    d0 = dur(p["films"][0][0]) if p["films"] else ""
    items = ""
    for icon, title, text in p["delivered"]:
        ic = I_VID if icon == "vid" else I_CAM
        title = title.format(d0=d0)
        items += f"<li>{ic}<span><b>{title}</b>{'<small>' + text + '</small>' if long else ''}</span></li>"
    return f'<ul class="dl{" long" if long else ""}">{items}</ul>'


# ───────────────────────────── Gabarit commun ─────────────────────────────
def head(title: str, desc: str, path: str = "", og: str = "assets/og/accueil.jpg", preload: str = "") -> str:
    return f"""<!DOCTYPE html>
<html lang="fr">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0, viewport-fit=cover">
<title>{title}</title>
<meta name="description" content="{e(desc)}">
<link rel="canonical" href="{SITE}/{path}">
<meta property="og:type" content="website">
<meta property="og:site_name" content="Nathan Fritsch">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{e(desc)}">
<meta property="og:url" content="{SITE}/{path}">
<meta property="og:image" content="{SITE}/{og}">
<meta name="twitter:card" content="summary_large_image">
<meta name="theme-color" content="#0B0D0E">
<link rel="icon" href="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 64 64'%3E%3Crect width='64' height='64' rx='14' fill='%230B0D0E'/%3E%3Ctext x='50%25' y='56%25' text-anchor='middle' dominant-baseline='middle' font-family='Georgia,serif' font-size='34' fill='%23F3F0EA'%3ENF%3C/text%3E%3C/svg%3E">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,400..600&family=Inter:wght@400;500;600&display=swap" rel="stylesheet">
{preload}<link rel="stylesheet" href="assets/site.css?v={CSS_V}">
<script>document.documentElement.classList.add('js')</script>
</head>
"""


def header(active: str = "", home: bool = False) -> str:
    quote = "#contact" if home else "contact.html"
    dd = "".join(f'<a href="{s["slug"]}.html"><b>{s["name"]}</b><span>{s["short"]}</span></a>' for s in SECTORS)
    mm_sectors = "".join(f'<a href="{s["slug"]}.html">{s["name"]}</a>' for s in SECTORS)
    mm_projects = '<a href="realisations.html">Toutes les réalisations</a>' + "".join(
        f'<a href="{p["slug"]}.html">{p["title"]}</a>' for p in PROJECTS[:4])
    on = lambda k: ' class="on" aria-current="page"' if active == k else ""
    about = "#apropos" if home else "index.html#apropos"
    return f"""<a class="skip" href="#main">Aller au contenu</a>
<header class="hd">
  <a href="index.html" class="logo" aria-label="Nathan Fritsch, accueil"><b>Nathan Fritsch</b><small>Photo · Vidéo · Bordeaux</small></a>
  <div class="hd-nav" role="navigation" aria-label="Navigation principale">
    <ul class="nav">
      <li><a href="realisations.html"{on('realisations')}>Réalisations</a></li>
      <li><button type="button" aria-haspopup="true">Services {I_CHEV}</button>
        <div class="dd"><div class="dd-in">{dd}</div></div></li>
      <li><a href="{about}">À propos</a></li>
      <li><a href="contact.html"{on('contact')}>Contact</a></li>
    </ul>
  </div>
  <div class="hd-right">
    <a class="hd-ig" href="{IG}" target="_blank" rel="noopener" aria-label="Instagram @{IG_HANDLE}">{I_IG}</a>
    <a href="{quote}" class="btn sm">Demander un devis <span class="ar">{I_ARROW}</span></a>
    <button class="burger" type="button" aria-label="Menu" aria-expanded="false" aria-controls="menu"><i></i><i></i></button>
  </div>
</header>
<div class="mm" id="menu" role="dialog" aria-label="Menu">
  <div class="mm-nav" role="navigation" aria-label="Menu mobile">
    <div class="mm-g">
      <button type="button" class="mm-t" aria-expanded="false">Réalisations<span class="mm-pl"></span></button>
      <div class="mm-sub"><div>{mm_projects}</div></div>
    </div>
    <div class="mm-g">
      <button type="button" class="mm-t" aria-expanded="false">Services<span class="mm-pl"></span></button>
      <div class="mm-sub"><div>{mm_sectors}</div></div>
    </div>
    <div class="mm-g"><a href="{about}" class="mm-t">À propos</a></div>
    <div class="mm-g"><a href="contact.html" class="mm-t">Contact</a></div>
  </div>
  <div class="mm-foot">
    <a href="{quote}" class="btn">Demander un devis <span class="ar">{I_ARROW}</span></a>
    <p><a href="{IG}" target="_blank" rel="noopener">@{IG_HANDLE}</a> · <a href="mailto:{EMAIL}">{EMAIL}</a></p>
  </div>
</div>
"""


def sticky_cta(home: bool) -> str:
    quote = "#contact" if home else "contact.html"
    return f'<div class="mcta"><a href="{quote}" class="btn">Demander un devis <span class="ar">{I_ARROW}</span></a></div>\n'


def footer() -> str:
    sectors = "".join(f'<li><a href="{s["slug"]}.html">{s["name"]}</a></li>' for s in SECTORS)
    return f"""<footer class="ft">
  <div class="wrap">
    <div class="ft-top">
      <div class="ft-brand">
        <a href="index.html" class="logo"><b>Nathan Fritsch</b><small>Photo · Vidéo · Bordeaux</small></a>
        <p>Photographe et vidéaste à Bordeaux.<br>Partout en France.</p>
      </div>
      <div><h4>Réalisations</h4><ul>
        <li><a href="realisations.html">Tous les projets</a></li>
        <li><a href="one-fitness.html">One Fitness Club</a></li>
        <li><a href="french-kiss.html">French Kiss</a></li>
        <li><a href="lacanau-pro.html">Lacanau Pro</a></li>
      </ul></div>
      <div><h4>Services</h4><ul>{sectors}</ul></div>
      <div><h4>Contact</h4><ul>
        <li><a href="contact.html">Demander un devis</a></li>
        <li><a href="{CAL}" target="_blank" rel="noopener">Réserver un appel</a></li>
        <li><a href="{IG}" target="_blank" rel="noopener">@{IG_HANDLE}</a></li>
        <li><a href="mailto:{EMAIL}">{EMAIL}</a></li>
      </ul></div>
    </div>
    <div class="ft-bot">
      <span>© <span data-year>2026</span> Nathan Fritsch</span>
      <span><a href="mentions-legales.html">Mentions légales</a> · <a href="confidentialite.html">Confidentialité</a></span>
    </div>
  </div>
</footer>
"""


def scripts(*extra: str) -> str:
    out = f'<script src="assets/site.js?v={JS_V}" defer></script>\n'
    for x in extra:
        out += f'<script src="assets/{x}?v={JS_V}" defer></script>\n'
    return out


def page(title: str, desc: str, body: str, path: str = "", active: str = "", og: str = "assets/og/accueil.jpg",
         home: bool = False, js: tuple = (), preload: str = "", sticky: bool = True, extra: str = "") -> str:
    cls = ' class="home"' if home else ""
    return (head(title, desc, path, og, preload) + f"<body{cls}>\n" + header(active, home)
            + f'<main id="main">\n{body}</main>\n' + footer() + (sticky_cta(home) if sticky else "") + extra + scripts(*js) + "</body>\n</html>\n")


# ───────────────────────────── Blocs réutilisables ─────────────────────────────
def card(p: dict) -> str:
    return f"""<a class="card" href="{p['slug']}.html" data-cats="{' '.join(p['sectors'])}" data-cursor="Voir" data-rv>
  <div class="card-img">{img(p['cover'], p['title'])}{badges(p)}</div>
  <div class="card-txt"><h3>{p['title']}</h3><p>{sub(p)}</p></div>
</a>"""


def film_button(video: str, label: str, loop: str | None = None, cls: str = "") -> str:
    """Vignette vidéo : ouvre le film avec le son dans une fenêtre (assets/site.js)."""
    r = ratio(video)
    poster = ver(poster_of(video))
    if loop:
        media = f'<video muted loop playsinline preload="none" poster="{ver(loop[:-4] + ".jpg")}" data-src="{ver(loop)}"></video>'
    else:
        media = f'<img src="{poster}" alt="" loading="lazy" decoding="async">'
    return (f'<button type="button" class="film {cls}" data-film="{ver(video)}" data-ratio="{r}" data-poster="{poster}" '
            f'data-cursor="Lire" aria-label="Lire la vidéo : {e(label)}">{media}'
            f'<span class="play">{I_PLAY}</span><span class="film-tag">{label} · {dur(video)}</span></button>')


def mosaic(p: dict) -> str:
    a, b = p["mosaic"]
    link = f'{p["slug"]}.html'
    sizes = "(max-width:900px) 45vw, 22vw"
    pa = f'<a href="{link}" class="mos-ph" data-cursor="Voir">{img(a, p["title"], sizes)}</a>'
    pb = f'<a href="{link}" class="mos-ph" data-cursor="Voir">{img(b, p["title"], sizes)}</a>'
    if p["films"]:
        video, label = p["films"][0]
        if ratio(video) == "9/16":
            k = (9 / 16) * (1 / ar(a) + 1 / ar(b))
            return f'<div class="mos v" style="--l:{k:.3f}fr;--ar:9/16">{film_button(video, label, p.get("loop"))}{pa}{pb}</div>'
        return f'<div class="mos h" style="--b:{ar(a):.3f}fr;--c:{ar(b):.3f}fr">{film_button(video, label)}{pa}{pb}</div>'
    lead = p["cover"]
    k = ar(lead) * (1 / ar(a) + 1 / ar(b))
    w, h = DIMS[lead]
    return (f'<div class="mos v" style="--l:{k:.3f}fr;--ar:{w}/{h}"><a href="{link}" class="mos-ph" data-cursor="Voir">'
            f'{img(lead, p["title"], "(max-width:900px) 55vw, 30vw")}</a>{pa}{pb}</div>')


def case(p: dict, rev: bool = False, tag: str = "h3") -> str:
    return f"""<article class="case{' rev' if rev else ''}">
  <div class="case-media" data-rv>{mosaic(p)}</div>
  <div class="case-txt" data-rv style="--d:.1s">
    {badges(p)}
    <{tag} class="h-m"><a href="{p['slug']}.html">{p['title']}</a></{tag}>
    <p class="case-kind">{sub(p)}</p>
    <p class="case-pitch">{p['pitch']}</p>
    <p class="label">Livré</p>
    {delivered(p, False)}
    <a href="{p['slug']}.html" class="btn ghost">Voir le projet <span class="ar">{I_ARROW}</span></a>
  </div>
</article>"""


def contact_block(h: str = "h2") -> str:
    types = [("evenement", "Événement"), ("sport", "Sport"), ("immobilier", "Immobilier"), ("entreprise", "Entreprise"), ("autre", "Autre")]
    needs = ["Photo", "Vidéo", "Les deux"]
    t = "".join(f'<span class="opt"><input type="radio" name="type_projet" id="t-{k}" value="{v}" data-k="{k}"><label for="t-{k}">{v}</label></span>' for k, v in types)
    n = "".join(f'<span class="opt"><input type="radio" name="besoin" id="n-{i}" value="{v}"><label for="n-{i}">{v}</label></span>' for i, v in enumerate(needs))
    return f"""<div class="wrap contact-grid">
  <div class="contact-txt">
    <{h} class="h-l split">Parlons de votre projet.</{h}>
    <p class="lead" data-rv>Devis gratuit. Réponse sous 24&nbsp;h.</p>
    <div class="me" data-rv>
      <img src="{AVATAR}" alt="Nathan Fritsch" width="56" height="56" loading="lazy" decoding="async">
      <span><b>Nathan Fritsch</b>C'est moi qui vous réponds.</span>
    </div>
  </div>
  <ul class="alts" data-rv>
    <li><a href="{CAL}" target="_blank" rel="noopener"><span class="ic">{I_CAL}</span><span><b>Réserver un appel</b><small>30 minutes, gratuit</small></span><span class="go">{I_ARROW}</span></a></li>
    <li><a href="{IG}" target="_blank" rel="noopener"><span class="ic">{I_IG}</span><span><b>Écrire sur Instagram</b><small>@{IG_HANDLE}</small></span><span class="go">{I_ARROW}</span></a></li>
    <li><a href="mailto:{EMAIL}"><span class="ic">{I_MAIL}</span><span><b>Envoyer un email</b><small>{EMAIL}</small></span><span class="go">{I_ARROW}</span></a></li>
  </ul>
  <div class="form-wrap" data-rv style="--d:.1s">
    <form class="form" id="devis" action="{FORM}" method="POST" novalidate>
      <input type="text" name="_gotcha" class="hp" tabindex="-1" autocomplete="off" aria-hidden="true">
      <input type="hidden" name="_subject" value="Nouvelle demande de devis">
      <fieldset class="fgrp"><legend class="flabel">Votre projet</legend><div class="opts">{t}</div></fieldset>
      <fieldset class="fgrp"><legend class="flabel">Vous avez besoin de</legend><div class="opts">{n}</div></fieldset>
      <div class="row2">
        <div class="fld"><label class="flabel" for="f-nom">Nom</label><input id="f-nom" name="nom" type="text" autocomplete="name" required></div>
        <div class="fld"><label class="flabel" for="f-mail">Email</label><input id="f-mail" name="email" type="email" autocomplete="email" inputmode="email" required></div>
      </div>
      <div class="fld"><label class="flabel" for="f-tel">Téléphone <i>(facultatif)</i></label><input id="f-tel" name="telephone" type="tel" autocomplete="tel" inputmode="tel"></div>
      <div class="fld"><label class="flabel" for="f-msg">Votre message</label><textarea id="f-msg" name="message" placeholder="Votre projet en quelques mots : quoi, où, quand…" required></textarea></div>
      <p class="err" role="alert" aria-live="polite"></p>
      <div class="form-foot">
        <button type="submit" class="btn">Envoyer ma demande <span class="ar">{I_ARROW}</span></button>
        <p class="form-note">Vos informations ne servent qu'à vous répondre. <a href="confidentialite.html">Confidentialité</a></p>
      </div>
    </form>
    <div class="done" role="status" hidden>
      <span class="done-ic">{I_CHECK}</span>
      <h3 class="h-m">Merci, c'est bien reçu.</h3>
      <p>Je reviens vers vous sous 24&nbsp;h.</p>
      <a href="realisations.html" class="btn ghost">Voir les réalisations <span class="ar">{I_ARROW}</span></a>
    </div>
  </div>
</div>"""


def cta_band(form: str = "") -> str:
    q = f"?type={form}" if form else ""
    return f"""<section class="sec cta-band">
  <div class="wrap">
    <h2 class="h-l split">Un projet&nbsp;? Parlons-en.</h2>
    <p class="lead" data-rv>Devis gratuit. Réponse sous 24&nbsp;h.</p>
    <div class="cta-row" data-rv>
      <a href="contact.html{q}" class="btn">Demander un devis <span class="ar">{I_ARROW}</span></a>
      <a href="{CAL}" target="_blank" rel="noopener" class="btn ghost">Réserver un appel <span class="ar">{I_ARROW}</span></a>
    </div>
  </div>
</section>
"""


# ───────────────────────────── Accueil ─────────────────────────────
def index() -> str:
    of, fk = BY_SLUG["one-fitness"], BY_SLUG["french-kiss"]

    def reel(p: dict, label: str) -> str:
        loop = p["hero_loop"]
        return (f'<a class="reel" href="{p["slug"]}.html" data-cursor="Voir">'
                f'<video muted loop playsinline preload="none" poster="{ver(loop[:-4] + ".jpg")}" data-src="{ver(loop)}" aria-label="{e(p["title"])}"></video>'
                f'<span class="reel-tag"><small>{I_VID}{label}</small>{p["title"]}</span></a>')

    others = "".join(card(BY_SLUG[s]) for s in ["lacanau-pro", "le-mahi-mahi", "triathlon-lacanau", "school-cup", "villas", "surf"])
    about_media = (f'<video src="{ABOUT_VIDEO}" poster="{thumb(ABOUT_PHOTO)}" controls playsinline preload="none"></video>'
                   if (ROOT / ABOUT_VIDEO).exists() else img(ABOUT_PHOTO, "Nathan Fritsch, photographe et vidéaste à Bordeaux", "(max-width:900px) 92vw, 40vw"))
    sectors = "".join(f'<a class="chip" href="{s["slug"]}.html">{s["name"]}</a>' for s in SECTORS)
    check = I_CHECK
    ld = json.dumps({"@context": "https://schema.org", "@type": "ProfessionalService", "name": "Nathan Fritsch, photographe et vidéaste",
                     "url": SITE, "image": f"{SITE}/assets/og/accueil.jpg", "email": EMAIL, "areaServed": "France",
                     "address": {"@type": "PostalAddress", "addressLocality": "Bordeaux", "addressCountry": "FR"}, "sameAs": [IG]}, ensure_ascii=False)
    body = f"""<section class="hero">
  <div class="wrap hero-grid">
    <div class="hero-txt">
      <h1 class="h-xl split">Photographe et vidéaste <em>à Bordeaux</em></h1>
      <p class="hero-sub" data-rv style="--d:.25s">Des photos et des vidéos qui donnent envie, livrées prêtes à publier. Partout en France.</p>
      <div class="hero-cta" data-rv style="--d:.35s">
        <a href="#contact" class="btn">Demander un devis <span class="ar">{I_ARROW}</span></a>
        <a href="realisations.html" class="btn ghost">Voir les réalisations</a>
      </div>
      <div class="me" data-rv style="--d:.45s">
        <img src="{AVATAR}" alt="" width="48" height="48" decoding="async">
        <span><b>Nathan Fritsch</b>Devis gratuit · Réponse sous 24&nbsp;h</span>
      </div>
    </div>
    <div class="reels" data-rv style="--d:.2s">
      {reel(of, "Vidéo")}
      {reel(fk, "Vidéo")}
    </div>
  </div>
</section>

<section class="sec" id="realisations">
  <div class="wrap">
    <header class="sec-head">
      <h2 class="h-l split">Dernières réalisations</h2>
      <a class="lnk" href="realisations.html" data-rv>Tout voir {I_RIGHT}</a>
    </header>
    {case(of)}
    {case(fk, rev=True)}
    <div class="cards more-cards">{others}</div>
    <div class="center" data-rv><a href="realisations.html" class="btn ghost">Toutes les réalisations <span class="ar">{I_ARROW}</span></a></div>
  </div>
</section>

<section class="sec light" id="services">
  <div class="wrap">
    <header class="sec-head col">
      <h2 class="h-l split">Photo, vidéo, ou les deux.</h2>
      <p class="lead" data-rv>Un seul interlocuteur, du premier échange à la livraison.</p>
    </header>
    <div class="offers">
      <article class="offer" data-rv>
        <span class="offer-ic">{I_CAM}</span>
        <h3>Photo</h3>
        <p>Votre lieu, vos équipes, vos produits, votre événement.</p>
        <ul><li>{check}Chaque photo est retouchée</li><li>{check}Prêtes pour le web, les réseaux et l'impression</li></ul>
      </article>
      <article class="offer" data-rv style="--d:.08s">
        <span class="offer-ic">{I_VID}</span>
        <h3>Vidéo</h3>
        <p>Des films courts, qui se regardent jusqu'au bout.</p>
        <ul><li>{check}Format vertical pour Instagram et TikTok</li><li>{check}Format horizontal pour votre site</li><li>{check}Montage et étalonnage inclus</li></ul>
      </article>
      <article class="offer feat" data-rv style="--d:.16s">
        <span class="offer-ic">{I_DUO}</span>
        <h3>Photo + vidéo</h3>
        <p>Les deux pendant la même intervention.</p>
        <ul><li>{check}Un rendu cohérent entre vos photos et vos films</li><li>{check}Une seule organisation, un seul devis</li></ul>
      </article>
    </div>
    <ol class="steps">
      <li data-rv><span><b>On échange</b>Appel gratuit, devis clair.</span></li>
      <li data-rv style="--d:.08s"><span><b>Je viens tourner</b>Sur place, discret, efficace.</span></li>
      <li data-rv style="--d:.16s"><span><b>Vous recevez tout</b>Prêt à publier.</span></li>
    </ol>
    <div class="sectors" data-rv><span>Pour qui&nbsp;?</span>{sectors}</div>
  </div>
</section>

<section class="band" aria-label="L'instant, l'émotion, l'image">
  <div class="band-frame" data-grow>
    {img(BAND_PHOTO, "Triathlète allongé dans l'herbe après l'arrivée", "100vw")}
    <p class="band-line">L'instant, l'émotion, l'image.</p>
  </div>
</section>

<section class="sec" id="apropos">
  <div class="wrap about">
    <div class="about-media" data-rv>{about_media}</div>
    <div class="about-txt">
      <h2 class="h-l split">Enchanté, moi c'est Nathan.</h2>
      <p data-rv>Jeune photographe et vidéaste basé à Bordeaux — disponible partout en France et à l'étranger pour accompagner mes clients.</p>
      <p data-rv>Tout a commencé il y a trois ans, avec le premier appareil de mon père — et depuis, l'image ne m'a plus lâché. Je me consacre surtout au sport et à l'événementiel, sans oublier l'immobilier : des univers où je cherche à saisir <strong>l'intensité d'un geste et l'émotion d'un instant</strong>.</p>
      <p data-rv>Ce qui me guide, c'est le regard — cette façon de voir et de raconter qui rend chaque image unique. J'avance avec une idée simple : <strong>toujours faire de son mieux, même quand personne ne regarde</strong>.</p>
      <p class="about-quote" data-rv>Figez l'instant, capturez l'émotion.</p>
      <div class="about-cta" data-rv>
        <a href="#contact" class="btn">Travaillons ensemble <span class="ar">{I_ARROW}</span></a>
        <a class="lnk" href="{IG}" target="_blank" rel="noopener">{I_IG} @{IG_HANDLE}</a>
      </div>
    </div>
  </div>
</section>

<section class="sec contact" id="contact">
{contact_block("h2")}
</section>
"""
    preload = f'<link rel="preload" as="image" href="{ver(of["hero_loop"][:-4] + ".jpg")}" fetchpriority="high">\n'
    return page("Nathan Fritsch · Photographe et vidéaste à Bordeaux",
                "Photographe et vidéaste à Bordeaux. Photos et vidéos pour les entreprises, l'événementiel, le sport et l'immobilier, partout en France. Devis gratuit, réponse sous 24 h.",
                body, home=True, js=("contact.js",), preload=preload,
                extra=f'<script type="application/ld+json">{ld}</script>\n')


# ───────────────────────────── Réalisations + secteurs ─────────────────────────────
def realisations() -> str:
    chips = '<button type="button" class="chip on" data-cat="all" aria-pressed="true">Tout</button>' + "".join(
        f'<button type="button" class="chip" data-cat="{s["slug"]}" aria-pressed="false">{s.get("nav", s["name"])}</button>' for s in SECTORS)
    body = f"""<section class="ph">
  <div class="wrap">
    <h1 class="h-xl split">Réalisations</h1>
    <p class="lead" data-rv>Photo, vidéo, ou les deux. Ouvrez un projet pour voir ce que j'ai livré.</p>
    <div class="chips" id="filters" data-rv>{chips}</div>
  </div>
</section>
<section class="sec tight">
  <div class="wrap">
    <div class="cards" id="grid">{"".join(card(p) for p in PROJECTS)}</div>
  </div>
</section>
{cta_band()}"""
    return page("Réalisations · Nathan Fritsch, photographe et vidéaste à Bordeaux",
                "Projets photo et vidéo réalisés à Bordeaux et partout en France : One Fitness Club, French Kiss, Lacanau Pro, Le Mahi Mahi, immobilier, sport.",
                body, path="realisations", active="realisations", og="assets/og/one-fitness.jpg")


def sector(s: dict) -> str:
    ps = [p for p in PROJECTS if s["slug"] in p["sectors"]]
    n_cases = len(ps) if len(ps) <= 3 else 2
    cases = "".join(case(p, rev=bool(i % 2), tag="h2") for i, p in enumerate(ps[:n_cases]))
    rest = ps[n_cases:]
    cards = f'<div class="cards more-cards">{"".join(card(p) for p in rest)}</div>' if rest else ""
    offers = "".join(f"<li data-rv>{I_CHECK}{o}</li>" for o in s["offers"])
    body = f"""<section class="ph sector-ph">
  <div class="wrap ph-grid">
    <div>
      <h1 class="h-xl split">{s['name']}</h1>
      <p class="lead" data-rv>{s['hook']}</p>
      <div class="hero-cta" data-rv>
        <a href="contact.html?type={s['form']}" class="btn">Demander un devis <span class="ar">{I_ARROW}</span></a>
        <a href="{CAL}" target="_blank" rel="noopener" class="btn ghost">Réserver un appel</a>
      </div>
    </div>
    <div class="does">
      <p class="label" data-rv>Ce que je réalise</p>
      <ul>{offers}</ul>
    </div>
  </div>
</section>
<section class="sec tight">
  <div class="wrap">
    {cases}
    {cards}
  </div>
</section>
{cta_band(s['form'])}"""
    return page(f"{s['name']} · Photographe et vidéaste à Bordeaux · Nathan Fritsch",
                f"{s['hook']} Photo et vidéo à Bordeaux et partout en France : {', '.join(o.lower() for o in s['offers'][:3])}.",
                body, path=s["slug"], og=f"assets/og/{ps[0]['slug']}.jpg")


# ───────────────────────────── Page projet ─────────────────────────────
def player(video: str, label: str, cls: str = "") -> str:
    r = ratio(video)
    load = 'loading="lazy" decoding="async"' if cls else 'fetchpriority="high"'
    return (f'<div class="player {"v" if r == "9/16" else "h"} {cls}" data-src="{ver(video)}" data-cursor="Lire" role="button" tabindex="0" '
            f'aria-label="Lire la vidéo : {e(label)}"><img src="{ver(poster_of(video))}" alt="" {load}>'
            f'<span class="play">{I_PLAY}</span><span class="film-tag">{label} · {dur(video)}</span></div>')


def project(p: dict, nxt: dict) -> str:
    photos = PHOTOS[p["slug"]]
    form = SECTOR[p["sectors"][0]]["form"]
    main_film = p["films"][0] if p["films"] else None
    vertical = bool(main_film) and ratio(main_film[0]) == "9/16"
    info = f"""<div class="proj-info">
      {badges(p)}
      <h1 class="h-xl split">{p['title']}</h1>
      <p class="proj-kind" data-rv>{sub(p)}</p>
      <p class="proj-mission" data-rv>{p['mission']}</p>
      <div data-rv>
        <p class="label">Ce que j'ai livré</p>
        {delivered(p, True)}
      </div>
      <a href="contact.html?type={form}" class="btn" data-rv>Je veux le même résultat <span class="ar">{I_ARROW}</span></a>
    </div>"""
    if main_film and vertical:
        top = f'<div class="proj-top v">{info}<div class="proj-film" data-rv style="--d:.15s">{player(*main_film)}</div></div>'
    elif main_film:
        top = f'<div class="proj-top h">{info}<div class="proj-film" data-rv style="--d:.15s">{player(*main_film)}</div></div>'
    else:
        w, h = DIMS[p["cover"]]
        top = (f'<div class="proj-top v">{info}<div class="proj-film photo" data-rv style="--d:.15s;--ar:{w}/{h}">'
               f'{img(p["cover"], p["title"], "(max-width:900px) 92vw, 36vw", lazy=False)}</div></div>')
    more_films = ""
    if len(p["films"]) > 1:
        tiles = "".join(f'<div data-rv>{player(v, t, "tile")}</div>' for v, t in p["films"][1:])
        more_films = f'<section class="proj-sec"><h2 class="h-m">Autres films</h2><div class="films">{tiles}</div></section>'
    base = photos[0].rsplit("/", 1)[0] if len({x.rsplit("/", 1)[0] for x in photos}) == 1 else "photos"
    data = [[x[len(base) + 1:], DIMS[x][0], DIMS[x][1]] for x in photos]
    portrait = sum(1 for _, w, h in data if h > w) / len(data)
    gallery = f"""<section class="proj-sec" id="photos">
      <h2 class="h-m">Les photos <span class="count">{len(photos)}</span></h2>
      <div class="masonry" id="gal" data-base="{base}" data-title="{e(p['title'])}" data-portrait="{portrait:.2f}"></div>
      <div class="center"><button type="button" class="btn ghost" id="more" hidden>Afficher plus de photos</button></div>
      <script type="application/json" id="gal-data">{json.dumps(data, separators=(',', ':'))}</script>
      <noscript><p class="lead">Activez JavaScript pour afficher la galerie.</p></noscript>
    </section>"""
    body = f"""<article class="proj">
  <div class="wrap">
    <a class="back" href="realisations.html">{I_BACK} Réalisations</a>
    {top}
    {more_films}
    {gallery}
  </div>
</article>
<section class="next">
  <a href="{nxt['slug']}.html" class="wrap next-in" data-cursor="Voir">
    <span class="label">Projet suivant</span>
    <span class="h-l">{nxt['title']}</span>
    <span class="next-sub">{sub(nxt)}</span>
  </a>
</section>
{cta_band(form)}"""
    what = "Photo et vidéo" if p["has_video"] else "Reportage photo"
    desc = re.sub(r"<[^>]+>", "", p["mission"]).replace("&nbsp;", " ")
    return page(f"{p['title']} · {what} · Nathan Fritsch",
                desc, body, path=p["slug"], og=f"assets/og/{p['slug']}.jpg", js=("gallery.js",))


# ───────────────────────────── Contact, légal, 404 ─────────────────────────────
def contact() -> str:
    body = f'<section class="ph contact contact-page">\n{contact_block("h1")}\n</section>\n'
    return page("Contact et devis · Nathan Fritsch, photographe et vidéaste à Bordeaux",
                "Demandez un devis gratuit pour votre projet photo ou vidéo à Bordeaux et partout en France. Réponse sous 24 h.",
                body, path="contact", active="contact", js=("contact.js",), sticky=False)


def legal(name: str, title: str) -> str:
    content = (ROOT / f"bin/legal/{name}.html").read_text(encoding="utf-8")
    body = f"""<section class="ph legal">
  <div class="wrap">
    <h1 class="h-l">{title}</h1>
    <div class="legal-body">
{content}
    </div>
  </div>
</section>
"""
    return page(f"{title} · Nathan Fritsch", f"{title} du site de Nathan Fritsch, photographe et vidéaste à Bordeaux.", body, path=name, sticky=False)


def notfound() -> str:
    body = f"""<section class="ph nf">
  <div class="wrap">
    <h1 class="h-xl">Page introuvable</h1>
    <p class="lead">Cette page n'existe pas ou a été déplacée.</p>
    <div class="hero-cta">
      <a href="/" class="btn">Retour à l'accueil <span class="ar">{I_ARROW}</span></a>
      <a href="/realisations" class="btn ghost">Voir les réalisations</a>
    </div>
  </div>
</section>
"""
    doc = page("Page introuvable · Nathan Fritsch", "Cette page n'existe pas.", body, path="404", sticky=False)
    # Servie pour n'importe quelle adresse inconnue : toutes les adresses relatives partent de la racine
    return doc.replace("<head>", '<head>\n<base href="/">', 1)


# ───────────────────────────── Sorties ─────────────────────────────
def nbsp(doc: str) -> str:
    """Espaces insécables avant ? ! : ; (typographie française), hors balises, scripts et styles."""
    parts = re.split(r"(<script.*?</script>|<style.*?</style>|<[^>]+>)", doc, flags=re.S)
    return "".join(p if p.startswith("<") else re.sub(r" ([?!:;»])", r"&nbsp;\1", p).replace("« ", "«&nbsp;") for p in parts)


def make_og(name: str, photo: str, focus: float) -> None:
    out = ROOT / "assets/og" / f"{name}.jpg"
    src = ROOT / photo
    if out.exists() and out.stat().st_mtime >= src.stat().st_mtime:
        return
    out.parent.mkdir(parents=True, exist_ok=True)
    w, h = DIMS[photo]
    sh = round(h * 1200 / w)
    y = max(0, round((sh - 630) * focus))
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", str(src), "-vf", f"scale=1200:{sh}:flags=lanczos,crop=1200:630:0:{y}",
                    "-q:v", "4", str(out)], check=True)


def make_avatar() -> None:
    out = ROOT / AVATAR
    if out.exists():
        return
    w, _ = DIMS[ABOUT_PHOTO]
    k = w / 720  # repères pris sur la vignette de 720 px de large
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", str(ROOT / ABOUT_PHOTO), "-vf",
                    f"crop={round(290 * k)}:{round(290 * k)}:{round(335 * k)}:{round(150 * k)},scale=192:192:flags=lanczos", "-q:v", "3", str(out)], check=True)


def file_v(rel: str) -> str:
    return hashlib.md5((ROOT / rel).read_bytes()).hexdigest()[:8]


CSS_V = file_v("assets/site.css")
JS_V = hashlib.md5(b"".join((ROOT / f"assets/{n}").read_bytes() for n in ("site.js", "gallery.js", "contact.js"))).hexdigest()[:8]

if __name__ == "__main__":
    make_avatar()
    make_og("accueil", BAND_PHOTO, .45)
    for p in PROJECTS:
        make_og(p["slug"], *p["og"])

    pages = {"index.html": index(), "realisations.html": realisations(), "contact.html": contact(),
             "mentions-legales.html": legal("mentions-legales", "Mentions légales"),
             "confidentialite.html": legal("confidentialite", "Politique de confidentialité"),
             "404.html": notfound()}
    for s in SECTORS:
        pages[f"{s['slug']}.html"] = sector(s)
    for i, p in enumerate(PROJECTS):
        pages[f"{p['slug']}.html"] = project(p, PROJECTS[(i + 1) % len(PROJECTS)])
    for name, doc in pages.items():
        (ROOT / name).write_text(nbsp(doc), encoding="utf-8")

    urls = [""] + [n[:-5] for n in pages if n not in ("index.html", "404.html")]
    (ROOT / "sitemap.xml").write_text('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
                                      + "".join(f"  <url><loc>{SITE}/{u}</loc></url>\n" for u in urls) + "</urlset>\n", encoding="utf-8")
    (ROOT / "robots.txt").write_text(f"User-agent: *\nAllow: /\n\nSitemap: {SITE}/sitemap.xml\n", encoding="utf-8")
    print(f"ok · {len(pages)} pages")
