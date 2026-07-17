#!/usr/bin/env python3
"""
Renomme tous les fichiers/dossiers de photos/ et videos/ qui contiennent
des caracteres speciaux (espace, ':', '#', accents) et met a jour les
references dans les 3 fichiers HTML.

Vercel a des soucis a servir certains chemins avec espaces/':'/'#' :
ce script les remplace par des tirets et underscore.
"""
import os
import re
import unicodedata
import urllib.parse
import subprocess
from pathlib import Path

SITE = Path(__file__).resolve().parent.parent
HTML_FILES = ["index.html", "portfolio.html", "contact.html"]
ROOTS = ["photos", "videos"]

def slugify_segment(name: str) -> str:
    """Rend un nom de fichier/dossier safe pour Vercel."""
    # separer nom et extension
    stem, dot, ext = name.rpartition('.')
    if not dot:
        stem, ext = name, ''
    # normaliser les accents : é → e, ç → c, etc.
    s = unicodedata.normalize('NFKD', stem)
    s = ''.join(c for c in s if not unicodedata.combining(c))
    # remplacer les chars problematiques
    s = s.replace('#', 'n')
    s = re.sub(r'[:\s]+', '-', s)  # ':' et espaces → tirets
    s = re.sub(r'-+', '-', s).strip('-')
    # extension: lowercase + safe
    ext_safe = re.sub(r'[^a-zA-Z0-9]', '', ext).lower()
    return s + ('.' + ext_safe if ext_safe else '')

def needs_rename(name: str) -> bool:
    return bool(re.search(r'[\s:#]', name)) or any(ord(c) > 127 for c in name)

def collect_renames():
    """Bottom-up : d'abord les fichiers, puis les dossiers."""
    renames = []  # list of (old_path, new_path) as strings relative to SITE
    for root in ROOTS:
        rp = SITE / root
        if not rp.exists():
            continue
        # walk bottom-up
        for dirpath, dirnames, filenames in os.walk(rp, topdown=False):
            for f in filenames:
                if needs_rename(f):
                    old = os.path.join(dirpath, f)
                    new = os.path.join(dirpath, slugify_segment(f))
                    if old != new:
                        renames.append((old, new))
            # Le dirname
            for d in dirnames:
                if needs_rename(d):
                    old = os.path.join(dirpath, d)
                    new = os.path.join(dirpath, slugify_segment(d))
                    if old != new:
                        renames.append((old, new))
    return renames

def git_mv(old, new):
    # Cree le dossier parent si besoin
    Path(new).parent.mkdir(parents=True, exist_ok=True)
    # git mv gere l'index git
    r = subprocess.run(['git', 'mv', old, new], capture_output=True, text=True, cwd=SITE)
    if r.returncode != 0:
        # fallback: rename normal
        os.rename(old, new)
        subprocess.run(['git', 'add', new], cwd=SITE)
        subprocess.run(['git', 'rm', '--cached', old], cwd=SITE, capture_output=True)

def main():
    renames = collect_renames()
    if not renames:
        print("Rien a renommer.")
        return

    print(f"{len(renames)} rename(s) a effectuer :")
    for old, new in renames:
        old_rel = os.path.relpath(old, SITE)
        new_rel = os.path.relpath(new, SITE)
        print(f"  {old_rel}\n    -> {new_rel}")

    # Batir la map complete (rel path old -> rel path new) en tenant compte
    # de la cascade (un fichier dans un dossier renomme change de chemin aussi)
    full_map = {}  # ancien chemin complet -> nouveau chemin complet
    dir_renames = [(os.path.relpath(o, SITE), os.path.relpath(n, SITE))
                   for o, n in renames if os.path.isdir(o)]
    file_renames = [(os.path.relpath(o, SITE), os.path.relpath(n, SITE))
                    for o, n in renames if os.path.isfile(o)]

    # Faire les renames physiques
    for old, new in renames:
        git_mv(old, new)

    # Maintenant construire la map old_rel → new_rel pour TOUS les fichiers
    # sous photos/ et videos/, en composant les renames
    def compose(rel_path: str) -> str:
        # Applique tous les renames de dossiers dans le chemin
        parts = rel_path.split('/')
        # Le premier dossier est photos/ ou videos/. Slugify pour eviter le pb.
        for i in range(len(parts)):
            seg = parts[i]
            if needs_rename(seg):
                parts[i] = slugify_segment(seg)
        return '/'.join(parts)

    print("\nMise a jour des HTML...")
    total_repl = 0
    for htmlname in HTML_FILES:
        p = SITE / htmlname
        if not p.exists():
            continue
        text = p.read_text(encoding='utf-8')
        orig = text
        # Trouver toutes les refs (2 formes : brute et URL-encoded)
        # On travaille sur les refs entre quotes.
        REF_RE = re.compile(r'''(["'])((?:photos|videos)/[^"'\n\r]+?)(["'])''')
        def repl(m):
            q1, path, q2 = m.group(1), m.group(2), m.group(3)
            # decode URL if encoded
            decoded = urllib.parse.unquote(path)
            new_path = compose(decoded)
            if new_path == decoded:
                return m.group(0)
            # Re-encode uniquement si l'original etait encode
            if '%' in path:
                new_out = urllib.parse.quote(new_path)
            else:
                new_out = new_path
            return f"{q1}{new_out}{q2}"
        text = REF_RE.sub(repl, text)
        if text != orig:
            p.write_text(text, encoding='utf-8')
            n = sum(1 for _ in re.finditer(r'', text))  # cosmetique
            print(f"  OK {htmlname}")
            total_repl += 1
        else:
            print(f"  -- {htmlname} rien a changer")

    print(f"\nFini. {len(renames)} rename(s), {total_repl} HTML modifie(s).")

if __name__ == '__main__':
    main()
