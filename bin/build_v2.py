#!/usr/bin/env python3
"""Génère les pages V2 (accueil, pages services, contact) avec header/footer communs.
Usage : python3 bin/build_v2.py   (depuis la racine du site)"""
from pathlib import Path
import json

ROOT = Path(__file__).resolve().parent.parent
EMAIL = "nathan.fritsch.pro@gmail.com"
IG = "https://www.instagram.com/nathanfrt_visuals"
CAL = "https://calendly.com/nathan-fritsch-pro/30min"
SITE = "https://nathanfritsch.fr"

ARROW = '<svg viewBox="0 0 12 12" fill="none" stroke="currentColor" stroke-width="1.6"><path d="M1 11 11 1M4 1h7v7"/></svg>'
ARR_R = '<svg viewBox="0 0 12 12" fill="none" stroke="currentColor" stroke-width="1.6"><path d="M1 6h10M7 2l4 4-4 4"/></svg>'
CHEV = '<svg class="chev" viewBox="0 0 10 10" fill="none" stroke="currentColor" stroke-width="1.4"><path d="m2 3.5 3 3 3-3"/></svg>'
PLUS = '<svg viewBox="0 0 12 12" fill="none" stroke="currentColor" stroke-width="1.6"><path d="M6 1v10M1 6h10"/></svg>'
MAIL = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6"><rect x="3" y="5" width="18" height="14" rx="2"/><path d="m3 7 9 6 9-6"/></svg>'

SERVICES = [
    dict(slug="entreprises", cat="evenement", nav="Entreprises et marques", short="Contenus pour votre communication",
         title="Entreprises et marques", kicker="Photo et vidéo corporate",
         h1='Des images qui donnent <em class="it-a">envie</em> de vous choisir.',
         lead="Photos et vidéos pour votre site, vos réseaux et vos clients.",
         hero="assets/img/mahi.jpg",
         gallery=["assets/img/mahi-2.jpg", "assets/img/mahi.jpg", "assets/img/mahi-3.jpg", "assets/img/event.jpg"],
         offers=[("Photos pour votre site et vos réseaux", "Vos lieux, vos produits, vos équipes et vos clients en situation. Un stock d'images cohérent pour communiquer toute l'année."),
                 ("Portraits professionnels", "Dirigeants, équipes, collaborateurs : des portraits naturels qui humanisent votre marque."),
                 ("Film de présentation", "Une vidéo qui raconte votre activité en quelques minutes, pour votre site, vos salons ou vos rendez-vous commerciaux."),
                 ("Formats courts pour les réseaux", "Reels, stories, contenus verticaux : des vidéos rythmées, montées pour être vues."),
                 ("Séminaires et inaugurations", "Vos temps forts d'entreprise couverts en photo et en vidéo, livrés prêts à partager.")],
         why=[("Un seul interlocuteur", "Photo et vidéo réalisées par la même personne, le même jour si besoin. Un style homogène, une organisation simplifiée."),
              ("Pensé pour votre communication", "Je pars de vos usages (site, réseaux, print) pour livrer les bons formats, directement exploitables."),
              ("Discret et efficace", "Je m'intègre à votre activité sans la perturber, pour capter des images vraies.")],
         case=("Le Mahi Mahi", "Base nautique · Lacanau", "Reportage photo et film d'ambiance pour embellir la communication de la base et promouvoir ses excursions sur le lac.", "assets/img/mahi-3.jpg", "portfolio.html?type=photo&cat=evenement"),
         form="entreprise"),
    dict(slug="immobilier", cat="immobilier", nav="Immobilier et conciergeries", short="Valoriser et louer plus vite",
         title="Immobilier et conciergeries", kicker="Photo HDR et vidéo de visite",
         h1='Vos biens méritent mieux qu\'une photo de <em class="it-a">téléphone</em>.',
         lead="Photos HDR et vidéos de visite qui font cliquer sur vos annonces.",
         hero="assets/img/immo.jpg",
         gallery=["assets/img/immo-2.jpg", "assets/img/immo.jpg", "assets/img/immo-3.jpg", "assets/img/immo-4.jpg"],
         offers=[("Photographie HDR", "Des intérieurs lumineux et fidèles, sans fenêtres brûlées ni coins sombres. Chaque pièce sous son meilleur angle."),
                 ("Vidéo de visite", "Un film fluide qui fait vivre le bien et ses volumes, idéal pour les annonces et les réseaux."),
                 ("Annonces Airbnb et Booking", "Pour les conciergeries et locations saisonnières : des photos qui convertissent et se démarquent des annonces voisines."),
                 ("Formats verticaux", "Des vidéos courtes pensées pour Instagram et TikTok, pour donner de la visibilité à vos mandats."),
                 ("Détails et ambiance", "Matériaux, décoration, extérieurs, lumière du soir : les images qui font rêver et déclenchent la visite.")],
         why=[("Des annonces qui sortent du lot", "Sur un portail, la première photo décide du clic. Je la travaille comme une couverture."),
              ("Réactivité", "Je m'adapte à vos agendas de mandats et aux disponibilités des propriétaires et locataires."),
              ("Retouche soignée", "Chaque image est traitée à la main : lignes droites, couleurs justes, lumière naturelle.")],
         case=("Présentation villa", "Vidéo · Vente immobilière", "Film de présentation réalisé pour un agent immobilier afin de l'aider à vendre le bien de son client : volumes, lumière et détails mis en valeur.", "assets/img/immo-3.jpg", "portfolio.html?type=video&cat=immobilier"),
         form="immobilier"),
    dict(slug="sport", cat="sport", nav="Sport", short="Compétitions, clubs, athlètes",
         title="Sport", kicker="Photo et vidéo sportive",
         h1='L\'intensité d\'un geste, <em class="it-a">figée</em> pour de bon.',
         lead="Compétitions, clubs, athlètes. Tous les sports.",
         hero="assets/img/triathlon-2.jpg",
         gallery=["assets/img/lacanau.jpg", "assets/img/sport.jpg", "assets/img/surf.jpg", "assets/img/ski.jpg"],
         offers=[("Couverture de compétition", "Du départ à la remise des prix : action, coulisses, public et podiums sur une ou plusieurs journées."),
                 ("Contenus pour les partenaires", "Des images qui mettent en valeur vos sponsors et vos marques partenaires, livrées aux bons formats."),
                 ("Portraits d'athlètes", "Pour vos réseaux, vos dossiers de sponsoring ou votre presse."),
                 ("Aftermovie et vidéos récap", "Un film rythmé qui fait revivre l'événement et donne envie de revenir l'année suivante."),
                 ("Clubs et associations", "Des images pour vos licenciés, vos réseaux et vos demandes de subventions.")],
         why=[("Au cœur de l'action", "Placement, anticipation, réactivité : je connais le terrain et les temps forts d'une compétition."),
              ("Du volume sans perdre la qualité", "Des centaines d'images triées et retouchées, prêtes pour vos médias."),
              ("Passionné de sport", "Je pratique et j'aime ce que je photographie. Ça se voit dans les images.")],
         case=("Lacanau Pro", "Compétition de surf · Lacanau", "Reportage photo et vidéo sur plusieurs jours de l'un des grands rendez-vous du surf : action dans l'eau, ambiance sur le sable et énergie du public.", "assets/img/lacanau-3.jpg", "portfolio.html?type=photo&cat=sport"),
         form="sport"),
    dict(slug="evenementiel", cat="evenement", nav="Événementiel", short="Soirées, séminaires, célébrations",
         title="Événementiel", kicker="Reportage photo et film d'événement",
         h1='Votre événement se vit une fois. Les <em class="it-a">images</em> restent.',
         lead="Soirées, séminaires, lancements, mariages. Photo et film.",
         hero="assets/img/schoolcup.jpg",
         gallery=["assets/img/event.jpg", "assets/img/schoolcup-2.jpg", "assets/img/triathlon.jpg", "assets/img/mahi-2.jpg"],
         offers=[("Reportage photo", "Ambiance, invités, discours, moments spontanés : toute l'histoire de votre événement, racontée en images."),
                 ("Aftermovie", "Un film court et rythmé pour prolonger l'événement sur vos réseaux et préparer la prochaine édition."),
                 ("Photos express pour les réseaux", "Une sélection d'images livrée rapidement pour publier pendant que l'événement fait encore parler."),
                 ("Mariages et célébrations privées", "Des souvenirs naturels et élégants, sans poses forcées."),
                 ("Événements sportifs et associatifs", "Courses, tournois, rassemblements : l'énergie collective captée du début à la fin.")],
         why=[("Discrétion", "Je me fonds dans l'événement pour capter des instants vrais, sans jamais le perturber."),
              ("Anticipation", "Je prépare le déroulé avec vous pour ne manquer aucun temps fort."),
              ("Photo + vidéo", "Les deux au même endroit, avec le même regard. Un seul contact, un résultat cohérent.")],
         case=("School Cup", "Événement sportif étudiant", "Couverture complète d'une journée de compétitions étudiantes : épreuves, cérémonies, tribunes et instants d'émotion.", "assets/img/schoolcup-2.jpg", "portfolio.html?type=photo&cat=evenement"),
         form="evenement"),
]


