#!/usr/bin/env python3
"""
Compresse les medias utilises par le site (photos + videos).

Comment ca marche :
- Lit les 3 fichiers HTML (index, portfolio, contact)
- Detecte tous les chemins photos/... et videos-src/... (ou videos/...) references
- Pour chaque photo  : resize max 2560 px, qualite JPG 82  (via ffmpeg)
- Pour chaque video  : encode H.264 1080p, bitrate ~5 Mbps (via ffmpeg)
- Ecrit les resultats compresses dans mon-site/photos/ et mon-site/videos/
  en preservant l'arborescence des sous-dossiers
- IDEMPOTENT : si un fichier compresse existe deja et qu'il est plus recent
  que la source, on le saute (donc les prochaines executions sont rapides)

Sources par defaut :
- Photos  : /Users/nathan/Desktop/photos
- Videos  : /Users/nathan/Desktop/videos

Usage :
  python3 bin/compress-media.py            # compresse tout ce qui manque
  python3 bin/compress-media.py --dry-run  # liste ce qui serait fait, sans agir
  python3 bin/compress-media.py --force    # re-compresse meme si a jour
  python3 bin/compress-media.py --only-photos
  python3 bin/compress-media.py --only-videos
"""

from __future__ import annotations
import argparse
import os
import re
import shutil
import subprocess
import sys
import time
import urllib.parse
from pathlib import Path

# ------- CONFIG ----------------------------------------------------------------

SITE_DIR = Path(__file__).resolve().parent.parent          # mon-site/
HTML_FILES = ["index.html", "portfolio.html", "contact.html"]

# Ou trouver les originaux
PHOTOS_SRC = Path("/Users/nathan/Desktop/photos")
VIDEOS_SRC = Path("/Users/nathan/Desktop/videos")

# Ou ecrire les versions compressees (dans le dossier du site)
PHOTOS_DST = SITE_DIR / "photos"
VIDEOS_DST = SITE_DIR / "videos"

# Prefixes reconnus dans le HTML
PHOTO_PREFIX = "photos/"
# Le HTML utilise historiquement videos-src/ (le symlink en dev).
# Cible finale sur le site : videos/. On accepte les deux dans les regex.
VIDEO_PREFIXES = ("videos-src/", "videos/")

# Parametres de compression photos
PHOTO_MAX_WIDTH = 2560
PHOTO_QUALITY = 3   # qualite ffmpeg mjpeg : 2 = tres haut, 5 = correct. 3 ~= JPG q82

# Parametres de compression videos
VIDEO_MAX_HEIGHT = 1080
VIDEO_CRF = 23            # qualite (18 = tres haut, 28 = bas). 23 = defaut web
VIDEO_PRESET = "medium"   # slow = plus petit, faster = plus rapide
VIDEO_AUDIO_KBPS = 128

PHOTO_EXTS = {".jpg", ".jpeg", ".png"}
VIDEO_EXTS = {".mov", ".mp4", ".m4v", ".webm"}

# Regex pour attraper les chemins dans le HTML
REF_RE = re.compile(
    r'(?<![\w/])(?:photos|videos-src|videos)/[^\s"\')>]+',
    re.IGNORECASE,
)

# ------- UTILS -----------------------------------------------------------------

def log(msg: str, level: str = "info") -> None:
    tag = {"ok": "\033[32m✓\033[0m", "skip": "\033[90m·\033[0m",
           "warn": "\033[33m!\033[0m", "err": "\033[31m✗\033[0m",
           "info": " "}[level]
    print(f"{tag} {msg}")

def url_to_path(ref: str) -> str:
    """'photos/le%20mahi%20mahi/IMG_6163.jpg' -> 'photos/le mahi mahi/IMG_6163.jpg'"""
    return urllib.parse.unquote(ref.split("#", 1)[0].split("?", 1)[0])

def is_photo(name: str) -> bool:
    return Path(name).suffix.lower() in PHOTO_EXTS

def is_video(name: str) -> bool:
    return Path(name).suffix.lower() in VIDEO_EXTS