SERVICES = [next(x for x in SERVICES if x['slug']==k) for k in ('evenementiel','sport','immobilier','entreprises')]


def head(title, desc, extra_css="", path=""):
    return f"""<!DOCTYPE html>
<html lang="fr">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0, viewport-fit=cover">
<title>{title}</title>
<meta name="description" content="{desc}">
<link rel="canonical" href="{SITE}/{path}">
<meta property="og:type" content="website">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:image" content="{SITE}/assets/img/hero.jpg">
<meta name="theme-color" content="#0D0F10">
<link rel="icon" href="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 64 64'%3E%3Crect width='64' height='64' rx='14' fill='%230D0F10'/%3E%3Ctext x='50%25' y='56%25' text-anchor='middle' dominant-baseline='middle' font-family='Georgia,serif' font-size='34' fill='%23F4F1EC'%3ENF%3C/text%3E%3C/svg%3E">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Fraunces:ital,opsz,wght@0,9..144,300..600;1,9..144,300..600&family=Inter:wght@300;400;500;600&display=swap" rel="stylesheet">
<link rel="stylesheet" href="assets/site.css">
<style>{extra_css}</style>
</head>
"""


def header(active=""):
    svc_dd = "".join(f'<a href="{s["slug"]}.html"><b>{s["nav"]}</b><span>{s["short"]}</span></a>' for s in SERVICES)
    mm_svc = "".join(f'<li><a href="{s["slug"]}.html">{s["nav"]}</a></li>' for i, s in enumerate(SERVICES))
    on = lambda k: ' class="on"' if active == k else ""
    return f"""<header class="hd">
  <a href="index.html" class="hd-logo" aria-label="Nathan Fritsch, accueil"><b>Nathan Fritsch</b><small>Photo · Vidéo · Bordeaux</small></a>
  <div role="navigation" aria-label="Navigation principale">
    <ul class="hd-nav">
      <li><button type="button" aria-haspopup="true">Services {CHEV}</button>
        <div class="hd-dd"><div class="hd-dd-in">{svc_dd}</div></div></li>
      <li><button type="button" aria-haspopup="true">Réalisations {CHEV}</button>
        <div class="hd-dd"><div class="hd-dd-in">
          <a href="portfolio.html?type=photo"><b>Photos</b><span>Reportages et séries</span></a>
          <a href="portfolio.html?type=video"><b>Vidéos</b><span>Films, aftermovies, formats courts</span></a>
        </div></div></li>
      <li><a href="index.html#apropos"{on('about')}>À propos</a></li>
      <li><a href="contact.html"{on('contact')}>Contact</a></li>
    </ul>
  </div>
  <div class="hd-right">
    <a href="contact.html" class="btn">Demander un devis <span class="ar">{ARROW}</span></a>
    <button class="hd-burger" type="button" aria-label="Menu" aria-expanded="false"><i></i><i></i></button>
  </div>
</header>
<div class="mm" role="dialog" aria-label="Menu">
  <ul class="mm-links">
    <li><a href="index.html">Accueil</a></li>
    {mm_svc}
    <li><a href="portfolio.html?type=photo">Réalisations</a></li>
    <li><a href="contact.html">Contact</a></li>
  </ul>
  <div class="mm-foot">
    <a href="contact.html" class="btn light">Demander un devis <span class="ar">{ARROW}</span></a>
    <p><a href="mailto:{EMAIL}">{EMAIL}</a> · <a href="{IG}" target="_blank" rel="noopener">Instagram</a></p>
  </div>
</div>
<div class="mcta">
  <a href="contact.html" class="btn no-mag">Demander un devis <span class="ar">{ARROW}</span></a>
  <a href="mailto:{EMAIL}" class="btn tel no-mag" aria-label="Envoyer un email">{MAIL}</a>
</div>
"""


def footer():
    svc = "".join(f'<li><a href="{s["slug"]}.html">{s["nav"]}</a></li>' for s in SERVICES)
    return f"""<footer class="fx">
  <div class="wrap">
    <div class="fx-top">
      <div class="fx-cta">
        <h3>Un projet en tête ?<br><em>Parlons-en.</em></h3>
        <a href="contact.html" class="btn light">Demander un devis <span class="ar">{ARROW}</span></a>
      </div>
      <div><h4>Services</h4><ul>{svc}</ul></div>
      <div><h4>Réalisations</h4><ul>
        <li><a href="portfolio.html?type=photo">Photos</a></li>
        <li><a href="portfolio.html?type=video">Vidéos</a></li>
        <li><a href="index.html#apropos">À propos</a></li>
      </ul></div>
      <div><h4>Contact</h4><ul>
        <li><a href="mailto:{EMAIL}">{EMAIL}</a></li>
        <li><a href="{CAL}" target="_blank" rel="noopener">Réserver un appel</a></li>
        <li><a href="{IG}" target="_blank" rel="noopener">Instagram</a></li>
        <li><a href="contact.html">Bordeaux · France entière</a></li>
      </ul></div>
    </div>
    <div class="fx-big" aria-hidden="true">Nathan Fritsch</div>
    <div class="fx-bot">
      <span>© <span data-year>2026</span> Nathan Fritsch · Photographe et vidéaste à Bordeaux</span>
      <span><a href="mentions-legales.html">Mentions légales</a> · <a href="confidentialite.html">Confidentialité</a></span>
    </div>
  </div>
</footer>
"""


SCRIPTS = """<script src="assets/site.js" defer></script>
"""


def cta_end(img, title='Un projet ?<br><em class="it-a">Parlons-en.</em>', text="Devis gratuit. Réponse sous 24 h.", q=""):
    return f"""<section class="cta-end">
  <div class="cta-end-bg" style="background-image:url('{img}')" data-px=".12"></div>
  <div class="wrap">
    <h2 class="d1 split">{title}</h2>
    <p data-rv style="--dl:.2s">{text}</p>
    <div class="cta-end-actions" data-rv style="--dl:.3s">
      <a href="contact.html{q}" class="btn light big">Demander un devis <span class="ar">{ARROW}</span></a>
      <a href="{CAL}" target="_blank" rel="noopener" class="btn ghost-l big">Réserver un appel <span class="ar">{ARROW}</span></a>
    </div>
    <div class="cta-end-meta" data-rv style="--dl:.4s"><a href="mailto:{EMAIL}">{EMAIL}</a></div>
  </div>
</section>
"""