def newer(src: Path, dst: Path) -> bool:
    """True si dst manque ou si src est plus recent que dst."""
    return (not dst.exists()) or (src.stat().st_mtime > dst.stat().st_mtime)

def run(cmd: list[str]) -> tuple[bool, str]:
    try:
        r = subprocess.run(cmd, capture_output=True, text=True)
        return r.returncode == 0, (r.stderr or r.stdout).strip()
    except FileNotFoundError as e:
        return False, str(e)

# ------- COLLECTE --------------------------------------------------------------

def collect_refs() -> tuple[set[str], set[str]]:
    """Retourne (photos_relatives, videos_relatives)."""
    photos: set[str] = set()
    videos: set[str] = set()

    for html in HTML_FILES:
        p = SITE_DIR / html
        if not p.exists():
            log(f"HTML introuvable : {html}", "warn")
            continue
        text = p.read_text(encoding="utf-8")
        for match in REF_RE.findall(text):
            rel = url_to_path(match)
            # On veut le nom apres le prefix
            if rel.startswith("photos/") and is_photo(rel):
                photos.add(rel[len("photos/"):])
            elif rel.startswith("videos-src/") and is_video(rel):
                videos.add(rel[len("videos-src/"):])
            elif rel.startswith("videos/") and is_video(rel):
                videos.add(rel[len("videos/"):])
    return photos, videos

# ------- COMPRESSION PHOTOS ---------------------------------------------------

def compress_photo(src: Path, dst: Path, dry: bool, force: bool) -> str:
    if not src.exists():
        return "missing"
    if not force and not newer(src, dst):
        return "skip"
    if dry:
        return "todo"
    dst.parent.mkdir(parents=True, exist_ok=True)
    tmp = dst.with_name(dst.stem + ".part" + dst.suffix)
    cmd = [
        "ffmpeg", "-y", "-loglevel", "error",
        "-i", str(src),
        "-vf", f"scale='min({PHOTO_MAX_WIDTH},iw)':-2:flags=lanczos",
        "-q:v", str(PHOTO_QUALITY),
        "-pix_fmt", "yuvj420p",
        "-f", "mjpeg",
        str(tmp),
    ]
    ok, err = run(cmd)
    if not ok:
        tmp.unlink(missing_ok=True)
        raise RuntimeError(f"ffmpeg photo error: {err}")
    tmp.replace(dst)
    return "done"

# ------- COMPRESSION VIDEOS ---------------------------------------------------

def compress_video(src: Path, dst: Path, dry: bool, force: bool) -> str:
    # On force la sortie en .mp4 (universellement lu, streamable)
    if dst.suffix.lower() not in {".mp4"}:
        dst = dst.with_suffix(".mp4")

    if not src.exists():
        return "missing"
    if not force and not newer(src, dst):
        return "skip"
    if dry:
        return "todo"
    dst.parent.mkdir(parents=True, exist_ok=True)
    tmp = dst.with_name(dst.stem + ".part.mp4")
    cmd = [
        "ffmpeg", "-y", "-loglevel", "error",
        "-i", str(src),
        # Downscale a 1080p max (garde l'aspect), pad a taille paire
        "-vf", f"scale='min({VIDEO_MAX_HEIGHT}*iw/ih,iw)':'min({VIDEO_MAX_HEIGHT},ih)':force_original_aspect_ratio=decrease,scale=trunc(iw/2)*2:trunc(ih/2)*2",
        # H.264 avec CRF (qualite auto)
        "-c:v", "libx264", "-preset", VIDEO_PRESET, "-crf", str(VIDEO_CRF),
        "-pix_fmt", "yuv420p",
        "-profile:v", "high", "-level", "4.1",
        # Audio AAC (compatible tout navigateur)
        "-c:a", "aac", "-b:a", f"{VIDEO_AUDIO_KBPS}k",
        # Streaming : moov atom au debut => la video demarre avant d'etre finie de dl
        "-movflags", "+faststart",
        str(tmp),
    ]
    ok, err = run(cmd)
    if not ok:
        tmp.unlink(missing_ok=True)
        raise RuntimeError(f"ffmpeg video error: {err}")
    tmp.replace(dst)
    return "done"