# ═════════════════════════════ INDEX ═════════════════════════════
INDEX_CSS = """
.hero{position:relative;height:100vh;height:100svh;min-height:640px;overflow:hidden;background:var(--ink);color:#fff;}
.hero-bg{position:absolute;inset:-6% 0;background:url('assets/img/hero.jpg') center 35%/cover no-repeat;transform:scale(1.12);transition:transform 2.6s var(--ease);will-change:transform;}
body.ready .hero-bg{transform:scale(1.02);}
.hero::after{content:'';position:absolute;inset:0;background:linear-gradient(180deg,rgba(13,15,16,.55) 0%,rgba(13,15,16,.18) 30%,rgba(13,15,16,.45) 58%,rgba(13,15,16,.92) 100%),linear-gradient(90deg,rgba(13,15,16,.35),rgba(13,15,16,0) 60%);}
.hero-in{position:relative;z-index:2;height:100%;display:flex;flex-direction:column;justify-content:flex-end;padding-bottom:clamp(2rem,5vh,3.5rem);}
.hero-grid{display:grid;grid-template-columns:1.35fr 1fr;gap:4rem;align-items:end;}
.hero .eyebrow{color:var(--a-xl);margin-bottom:1.6rem;}
.hero h1{max-width:11ch;}
.hero h1 .sm{display:block;font-size:.34em;font-style:normal;font-weight:450;letter-spacing:-.01em;color:var(--a-l);margin-top:.55em;line-height:1.1;}
.hero-side{display:flex;flex-direction:column;gap:2rem;padding-bottom:.6rem;}
.hero-side p{color:rgba(255,255,255,.78);font-weight:300;font-size:clamp(1rem,1.2vw,1.12rem);line-height:1.75;max-width:30em;}
.hero-actions{display:flex;flex-wrap:wrap;align-items:center;gap:1.4rem 2rem;}
.hero-bar{display:flex;justify-content:space-between;align-items:center;gap:2rem;margin-top:clamp(2.2rem,5vh,3.6rem);padding-top:1.5rem;border-top:1px solid rgba(255,255,255,.18);}
.hero-tags{display:flex;flex-wrap:wrap;gap:.6rem;}
.hero-tags a{font-size:.7rem;letter-spacing:.14em;text-transform:uppercase;text-decoration:none;padding:.55rem 1rem;border:1px solid rgba(255,255,255,.25);border-radius:100px;color:rgba(255,255,255,.88);transition:background .4s,color .4s,border-color .4s;}
.hero-tags a:hover{background:#fff;color:var(--ink);border-color:#fff;}
.hero-scroll{display:flex;align-items:center;gap:.9rem;font-size:.66rem;letter-spacing:.26em;text-transform:uppercase;color:rgba(255,255,255,.7);white-space:nowrap;}
.hero-scroll i{position:relative;width:1px;height:44px;background:rgba(255,255,255,.2);overflow:hidden;}
.hero-scroll i::after{content:'';position:absolute;left:0;top:-50%;width:1px;height:50%;background:#fff;animation:drip 2s var(--ease-io) infinite;}
@keyframes drip{to{top:100%;}}
.hero [data-hold] [data-rv],.hero [data-hold] .split{transition-delay:calc(var(--dl,0s) + .15s);}

/* manifesto */
.mani{padding:clamp(5rem,10vw,9rem) 0 clamp(4rem,7vw,6rem);}
.mani-txt{font-family:var(--serif);font-weight:450;font-size:clamp(2.6rem,7vw,7.4rem);line-height:1;letter-spacing:-.03em;}
.mani-txt .mw{opacity:.14;transition:opacity .35s linear;}
.mani-txt .mw.lit{opacity:1;}
.mani-txt em{font-style:normal;color:var(--a);}
.mani-row{display:grid;grid-template-columns:repeat(3,1fr);gap:2rem;margin-top:clamp(3.5rem,7vw,6rem);padding-top:2.2rem;border-top:1px solid var(--line);}
.mani-row div{display:flex;flex-direction:column;gap:.5rem;}
.mani-row b{font-family:var(--serif);font-weight:450;font-size:clamp(1.3rem,1.8vw,1.7rem);}
.mani-row span{color:var(--mute);font-weight:300;font-size:.95rem;line-height:1.65;}
.mani-row small{font-size:.66rem;letter-spacing:.2em;color:var(--a);font-weight:600;}

/* scroll expansion (kept) */
#se-hero{position:relative;height:170vh;background:var(--paper);}
.se-stage{position:sticky;top:0;height:100vh;height:100svh;display:flex;align-items:center;justify-content:center;overflow:hidden;}
.se-frame{position:relative;z-index:1;width:46vw;height:64vh;border-radius:22px;overflow:hidden;will-change:width,height;}
.se-media{position:absolute;inset:0;width:100%;height:100%;object-fit:cover;}
.se-shade{position:absolute;inset:0;background:linear-gradient(to top,rgba(13,15,16,.8) 0%,rgba(13,15,16,.25) 45%,rgba(13,15,16,.45) 100%);}
.se-head{position:absolute;inset:0;z-index:2;display:flex;flex-direction:column;align-items:center;justify-content:center;text-align:center;color:#fff;padding:2rem;}
.se-tag{font-size:.7rem;font-weight:500;letter-spacing:.34em;text-transform:uppercase;color:var(--a-xl);margin-bottom:1.2rem;}
.se-title{font-family:var(--serif);font-weight:450;font-size:64px;line-height:1;letter-spacing:-.025em;white-space:nowrap;}
.se-title em{font-style:normal;font-weight:450;color:var(--a-l);}
.se-sub{margin-top:1.6rem;font-size:clamp(.66rem,1.1vw,.84rem);letter-spacing:.26em;text-transform:uppercase;opacity:0;padding:.65rem 1.4rem;border:1px solid rgba(255,255,255,.3);border-radius:40px;background:rgba(255,255,255,.07);backdrop-filter:blur(6px);}
.se-scroll-cue{position:absolute;bottom:2rem;left:50%;transform:translateX(-50%);display:flex;flex-direction:column;align-items:center;gap:.5rem;color:rgba(255,255,255,.88);z-index:5;animation:scB 2.2s ease infinite;transition:opacity .4s;}
.se-scroll-cue span{font-size:.62rem;letter-spacing:.3em;text-transform:uppercase;font-weight:500;}
.se-scroll-cue svg{width:20px;height:20px;}
@keyframes scB{0%,100%{transform:translate(-50%,0);}50%{transform:translate(-50%,8px);}}

/* for who: accordion panels */
.who-head{display:flex;justify-content:space-between;align-items:flex-end;gap:3rem;margin-bottom:clamp(2.5rem,5vw,4rem);}
.who-head .lead{max-width:26em;}
.who{display:flex;gap:10px;height:min(78vh,760px);min-height:520px;}
.who-p{position:relative;flex:1;overflow:hidden;border-radius:18px;text-decoration:none;color:#fff;background:var(--ink);transition:flex 1s var(--ease);isolation:isolate;}
.who:hover .who-p{flex:.7;}
.who .who-p:hover{flex:2.6;}
.who-p img{position:absolute;inset:0;width:100%;height:100%;object-fit:cover;transform:scale(1.06);transition:transform 1.4s var(--ease),filter 1s;filter:brightness(.72) saturate(.9);z-index:-1;}
.who-p:hover img{transform:scale(1);filter:brightness(.6) saturate(1);}
.who-p::after{content:'';position:absolute;inset:0;z-index:-1;background:linear-gradient(0deg,rgba(13,15,16,.88) 0%,rgba(13,15,16,0) 60%);}
.who-n{position:absolute;top:1.4rem;left:1.5rem;font-size:.7rem;letter-spacing:.2em;font-weight:600;color:rgba(255,255,255,.75);}
.who-b{position:absolute;left:0;right:0;bottom:0;padding:1.8rem 1.6rem;display:flex;flex-direction:column;gap:.9rem;}
.who-t{font-family:var(--serif);font-weight:400;font-size:clamp(1.5rem,2.2vw,2.3rem);line-height:1.02;letter-spacing:-.015em;}
.who-d{font-size:.95rem;font-weight:300;line-height:1.6;color:rgba(255,255,255,.8);max-width:28em;max-height:0;opacity:0;overflow:hidden;transition:max-height .9s var(--ease),opacity .6s;}
.who-p:hover .who-d{max-height:8em;opacity:1;transition-delay:.15s;}
.who-go{display:inline-flex;align-items:center;gap:.6rem;font-size:.7rem;letter-spacing:.18em;text-transform:uppercase;font-weight:600;}
.who-go span{width:34px;height:34px;border-radius:50%;background:#fff;color:var(--ink);display:grid;place-items:center;transition:transform .5s var(--ease);}
.who-go svg{width:11px;height:11px;}
.who-p:hover .who-go span{transform:rotate(-45deg);}

/* work: pinned horizontal */
.work{background:var(--ink);color:var(--bone);position:relative;}
.work-pin{position:sticky;top:0;height:100vh;height:100svh;overflow:hidden;display:flex;flex-direction:column;justify-content:center;gap:clamp(1.5rem,4vh,3rem);}
.work-top{display:flex;justify-content:space-between;align-items:flex-end;gap:2rem;}
.work-count{font-family:var(--serif);font-size:1.1rem;color:var(--mute-d);}
.work-count b{color:var(--bone);font-weight:400;}
.work-track{display:flex;gap:clamp(1rem,2vw,2rem);padding:0 var(--gut);will-change:transform;}
.case{flex:none;width:clamp(300px,36vw,560px);text-decoration:none;color:inherit;display:flex;flex-direction:column;gap:1.2rem;}
.case.wide{width:clamp(340px,52vw,820px);}
.case-img{position:relative;overflow:hidden;border-radius:14px;height:min(58vh,560px);background:var(--ink-3);}
.case-img img{width:100%;height:100%;object-fit:cover;transform:scale(1.04);transition:transform 1.4s var(--ease);}
.case:hover .case-img img{transform:scale(1.1);}
.case-tag{position:absolute;top:1rem;left:1rem;font-size:.64rem;letter-spacing:.18em;text-transform:uppercase;background:rgba(13,15,16,.55);backdrop-filter:blur(8px);padding:.5rem .8rem;border-radius:100px;color:#fff;}
.case-meta{display:flex;justify-content:space-between;align-items:flex-start;gap:1.5rem;}
.case h3{font-family:var(--serif);font-weight:400;font-size:clamp(1.4rem,2vw,1.9rem);letter-spacing:-.01em;line-height:1.1;}
.case p{font-size:.9rem;color:var(--mute-d);font-weight:300;margin-top:.35rem;max-width:30em;line-height:1.6;}
.case-ar{flex:none;width:44px;height:44px;border-radius:50%;border:1px solid var(--line-d);display:grid;place-items:center;transition:background .4s,color .4s,transform .5s var(--ease);}
.case-ar svg{width:12px;height:12px;}
.case:hover .case-ar{background:var(--bone);color:var(--ink);transform:rotate(-45deg);}
.case-all{flex:none;width:clamp(260px,26vw,380px);height:min(58vh,560px);border-radius:14px;border:1px solid var(--line-d);display:flex;flex-direction:column;justify-content:space-between;padding:2rem;text-decoration:none;color:var(--bone);transition:background .5s,color .5s;}
.case-all:hover{background:var(--bone);color:var(--ink);}
.case-all b{font-family:var(--serif);font-weight:450;font-size:clamp(1.8rem,2.6vw,2.6rem);line-height:1.05;letter-spacing:-.015em;}
.case-all b em{font-style:normal;color:var(--a-l);}
.case-all:hover b em{color:var(--a);}
.case-all span{display:flex;gap:1rem;flex-direction:column;font-size:.72rem;letter-spacing:.16em;text-transform:uppercase;}
.work-prog{height:1px;background:var(--line-d);position:relative;}
.work-prog i{position:absolute;left:0;top:0;bottom:0;width:100%;background:var(--a-l);transform-origin:left;transform:scaleX(0);}

/* method */
.method{display:grid;grid-template-columns:1fr 1.25fr;gap:clamp(3rem,8vw,8rem);}
.method-l{position:sticky;top:18vh;align-self:start;display:flex;flex-direction:column;gap:1.6rem;}
.steps{list-style:none;counter-reset:s;}
.step{display:grid;grid-template-columns:auto 1fr;gap:2rem;padding:2.6rem 0;border-top:1px solid var(--line);}
.step:last-child{border-bottom:1px solid var(--line);}
.step-n{font-family:var(--serif);font-style:normal;font-weight:450;font-size:clamp(3rem,5vw,4.6rem);line-height:.8;color:var(--a);min-width:1.6em;}
.step h3{font-family:var(--serif);font-weight:420;font-size:clamp(1.4rem,2vw,1.9rem);margin-bottom:.8rem;letter-spacing:-.01em;}
.step p{color:var(--mute);font-weight:300;line-height:1.8;}
.step ul{list-style:none;display:flex;flex-wrap:wrap;gap:.5rem;margin-top:1.1rem;}
.step li{font-size:.7rem;letter-spacing:.1em;text-transform:uppercase;padding:.45rem .8rem;border:1px solid var(--line);border-radius:100px;color:var(--mute);}

/* about */
.about{display:grid;grid-template-columns:.9fr 1.1fr;gap:clamp(3rem,7vw,7rem);align-items:center;}
.about-img{position:relative;border-radius:16px;overflow:hidden;aspect-ratio:3/4;}
.about-img img{width:100%;height:100%;object-fit:cover;}
.about-badge{position:absolute;left:1.2rem;bottom:1.2rem;background:rgba(13,15,16,.55);backdrop-filter:blur(10px);color:#fff;padding:.9rem 1.1rem;border-radius:12px;font-size:.8rem;line-height:1.4;}
.about-badge b{display:block;font-family:var(--serif);font-weight:420;font-size:1.05rem;}
.about-txt{display:flex;flex-direction:column;gap:1.7rem;}
.about-txt p{color:var(--mute-d);font-weight:300;line-height:1.85;font-size:1.02rem;max-width:36em;}
.about-txt p strong{color:var(--bone);font-weight:500;}
.about-q{font-family:var(--serif);font-style:normal;font-weight:450;font-size:clamp(1.4rem,2.2vw,2rem);line-height:1.3;color:var(--bone);padding-left:1.4rem;border-left:1px solid var(--a-l);}
.about-sig{display:flex;align-items:center;gap:2rem;flex-wrap:wrap;margin-top:.6rem;}
.about-sig span{font-family:var(--serif);font-style:normal;font-size:1.5rem;color:var(--a-l);}

/* faq */
.faq-wrap{display:grid;grid-template-columns:1fr 1.6fr;gap:clamp(3rem,7vw,7rem);}
.faq-l{display:flex;flex-direction:column;gap:1.6rem;align-self:start;position:sticky;top:18vh;}

@media (max-width:1080px){
  .hero-grid{grid-template-columns:1fr;gap:2rem;}
  .hero-bar{flex-direction:column;align-items:flex-start;}
  .hero-scroll{display:none;}
  .who-head{flex-direction:column;align-items:flex-start;gap:1.5rem;}
  .who{flex-direction:column;height:auto;min-height:0;}
  .who-p,.who:hover .who-p,.who .who-p:hover{flex:none;height:62vw;min-height:320px;max-height:480px;}
  .who-d{max-height:none;opacity:1;}
  .method,.faq-wrap{grid-template-columns:1fr;}
  .method-l,.faq-l{position:static;}
  .about{grid-template-columns:1fr;}
  .about-img{max-width:520px;}
  .work{height:auto!important;}
  .work-pin{position:relative;height:auto;padding:clamp(5rem,10vw,7rem) 0;}
  .work-track{transform:none!important;overflow-x:auto;scroll-snap-type:x mandatory;scroll-padding-left:var(--gut);padding-bottom:1rem;scrollbar-width:none;}
  .work-track::-webkit-scrollbar{display:none;}
  .case,.case.wide,.case-all{scroll-snap-align:start;width:78vw;}
  .case-img,.case-all{height:96vw;max-height:520px;}
  .work-prog{display:none;}
}
@media (max-width:768px){
  #se-hero{height:150vh;}
  .mani-row{grid-template-columns:1fr;gap:1.6rem;}
  .hero h1{font-size:clamp(2.7rem,12.5vw,4rem);}
  .hero h1 .sm{font-size:.44em;}
  .hero-side{gap:1.5rem;}
  .step{grid-template-columns:1fr;gap:1rem;}
}
"""