# ------- MAIN ------------------------------------------------------------------

def human_size(bytes_: int) -> str:
    for unit in ["o", "Ko", "Mo", "Go"]:
        if bytes_ < 1024:
            return f"{bytes_:.1f} {unit}"
        bytes_ /= 1024
    return f"{bytes_:.1f} To"

def process(kind: str, refs: set[str], src_root: Path, dst_root: Path,
            fn, dry: bool, force: bool) -> tuple[int, int, int, int]:
    """Retourne (done, skipped, missing, total)."""
    done = skipped = missing = 0
    total_src = total_dst = 0
    refs = sorted(refs)
    header = f"{kind.upper()}  ({len(refs)} fichier{'s' if len(refs)!=1 else ''})"
    print(f"\n▸ {header}")
    print(f"  Source      : {src_root}")
    print(f"  Destination : {dst_root}")
    if not refs:
        log("aucun fichier reference dans le HTML", "info")
        return 0, 0, 0, 0
    for i, rel in enumerate(refs, 1):
        src = src_root / rel
        dst = dst_root / rel
        prefix = f"  [{i:>3}/{len(refs)}] {rel}"
        try:
            status = fn(src, dst, dry, force)
        except Exception as e:
            log(f"{prefix}  ERREUR: {e}", "err")
            continue
        if status == "missing":
            log(f"{prefix}  source introuvable", "warn")
            missing += 1
            continue
        # On peut avoir change l'extension (video -> .mp4)
        if kind == "videos" and dst.suffix.lower() != ".mp4":
            dst = dst.with_suffix(".mp4")
        if status == "skip":
            log(f"{prefix}  a jour", "skip")
            skipped += 1
        elif status == "todo":
            log(f"{prefix}  a compresser", "info")
        elif status == "done":
            s_sz = src.stat().st_size
            d_sz = dst.stat().st_size if dst.exists() else 0
            total_src += s_sz
            total_dst += d_sz
            ratio = (1 - d_sz/s_sz)*100 if s_sz else 0
            log(f"{prefix}  {human_size(s_sz)} -> {human_size(d_sz)}  (-{ratio:.0f} %)", "ok")
            done += 1
    if done:
        ratio = (1 - total_dst/total_src)*100 if total_src else 0
        print(f"  ─── Total compresse : {human_size(total_src)} -> {human_size(total_dst)}  (-{ratio:.0f} %)")
    return done, skipped, missing, len(refs)

def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--dry-run", action="store_true", help="Liste ce qui serait fait, sans compresser")
    ap.add_argument("--force", action="store_true", help="Re-compresse meme si a jour")
    ap.add_argument("--only-photos", action="store_true")
    ap.add_argument("--only-videos", action="store_true")
    args = ap.parse_args()

    if not shutil.which("ffmpeg"):
        log("ffmpeg n'est pas installe (ou pas dans le PATH).", "err")
        log("Installe-le avec : brew install ffmpeg", "info")
        return 2

    t0 = time.time()
    photos, videos = collect_refs()
    print(f"Detecte : {len(photos)} photo(s), {len(videos)} video(s) utilisee(s) dans le HTML.")

    totals = [0, 0, 0, 0]
    if not args.only_videos:
        d = process("photos", photos, PHOTOS_SRC, PHOTOS_DST, compress_photo, args.dry_run, args.force)
        totals = [a+b for a, b in zip(totals, d)]
    if not args.only_photos:
        d = process("videos", videos, VIDEOS_SRC, VIDEOS_DST, compress_video, args.dry_run, args.force)
        totals = [a+b for a, b in zip(totals, d)]

    dt = time.time() - t0
    done, skipped, missing, total = totals
    print(f"\n━━━ {done} compresse(s) · {skipped} a jour · {missing} manquant(s) · {total} au total · {dt:.1f}s ━━━")
    return 0 if missing == 0 else 1

if __name__ == "__main__":
    sys.exit(main())