WHO = [
    ("evenementiel", "Événementiel", "Vos moments forts, pour toujours.", "assets/img/event.jpg"),
    ("sport", "Sport", "L'intensité, au plus près de l'action.", "assets/img/sport.jpg"),
    ("immobilier", "Immobilier<br>et conciergeries", "Vendez et louez plus vite.", "assets/img/immo.jpg"),
    ("entreprises", "Entreprises<br>et marques", "Des images qui vendent votre marque.", "assets/img/mahi.jpg"),
]
CASES = [
    ("School Cup", "Événement étudiant", "Une journée de compétitions, de cérémonies et d'émotion, du premier au dernier instant.", "assets/img/schoolcup.jpg", "portfolio.html?type=photo&cat=evenement", ""),
    ("Lacanau Pro", "Surf · Compétition", "Plusieurs jours au cœur d'un grand rendez-vous du surf, en photo et en vidéo.", "assets/img/lacanau.jpg", "portfolio.html?type=photo&cat=sport", ""),
    ("Triathlon de Lacanau", "Sport · 2 jours", "Départs, transitions, arrivées : toute la course documentée, jusque sur la moto photo.", "assets/img/triathlon-2.jpg", "portfolio.html?type=photo&cat=sport", "wide"),
    ("Villa à vendre", "Immobilier · Vidéo", "Un film de présentation pour aider un agent immobilier à vendre le bien de son client.", "assets/img/immo-2.jpg", "portfolio.html?type=video&cat=immobilier", "wide"),
    ("Le Mahi Mahi", "Entreprise · Communication", "Des images pour embellir la communication d'une base nautique et vendre ses excursions.", "assets/img/mahi.jpg", "portfolio.html?type=photo&cat=evenement", "wide"),
]
FAQ = [
    ("Où intervenez-vous ?", "Je suis basé à Bordeaux et je me déplace partout en France, ainsi qu'à l'étranger. Les éventuels frais de déplacement sont indiqués clairement dans le devis."),
    ("Photo, vidéo ou les deux ?", "Les deux. Je peux réaliser photos et vidéos sur la même intervention : un seul interlocuteur, une seule organisation et un rendu cohérent entre vos images et vos films."),
    ("Combien coûte une prestation ?", "Chaque projet est différent : durée, volume d'images, montage vidéo, déplacement. Après un court échange, je vous envoie un devis détaillé, gratuit et sans engagement."),
    ("Quand est-ce que je reçois mes images ?", "Le délai de livraison est fixé ensemble avant le projet, selon le volume et vos échéances. Si vous avez besoin d'une sélection rapide pour vos réseaux, on le prévoit dès le départ."),
    ("Puis-je utiliser les images pour ma communication ?", "Oui. Les droits d'utilisation (site, réseaux sociaux, print, publicité) sont précisés dans le devis selon vos besoins, pour que vous puissiez les exploiter en toute sérénité."),
    ("Comment se passe la prise de contact ?", "Vous remplissez le formulaire ou vous réservez un appel de 30 minutes. On parle de votre projet, de vos objectifs et de vos contraintes, puis je vous fais une proposition."),
]


def index():
    who = "".join(f"""<a href="{s}.html" class="who-p" data-cursor="Découvrir" data-rv style="--dl:{i*.08:.2f}s">
        <img src="{img}" alt="" loading="lazy" decoding="async">
        <div class="who-b"><h3 class="who-t">{t}</h3><p class="who-d">{d}</p><span class="who-go"><span>{ARROW}</span>Découvrir</span></div>
      </a>""" for i, (s, t, d, img) in enumerate(WHO))
    cases = "".join(f"""<a href="{href}" class="case {cls}" data-cursor="Voir">
          <div class="case-img"><img src="{img}" alt="{t}" loading="lazy" decoding="async"><span class="case-tag">{tag}</span></div>
          <div class="case-meta"><div><h3>{t}</h3></div><span class="case-ar">{ARROW}</span></div>
        </a>""" for (t, tag, d, img, href, cls) in CASES)
    faq = "".join(f'<details><summary>{q}<span class="pl">{PLUS}</span></summary><div class="ans">{a}</div></details>' for q, a in FAQ)
    faq_ld = json.dumps({"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in FAQ]}, ensure_ascii=False)
    biz_ld = json.dumps({"@context": "https://schema.org", "@type": "ProfessionalService", "name": "Nathan Fritsch, photographe et vidéaste", "image": f"{SITE}/assets/img/hero.jpg", "url": SITE, "email": EMAIL, "areaServed": "France", "address": {"@type": "PostalAddress", "addressLocality": "Bordeaux", "addressCountry": "FR"}, "sameAs": [IG]}, ensure_ascii=False)
    mani = "Vous avez le projet.<br><em>Je crée les images.</em>"

    return head("Nathan Fritsch · Photographe et vidéaste à Bordeaux",
                "Photographe et vidéaste professionnel à Bordeaux. Photo et vidéo pour les entreprises, l'immobilier, le sport et l'événementiel, partout en France. Devis gratuit.",
                INDEX_CSS) + f"""<body class="dark-top">
<div class="intro" aria-hidden="true"><div class="intro-in">
  <div class="intro-name"><span>Nathan Fritsch</span></div>
  <div class="intro-bar"></div>
  <div class="intro-sub">Photographe et vidéaste</div>
</div></div>
{header()}
<main>
<section class="hero">
  <div class="hero-bg" data-px="-.18" role="img" aria-label="Triathlète en pleine course à Lacanau"></div>
  <div class="wrap hero-in">
    <div class="hero-grid">
      <div>
        <span class="eyebrow" data-rv>Bordeaux · Partout en France</span>
        <h1 class="d1 split">Photographe et vidéaste <span class="sm">L'instant, l'émotion, l'image.</span></h1>
      </div>
      <div class="hero-side">
        <p data-rv style="--dl:.35s">Événements, sport, immobilier, marques.<br>Des images qui font la différence.</p>
        <div class="hero-actions" data-rv style="--dl:.5s">
          <a href="contact.html" class="btn light big">Demander un devis <span class="ar">{ARROW}</span></a>
          <a href="#realisations" class="link" style="color:#fff">Voir les réalisations {ARR_R}</a>
        </div>
      </div>
    </div>
    <div class="hero-bar" data-rv style="--dl:.65s">
      <div class="hero-tags">
        <a href="evenementiel.html">Événementiel</a><a href="sport.html">Sport</a><a href="immobilier.html">Immobilier</a><a href="entreprises.html">Entreprises</a>
      </div>
      <div class="hero-scroll"><i></i>Défiler</div>
    </div>
  </div>
</section>

<div class="marq" aria-label="Quelques projets réalisés"><div class="marq-t">{"".join(f'<span>{x}<i></i></span>' for x in ["Lacanau Pro", "Triathlon de Lacanau", "School Cup", "Le Mahi Mahi", "Compétition de golf", "Photographie immobilière", "Ski", "Surf à Lacanau"]*2)}</div></div>

<section class="mani">
  <div class="wrap">
    <p class="mani-txt" id="mani">{mani}</p>
    <div class="mani-row">
      <div data-rv><b>Photo et vidéo</b><span>Un seul interlocuteur</span></div>
      <div data-rv style="--dl:.1s"><b>Réponse sous 24 h</b><span>Devis gratuit</span></div>
      <div data-rv style="--dl:.2s"><b>Partout en France</b><span>Basé à Bordeaux</span></div>
    </div>
  </div>
</section>

<section id="se-hero" aria-label="Photo et vidéo">
  <div class="se-stage">
    <div class="se-frame" id="seFrame">
      <img class="se-media" src="assets/img/triathlon-2.jpg" alt="Triathlon de Lacanau, départ natation">
      <div class="se-shade"></div>
      <div class="se-head">
        <span class="se-tag">Deux savoir-faire, un seul regard</span>
        <h2 class="se-title" id="seTitle">Photo <em>et</em> Vidéo</h2>
        <span class="se-sub">Événementiel · Sport · Immobilier · Entreprises</span>
      </div>
      <div class="se-scroll-cue" id="seCue">
        <span>Défiler pour découvrir</span>
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M12 5v14"/><path d="M6 13l6 6 6-6"/></svg>
      </div>
    </div>
  </div>
</section>

<section class="sec" id="services" style="padding-top:clamp(3rem,6vw,5rem)">
  <div class="wrap">
    <div class="who-head">
      <h2 class="d2 split">Quel est <em class="it-a">votre projet ?</em></h2>
    </div>
    <div class="who">{who}</div>
  </div>
</section>

<section class="work" id="realisations">
  <div class="work-pin">
    <div class="wrap work-top">
      <h2 class="d2 split">Derniers <em class="it-a">projets</em></h2>
      <div class="work-count" data-rv><b id="wcN">01</b> / 0{len(CASES)}</div>
    </div>
    <div class="work-track" id="wTrack">
      {cases}
      <a href="portfolio.html?type=photo" class="case-all" data-cursor="Explorer">
        <b>Tout le <em>portfolio</em></b>
        <span><span>Photos et vidéos</span><span class="case-ar">{ARROW}</span></span>
      </a>
    </div>
    <div class="wrap"><div class="work-prog"><i id="wProg"></i></div></div>
  </div>
</section>

<section class="sec bone">
  <div class="wrap method">
    <div class="method-l">
      <h2 class="d2 split">3 étapes. <em class="it-a">C'est tout.</em></h2>
      <div data-rv><a href="contact.html" class="btn">Démarrer mon projet <span class="ar">{ARROW}</span></a></div>
    </div>
    <ol class="steps">
      <li class="step" data-rv><span class="step-n">01</span><div><h3>On échange</h3><p>Appel gratuit, devis clair.</p></div></li>
      <li class="step" data-rv><span class="step-n">02</span><div><h3>Je réalise</h3><p>Sur place, discret, efficace.</p></div></li>
      <li class="step" data-rv><span class="step-n">03</span><div><h3>Je livre</h3><p>Prêt pour le web, les réseaux et l'impression.</p></div></li>
    </ol>
  </div>
</section>

<section class="sec on-dark" id="apropos">
  <div class="wrap about">
    <div class="about-img imgrv" data-cursor="Nathan">
      <img src="assets/img/about.jpg" alt="Portrait de Nathan Fritsch, photographe et vidéaste à Bordeaux" loading="lazy">
      <div class="about-badge"><b>Nathan Fritsch</b>Photographe et vidéaste · Bordeaux</div>
    </div>
    <div class="about-txt">
      <h2 class="d2 split">Enchanté, <em class="it-a">moi c'est Nathan.</em></h2>
      <p data-rv>Jeune photographe et vidéaste basé à Bordeaux — disponible partout en France et à l'étranger pour accompagner mes clients.</p>
      <p data-rv>Tout a commencé il y a trois ans, avec le premier appareil de mon père — et depuis, l'image ne m'a plus lâché. Je me consacre surtout au sport et à l'événementiel, sans oublier l'immobilier : des univers où je cherche à saisir <strong>l'intensité d'un geste et l'émotion d'un instant</strong>.</p>
      <p data-rv>Ce qui me guide, c'est le regard — cette façon de voir et de raconter qui rend chaque image unique. J'avance avec une idée simple : <strong>toujours faire de son mieux, même quand personne ne regarde</strong>.</p>
      <p class="about-q" data-rv>Figez l'instant, capturez l'émotion.</p>
      <div class="about-sig" data-rv><a href="contact.html" class="btn light">Travaillons ensemble <span class="ar">{ARROW}</span></a></div>
    </div>
  </div>
</section>

{cta_end("assets/img/sunset.jpg")}
</main>
{footer()}
<script type="application/ld+json">{biz_ld}</script>
{SCRIPTS}<script src="assets/home.js" defer></script>
</body>
</html>
"""


# ═════════════════════════════ SERVICE PAGES ═════════════════════════════
SVC_CSS = """
.sh{position:relative;min-height:100vh;min-height:100svh;display:flex;align-items:flex-end;color:#fff;overflow:hidden;background:var(--ink);}
.sh-bg{position:absolute;inset:-8% 0;background-size:cover;background-position:center;transform:scale(1.1);transition:transform 2.4s var(--ease);}
body.ready .sh-bg{transform:scale(1);}
.sh::after{content:'';position:absolute;inset:0;background:linear-gradient(180deg,rgba(13,15,16,.55) 0%,rgba(13,15,16,.25) 30%,rgba(13,15,16,.7) 62%,rgba(13,15,16,.92) 100%),linear-gradient(90deg,rgba(13,15,16,.45),rgba(13,15,16,0) 70%);}
.sh .wrap{position:relative;z-index:2;padding-bottom:clamp(2.5rem,7vh,5rem);padding-top:9rem;}
.crumb{display:flex;gap:.7rem;font-size:.7rem;letter-spacing:.16em;text-transform:uppercase;color:rgba(255,255,255,.7);margin-bottom:2rem;}
.crumb a{text-decoration:none;color:#fff;}
.sh h1{max-width:14ch;margin:1.4rem 0 2rem;}
.sh-row{display:flex;justify-content:space-between;align-items:flex-end;gap:3rem;flex-wrap:wrap;}
.sh-row p{max-width:34em;color:rgba(255,255,255,.8);font-weight:300;font-size:1.08rem;line-height:1.75;}
.offers{display:grid;grid-template-columns:1fr 1.5fr;gap:clamp(3rem,7vw,7rem);}
.offers-l{position:sticky;top:18vh;align-self:start;display:flex;flex-direction:column;gap:1.5rem;}
.offer{display:block;padding:1.6rem 0;border-top:1px solid var(--line);transition:padding .5s var(--ease);}
.offer:last-child{border-bottom:1px solid var(--line);}
.offer:hover{padding-left:.8rem;}
.offer span{font-size:.72rem;font-weight:600;letter-spacing:.14em;color:var(--a);padding-top:.5rem;}
.offer h3{font-family:var(--serif);font-weight:420;font-size:clamp(1.35rem,2vw,1.8rem);letter-spacing:-.01em;margin-bottom:.6rem;}
.offer p{color:var(--mute);font-weight:300;line-height:1.75;max-width:36em;}
.gal{display:grid;grid-template-columns:1.2fr .8fr;grid-template-rows:auto auto;gap:12px;}
.gal figure{position:relative;overflow:hidden;border-radius:14px;background:var(--bone-2);}
.gal img{width:100%;height:100%;object-fit:cover;}
.gal figure:nth-child(1){grid-row:span 2;aspect-ratio:auto;min-height:100%;}
.gal figure:nth-child(2),.gal figure:nth-child(3){aspect-ratio:4/3;}
.gal figure:nth-child(4){grid-column:1/-1;aspect-ratio:21/8;}
.why{display:grid;grid-template-columns:repeat(3,1fr);gap:1.2rem;margin-top:clamp(3rem,6vw,5rem);}
.why div{padding:2.2rem 2rem;border:1px solid var(--line-d);border-radius:16px;display:flex;flex-direction:column;gap:1rem;transition:background .5s,border-color .5s;}
.why div:hover{background:var(--ink-2);border-color:rgba(156,195,210,.35);}
.why b{font-family:var(--serif);font-weight:420;font-size:1.4rem;letter-spacing:-.01em;}
.why p{color:var(--mute-d);font-weight:300;line-height:1.75;}
.why small{font-size:.7rem;font-weight:600;letter-spacing:.16em;color:var(--a-l);}
.feat{display:grid;grid-template-columns:1.1fr 1fr;gap:clamp(2.5rem,6vw,6rem);align-items:center;}
.feat-img{border-radius:16px;overflow:hidden;aspect-ratio:4/5;}
.feat-img img{width:100%;height:100%;object-fit:cover;}
.feat-txt{display:flex;flex-direction:column;gap:1.4rem;}
.feat-txt .tag{font-size:.72rem;letter-spacing:.16em;text-transform:uppercase;color:var(--mute);}
.others{display:grid;grid-template-columns:repeat(3,1fr);gap:12px;}
.other{position:relative;border-radius:14px;overflow:hidden;aspect-ratio:4/3;color:#fff;text-decoration:none;display:flex;align-items:flex-end;padding:1.5rem;isolation:isolate;}
.other img{position:absolute;inset:0;width:100%;height:100%;object-fit:cover;z-index:-2;transition:transform 1.2s var(--ease);}
.other::after{content:'';position:absolute;inset:0;z-index:-1;background:linear-gradient(0deg,rgba(13,15,16,.8),rgba(13,15,16,0) 65%);}
.other:hover img{transform:scale(1.07);}
.other b{font-family:var(--serif);font-weight:400;font-size:1.5rem;display:flex;align-items:center;justify-content:space-between;width:100%;gap:1rem;}
.other b svg{width:12px;height:12px;}
@media (max-width:1080px){
  .offers,.feat{grid-template-columns:1fr;}
  .offers-l{position:static;}
  .why{grid-template-columns:1fr;}
  .others{grid-template-columns:1fr;}
  .gal{grid-template-columns:1fr 1fr;}
  .gal figure:nth-child(1){grid-column:1/-1;grid-row:auto;aspect-ratio:4/3;}
  .gal figure:nth-child(4){aspect-ratio:4/3;}
}
@media (max-width:640px){.offer{grid-template-columns:1fr;gap:.4rem;}}
"""


def service(s):
    offers = "".join(f'<div class="offer" data-rv><h3>{t}</h3></div>' for t, d in s["offers"])
    why = "".join(f'<div data-rv style="--dl:{i*.1:.1f}s"><small>0{i+1}</small><b>{t}</b><p>{d}</p></div>' for i, (t, d) in enumerate(s["why"]))
    gal = "".join(f'<figure class="imgrv" data-cursor="Voir"><img src="{g}" alt="{s["title"]}, réalisation de Nathan Fritsch" loading="lazy" decoding="async"></figure>' for g in s["gallery"])
    others = "".join(f'<a href="{o["slug"]}.html" class="other" data-cursor="Découvrir"><img src="{o["hero"]}" alt="" loading="lazy"><b>{o["nav"]} {ARROW}</b></a>' for o in SERVICES if o is not s)
    cname, ctag, cdesc, cimg, clink = s["case"]
    plain_h1 = s["h1"].replace('<em class="it-a">', "").replace("</em>", "")
    return head(f"{s['title']} · Photographe et vidéaste à Bordeaux · Nathan Fritsch",
                f"{s['kicker']} à Bordeaux et partout en France. {s['lead'][:120]}",
                SVC_CSS, f"{s['slug']}") + f"""<body class="dark-top">
{header()}
<main>
<section class="sh">
  <div class="sh-bg" style="background-image:url('{s['hero']}')" data-px="-.15" role="img" aria-label="{s['title']}"></div>
  <div class="wrap">
    <span class="eyebrow lt" data-rv>{s['kicker']} · Bordeaux</span>
    <h1 class="d1 split" aria-label="{plain_h1}">{s['h1']}</h1>
    <div class="sh-row">
      <p data-rv style="--dl:.3s">{s['lead']}</p>
      <a href="contact.html?type={s['form']}" class="btn light big" data-rv style="--dl:.4s">Demander un devis <span class="ar">{ARROW}</span></a>
    </div>
  </div>
</section>

<section class="sec">
  <div class="wrap offers">
    <div class="offers-l">
      <h2 class="d2 split">Ce que je <em class="it-a">réalise.</em></h2>
      <div data-rv><a href="contact.html?type={s['form']}" class="btn">Parler de mon projet <span class="ar">{ARROW}</span></a></div>
    </div>
    <div>{offers}</div>
  </div>
</section>

<section class="sec bone" style="padding-top:clamp(4rem,7vw,6rem);padding-bottom:clamp(4rem,7vw,6rem)">
  <div class="wrap">
    <div style="display:flex;justify-content:space-between;align-items:flex-end;gap:2rem;flex-wrap:wrap;margin-bottom:2.5rem">
      <h2 class="d2 split">En <em class="it-a">images.</em></h2>
      <a href="portfolio.html?type=photo&amp;cat={s['cat']}" class="link" data-rv>Voir toute la galerie {ARR_R}</a>
    </div>
    <div class="gal">{gal}</div>
  </div>
</section>

<section class="sec">
  <div class="wrap feat">
    <div class="feat-img imgrv" data-cursor="Voir"><img src="{cimg}" alt="{cname}" loading="lazy"></div>
    <div class="feat-txt">
            <h2 class="d2 split">{cname}</h2>
      <span class="tag" data-rv>{ctag}</span>
      <div data-rv><a href="{clink}" class="link">Voir le projet {ARR_R}</a></div>
    </div>
  </div>
</section>

{cta_end(s['hero'], q=f"?type={s['form']}")}

<section class="sec" style="padding-bottom:clamp(4rem,7vw,6rem)">
  <div class="wrap">
    <h2 class="d3" data-rv>Autres services</h2>
    <div class="others" style="margin-top:2rem">{others}</div>
  </div>
</section>
</main>
{footer()}
{SCRIPTS}</body>
</html>
"""


# ═════════════════════════════ CONTACT ═════════════════════════════
CONTACT_CSS = """
.hd{color:var(--text)!important;}.hd::before{opacity:1!important;}
.ct{display:grid;grid-template-columns:.85fr 1.15fr;min-height:100vh;}
.ct-l{position:sticky;top:0;height:100vh;height:100svh;color:#fff;overflow:hidden;display:flex;align-items:flex-end;}
.ct-l-bg{position:absolute;inset:0;background:url('assets/img/lacanau-2.jpg') center/cover;transform:scale(1.08);transition:transform 2.4s var(--ease);}
body.ready .ct-l-bg{transform:scale(1);}
.ct-l::after{content:'';position:absolute;inset:0;background:linear-gradient(180deg,rgba(13,15,16,.5),rgba(13,15,16,.35) 40%,rgba(13,15,16,.92));}
.ct-l-in{position:relative;z-index:2;padding:0 clamp(1.5rem,4vw,4rem) clamp(2rem,6vh,4rem);display:flex;flex-direction:column;gap:1.8rem;width:100%;}
.ct-l h1{max-width:10ch;}
.ct-info{display:grid;grid-template-columns:1fr 1fr;gap:1.4rem 2rem;padding-top:1.8rem;border-top:1px solid rgba(255,255,255,.2);}
.ct-info small{display:block;font-size:.64rem;letter-spacing:.2em;text-transform:uppercase;color:var(--a-xl);margin-bottom:.35rem;}
.ct-info a,.ct-info span{color:#fff;text-decoration:none;font-size:.95rem;word-break:break-word;}
.ct-info a:hover{color:var(--a-l);}
.ct-r{padding:clamp(7.5rem,14vh,9rem) clamp(1.5rem,5vw,5.5rem) 5rem;display:flex;flex-direction:column;gap:2.4rem;background:var(--paper);}
.ct-top{display:flex;flex-direction:column;gap:1rem;}
.ct-top h2{font-family:var(--serif);font-weight:450;font-size:clamp(1.9rem,3vw,2.8rem);letter-spacing:-.02em;line-height:1.08;}
.ct-top h2 em{font-style:normal;color:var(--a);}
.ct-top p{color:var(--mute);font-weight:300;}
.prog{display:flex;align-items:center;gap:1rem;}
.prog-bar{flex:1;height:2px;background:var(--line);border-radius:2px;overflow:hidden;}
.prog-bar i{display:block;height:100%;background:var(--a);width:25%;transition:width .7s var(--ease);}
.prog span{font-size:.72rem;letter-spacing:.14em;color:var(--mute);font-weight:500;min-width:3.6em;text-align:right;}
.fs{border:0;display:none;flex-direction:column;gap:1.8rem;animation:stIn .7s var(--ease);}
.fs.on{display:flex;}
@keyframes stIn{from{opacity:0;transform:translateX(24px);}to{opacity:1;transform:none;}}
.fs legend{font-family:var(--serif);font-weight:420;font-size:clamp(1.35rem,2vw,1.7rem);letter-spacing:-.01em;margin-bottom:.4rem;}
.q{font-size:.74rem;letter-spacing:.14em;text-transform:uppercase;font-weight:600;color:var(--text);margin-bottom:.8rem;display:block;}
.opts{display:grid;grid-template-columns:repeat(auto-fill,minmax(180px,1fr));gap:.7rem;}
.opt{position:relative;}
.opt input{position:absolute;opacity:0;pointer-events:none;}
.opt label{display:flex;flex-direction:column;gap:.35rem;height:100%;padding:1.1rem 1.2rem;border:1px solid var(--line);border-radius:14px;cursor:pointer;background:#fff;transition:border-color .3s,background .3s,box-shadow .4s,transform .4s var(--ease);}
.opt label:hover{border-color:rgba(52,77,89,.5);transform:translateY(-2px);}
.opt label b{font-weight:550;font-size:.95rem;}
.opt label span{font-size:.8rem;color:var(--mute);line-height:1.45;}
.opt input:checked+label{border-color:var(--a);background:var(--a-xl);box-shadow:0 0 0 1px var(--a) inset;}
.opt input:focus-visible+label{outline:2px solid var(--a);outline-offset:2px;}
.opts.pill{display:flex;flex-wrap:wrap;}
.opts.pill label{flex-direction:row;padding:.8rem 1.2rem;border-radius:100px;}
.fld{display:flex;flex-direction:column;gap:.5rem;}
.fld label{font-size:.74rem;letter-spacing:.14em;text-transform:uppercase;font-weight:600;}
.fld label i{font-style:normal;color:var(--mute);font-weight:400;text-transform:none;letter-spacing:0;}
.fld input,.fld textarea{width:100%;font:inherit;font-size:1rem;padding:1rem 1.1rem;border:1px solid var(--line);border-radius:12px;background:#fff;color:var(--text);transition:border-color .3s,box-shadow .3s;}
.fld textarea{min-height:150px;resize:vertical;line-height:1.6;}
.fld input:focus,.fld textarea:focus{outline:0;border-color:var(--a);box-shadow:0 0 0 3px rgba(52,77,89,.12);}
.row2{display:grid;grid-template-columns:1fr 1fr;gap:1rem;}
.nav-f{display:flex;justify-content:space-between;align-items:center;gap:1rem;margin-top:.6rem;}
.back{font-size:.74rem;letter-spacing:.14em;text-transform:uppercase;font-weight:600;color:var(--mute);display:inline-flex;align-items:center;gap:.5rem;}
.back:hover{color:var(--text);}
.back svg{width:12px;height:12px;transform:rotate(180deg);}
.err{color:#A1412F;font-size:.85rem;min-height:1.2em;}
.recap{background:var(--bone);border-radius:14px;padding:1.2rem 1.4rem;font-size:.88rem;color:var(--mute);line-height:1.7;}
.recap b{color:var(--text);font-weight:550;}
.done{display:none;flex-direction:column;gap:1.4rem;align-items:flex-start;animation:stIn .7s var(--ease);}
.done.on{display:flex;}
.done-ic{width:64px;height:64px;border-radius:50%;background:var(--a);color:#fff;display:grid;place-items:center;}
.done-ic svg{width:26px;height:26px;}
.alt{display:grid;grid-template-columns:1fr 1fr;gap:.8rem;padding-top:2rem;border-top:1px solid var(--line);}
.alt a{display:flex;align-items:center;justify-content:space-between;gap:1rem;padding:1.2rem 1.3rem;border:1px solid var(--line);border-radius:14px;text-decoration:none;transition:border-color .3s,background .3s;}
.alt a:hover{border-color:var(--a);background:#fff;}
.alt b{display:block;font-weight:550;font-size:.95rem;}
.alt span{font-size:.8rem;color:var(--mute);}
.alt svg{width:12px;height:12px;flex:none;}
.hp{position:absolute;left:-9999px;}
@media (max-width:1080px){
  .ct{grid-template-columns:1fr;}
  .ct-l{position:relative;height:auto;min-height:72svh;}
  .ct-r{padding-top:3.5rem;}
}
@media (max-width:640px){.row2,.alt,.ct-info{grid-template-columns:1fr;}.opts{grid-template-columns:1fr 1fr;}}
"""

FORM_TYPES = [("entreprise", "Entreprise / marque", "Communication, réseaux, portraits"),
              ("immobilier", "Immobilier / conciergerie", "Annonces, visites, locations"),
              ("sport", "Sport", "Compétition, club, athlète"),
              ("evenement", "Événement", "Soirée, séminaire, célébration"),
              ("particulier", "Projet personnel", "Portrait, souvenir, autre idée")]


def contact():
    types = "".join(f'<div class="opt"><input type="radio" name="type_projet" id="t-{k}" value="{t}" data-k="{k}"><label for="t-{k}"><b>{t}</b><span>{d}</span></label></div>' for k, t, d in FORM_TYPES)
    need = "".join(f'<div class="opt"><input type="radio" name="besoin" id="n{i}" value="{v}"><label for="n{i}"><b>{v}</b></label></div>' for i, v in enumerate(["Photo", "Vidéo", "Photo + vidéo", "Je ne sais pas encore"]))
    return head("Contact et devis · Nathan Fritsch, photographe et vidéaste à Bordeaux",
                "Demandez un devis gratuit pour votre projet photo ou vidéo à Bordeaux et partout en France. Réponse sous 24 h.",
                CONTACT_CSS, "contact") + f"""<body class="dark-top">
{header('contact')}
<main class="ct">
  <aside class="ct-l">
    <div class="ct-l-bg" role="img" aria-label="Surfeur au Lacanau Pro"></div>
    <div class="ct-l-in">
      <span class="eyebrow lt" data-rv>Devis gratuit</span>
      <h1 class="d1 split" style="font-size:clamp(2.6rem,5.4vw,5.6rem)">Parlons de votre <em class="it-a">projet.</em></h1>
      <div class="ct-info" data-rv style="--dl:.3s">
        <div><small>Email</small><a href="mailto:{EMAIL}">{EMAIL}</a></div>
        <div><small>Réponse</small><span>Sous 24 h</span></div>
        <div><small>Zone</small><span>Bordeaux · France entière</span></div>
        <div><small>Instagram</small><a href="{IG}" target="_blank" rel="noopener">@nathanfrt_visuals</a></div>
      </div>
    </div>
  </aside>

  <section class="ct-r">
    <div class="ct-top">
      <h2>4 questions. <em>2 minutes.</em></h2>
    </div>
    <div class="prog" aria-hidden="true"><div class="prog-bar"><i id="pBar"></i></div><span id="pTxt">1 / 4</span></div>

    <form id="qf" action="https://formspree.io/f/VOTRE_ID_FORMSPREE" method="POST" novalidate>
      <input type="text" name="_gotcha" class="hp" tabindex="-1" autocomplete="off">
      <input type="hidden" name="_subject" id="subj" value="Nouvelle demande de devis · site">

      <fieldset class="fs on" data-step="1">
        <legend>Quel type de projet ?</legend>
        <div class="opts">{types}</div>
        <p class="err" aria-live="polite"></p>
        <div class="nav-f"><span></span><button type="button" class="btn nx">Continuer <span class="ar">{ARR_R}</span></button></div>
      </fieldset>

      <fieldset class="fs" data-step="2">
        <legend>De quoi avez-vous besoin ?</legend>
        <div><span class="q">Format</span><div class="opts pill">{need}</div></div>
        <div class="row2">
          <div class="fld"><label for="f-date">Date ou période <i>(si connue)</i></label><input id="f-date" name="date" type="text" placeholder="Ex. 14 juin, ou septembre"></div>
          <div class="fld"><label for="f-lieu">Lieu</label><input id="f-lieu" name="lieu" type="text" placeholder="Ex. Bordeaux, Lacanau…"></div>
        </div>
        <p class="err" aria-live="polite"></p>
        <div class="nav-f"><button type="button" class="back">{ARR_R} Retour</button><button type="button" class="btn nx">Continuer <span class="ar">{ARR_R}</span></button></div>
      </fieldset>

      <fieldset class="fs" data-step="3">
        <legend>Votre projet en quelques mots</legend>
        <div class="fld"><label for="f-msg" class="sr">Message</label><textarea id="f-msg" name="message" placeholder="Ce que vous imaginez, pour quand, pour quel usage…" required></textarea></div>
        <p class="err" aria-live="polite"></p>
        <div class="nav-f"><button type="button" class="back">{ARR_R} Retour</button><button type="button" class="btn nx">Continuer <span class="ar">{ARR_R}</span></button></div>
      </fieldset>

      <fieldset class="fs" data-step="4">
        <legend>Où puis-je vous répondre ?</legend>
        <div class="row2">
          <div class="fld"><label for="f-nom">Prénom et nom</label><input id="f-nom" name="nom" type="text" autocomplete="name" required></div>
          <div class="fld"><label for="f-soc">Entreprise <i>(facultatif)</i></label><input id="f-soc" name="entreprise" type="text" autocomplete="organization"></div>
        </div>
        <div class="row2">
          <div class="fld"><label for="f-mail">Email</label><input id="f-mail" name="email" type="email" autocomplete="email" required></div>
          <div class="fld"><label for="f-tel">Téléphone <i>(facultatif)</i></label><input id="f-tel" name="telephone" type="tel" autocomplete="tel"></div>
        </div>
        <div class="recap" id="recap"></div>
        <p class="err" aria-live="polite"></p>
        <div class="nav-f"><button type="button" class="back">{ARR_R} Retour</button><button type="submit" class="btn" id="sendBtn">Envoyer ma demande <span class="ar">{ARROW}</span></button></div>
      </fieldset>
    </form>

    <div class="done" id="done" role="status">
      <div class="done-ic"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="m5 12 5 5 9-10"/></svg></div>
      <h2 class="d3">Merci, c'est bien reçu.</h2>
      <p class="lead">Réponse sous 24 h.</p>
      <a href="portfolio.html?type=photo" class="btn">Voir le portfolio <span class="ar">{ARROW}</span></a>
    </div>

    <div class="alt">
      <a href="{CAL}" target="_blank" rel="noopener"><div><b>Réserver un appel</b><span>30 minutes, gratuit</span></div>{ARROW}</a>
      <a href="mailto:{EMAIL}"><div><b>Écrire un email</b><span>{EMAIL}</span></div>{ARROW}</a>
    </div>
  </section>
</main>
{footer()}
{SCRIPTS}<script src="assets/contact.js" defer></script>
</body>
</html>
"""


def patch_portfolio():
    import re
    p = ROOT / "portfolio.html"
    t = p.read_text(encoding="utf-8")
    hd = "<!--V2-HD-->\n" + header() + "<!--/V2-HD-->\n"
    if "<!--V2-HD-->" in t:
        t = re.sub(r"<!--V2-HD-->.*?<!--/V2-HD-->\n", lambda m: hd, t, flags=re.S)
    else:
        t = re.sub(r"<nav>.*?(?=<div class=\"ph\">)", lambda m: hd + "\n", t, count=1, flags=re.S)
    ft = "<!--V2-FT-->\n" + footer() + "<!--/V2-FT-->\n"
    if "<!--V2-FT-->" in t:
        t = re.sub(r"<!--V2-FT-->.*?<!--/V2-FT-->\n", lambda m: ft, t, flags=re.S)
    else:
        t = re.sub(r"<footer>.*?</footer>\n", lambda m: ft, t, count=1, flags=re.S)
    if "assets/site.css" not in t:
        t = t.replace("<style>", '<link rel="stylesheet" href="assets/site.css">\n<style>', 1)
        t = t.replace("</style>\n</head>", "/* V2 */\n#modal{z-index:520;}#lb{z-index:640;}.hd{color:var(--text)!important;}.hd::before{opacity:1!important;}\nbody{background:var(--bg);}\n.fx a,.hd a{cursor:none;}\n@media(pointer:coarse){.fx a,.hd a{cursor:auto;}}\n</style>\n</head>", 1)
        t = t.replace("<body>", '<body class="dark-top" data-lite>', 1)
        t = t.replace("</body>", '<script src="assets/site.js" defer></script>\n</body>', 1)
    p.write_text(t, encoding="utf-8")


if __name__ == "__main__":
    patch_portfolio()
    (ROOT / "index.html").write_text(index(), encoding="utf-8")
    for s in SERVICES:
        (ROOT / f"{s['slug']}.html").write_text(service(s), encoding="utf-8")
    (ROOT / "contact.html").write_text(contact(), encoding="utf-8")
    print("ok")
