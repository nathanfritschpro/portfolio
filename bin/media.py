#!/usr/bin/env python3
"""Prépare les médias du site (V3).

- Photos : importe les nouveaux projets depuis ~/Desktop/photos, ramène toutes
  les photos du site à 2048 px (grand côté) et crée une vignette de 720 px de
  large dans thumbs/ (même arborescence que photos/).
- Vidéos : encode les films verticaux (1080x1920, 25 i/s), leurs boucles
  d'aperçu muettes (720x1280) et une affiche (poster) par vidéo.
- Index : écrit bin/media-index.json (dimensions des photos, durée et
  dimensions des vidéos) utilisé par bin/build.py.

Idempotent : ce qui existe déjà et est à jour est sauté.
Usage : python3 bin/media.py            (depuis la racine du site)
"""
from __future__ import annotations

import json
import shutil
import struct
import subprocess
import sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SRC_PHOTOS = Path.home() / "Desktop" / "photos"
SRC_VIDEOS = Path.home() / "Desktop" / "videos"

LARGE = 2048          # grand côté des photos affichées en plein écran
THUMB_W = 720         # largeur des vignettes
Q_LARGE = 80
Q_THUMB = 72

# Nouveaux projets : dossier source -> dossier du site (+ fichiers à ignorer)
NEW_PHOTO_SETS = [
    ("one fitness", "one-fitness", {"IMG_3305.jpg"}),   # doublon de IMG_3305-2
    ("frenchkiss", "french-kiss", set()),
]
# Nouvelles photos immobilières (octobre 2026) : seulement celles-ci
IMMO_NEW = ["IMG_2630", "IMG_2632", "IMG_2634-2", "IMG_2636", "IMG_2637", "IMG_2641", "IMG_2643",
            "IMG_2644", "IMG_2647", "IMG_2648", "IMG_2650", "IMG_2655", "IMG_2673", "IMG_2674"]
# Voyage à Saint-Martin : photos avec un tag rouge dans le Finder
ST_MARTIN = ["IMG_3762.jpg", "IMG_3972.jpg", "IMG_4093.jpg", "IMG_3480.jpg", "IMG_3482.jpg", "IMG_3552.jpg", "IMG_3570.jpg", "IMG_3577.jpg", "IMG_3591.jpg", "IMG_3665.jpg", "IMG_3683.jpg", "IMG_3745.jpg", "IMG_3757.jpg", "IMG_3837.jpg", "IMG_3842.jpg", "IMG_3863.jpg", "IMG_4039.jpg", "IMG_4043.jpg", "IMG_4074.jpg", "IMG_4101.jpg", "IMG_4275.jpg", "IMG_4392.jpg", "IMG_4402.jpg", "dji_fly_20261021_185016_73_1793552194145_photo_optimized.jpg", "dji_fly_20261021_185306_80_1793552173016_photo_optimized.jpg", "dji_fly_20261021_185330_82_1793552171369_photo_optimized.jpg", "dji_fly_20261021_184910_69_1793552204383_photo_optimized.jpg"]  # photos tag rouge + photo du hero

# Films verticaux : source, sortie, boucles d'aperçu [(suffixe, début, durée)], instant de l'affiche
FILMS = [
    dict(src="one fitness/one fitness v1.mov", out="videos/one-fitness/ouverture.mp4",
         loops=[("loop", 0.0, 10.64), ("loop-2", 38.26, 10.50)], poster_at=45.6),
    dict(src="frenchkiss/frenchkiss V2.mov", out="videos/french-kiss/brunch.mp4",
         loops=[("loop", 0.0, 9.96), ("loop-2", 14.14, 9.72)], poster_at=2.1),
    dict(src="business/sunset st martin.MOV", out="videos/st-martin/sunset.mp4", size="1920:1080", loops=[], poster_at=5.0),
    dict(src="immo/Timeline 1.mov", out="videos/immo/villa-bar.mp4", size="1920:1080", loops=[], poster_at=4.6),
]

# Instant de l'affiche pour les vidéos déjà en ligne (défaut : 25 % de la durée)
POSTER_AT = {
    "videos/evenement/lacanau-pro-2026.mp4": 1.0,
    "videos/le-mahi-mahi-n1.mp4": 12.0,
    "videos/immo/maison-bertrand/immo-bertrand.mp4": 18.3,
}


def run(cmd: list[str]) -> None:
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode != 0:
        raise RuntimeError(f"{' '.join(cmd[:3])}… : {(r.stderr or r.stdout).strip()[-400:]}")


def jpeg_size(path: Path) -> tuple[int, int]:
    """Largeur, hauteur d'un JPEG (lecture de l'en-tête, orientation EXIF prise en compte)."""
    with path.open("rb") as f:
        data = f.read(256 * 1024)
    i, orient = 2, 1
    while i + 4 <= len(data):
        if data[i] != 0xFF:
            i += 1
            continue
        marker = data[i + 1]
        if marker in (0xD8, 0x01) or 0xD0 <= marker <= 0xD7:
            i += 2
            continue
        seg = struct.unpack(">H", data[i + 2:i + 4])[0]
        if marker == 0xE1 and data[i + 4:i + 10] == b"Exif\x00\x00":
            t = data[i + 10:i + 2 + seg]
            if len(t) >= 8:
                e = "<" if t[:2] == b"II" else ">"
                off = struct.unpack(e + "I", t[4:8])[0]
                if off + 2 <= len(t):
                    for k in range(struct.unpack(e + "H", t[off:off + 2])[0]):
                        p = off + 2 + 12 * k
                        if p + 12 <= len(t) and struct.unpack(e + "H", t[p:p + 2])[0] == 0x0112:
                            orient = struct.unpack(e + "H", t[p + 8:p + 10])[0]
        if marker in (0xC0, 0xC1, 0xC2):
            h, w = struct.unpack(">HH", data[i + 5:i + 9])
            return (h, w) if orient >= 5 else (w, h)
        i += 2 + seg
    out = subprocess.run(["sips", "-g", "pixelWidth", "-g", "pixelHeight", str(path)], capture_output=True, text=True).stdout
    vals = [int(x.split(":")[1]) for x in out.splitlines() if "pixel" in x]
    return vals[0], vals[1]


def sips(src: Path, dst: Path, *args: str, quality: int) -> None:
    dst.parent.mkdir(parents=True, exist_ok=True)
    tmp = dst.with_name(dst.stem + ".part.jpg")
    run(["sips", "-s", "format", "jpeg", "-s", "formatOptions", str(quality), *args, str(src), "--out", str(tmp)])
    tmp.replace(dst)


def all_photos() -> list[Path]:
    return sorted(p for p in (ROOT / "photos").rglob("*") if p.suffix.lower() in (".jpg", ".jpeg"))


def import_new_photos() -> None:
    jobs = []
    for src_dir, dst_dir, skip in NEW_PHOTO_SETS:
        for src in sorted((SRC_PHOTOS / src_dir).glob("*.jpg")):
            if src.name in skip:
                continue
            dst = ROOT / "photos" / dst_dir / src.name
            if not dst.exists() or src.stat().st_mtime > dst.stat().st_mtime:
                jobs.append((src, dst))
    for n in ST_MARTIN:
        src, dst = SRC_PHOTOS / "st martin" / n, ROOT / "photos" / "st-martin" / n
        if not dst.exists() or src.stat().st_mtime > dst.stat().st_mtime:
            jobs.append((src, dst))
    for n in IMMO_NEW:
        src, dst = SRC_PHOTOS / "immo" / f"{n}.jpg", ROOT / "photos" / "immo" / f"{n}.jpg"
        if not dst.exists() or src.stat().st_mtime > dst.stat().st_mtime:
            jobs.append((src, dst))
    print(f"• nouvelles photos à importer : {len(jobs)}")
    with ThreadPoolExecutor(8) as ex:
        list(ex.map(lambda j: sips(j[0], j[1], "-Z", str(LARGE), quality=Q_LARGE), jobs))


def shrink_existing() -> None:
    jobs = [p for p in all_photos() if max(jpeg_size(p)) > LARGE]
    print(f"• photos à ramener à {LARGE}px : {len(jobs)}")
    with ThreadPoolExecutor(8) as ex:
        list(ex.map(lambda p: sips(p, p, "-Z", str(LARGE), quality=Q_LARGE), jobs))


def make_thumbs() -> None:
    jobs = []
    for p in all_photos():
        t = ROOT / "thumbs" / p.relative_to(ROOT / "photos")
        if not t.exists() or p.stat().st_mtime > t.stat().st_mtime:
            jobs.append((p, t))
    print(f"• vignettes à créer : {len(jobs)}")

    def one(j):
        src, dst = j
        w, _ = jpeg_size(src)
        if w <= THUMB_W:
            dst.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(src, dst)
        else:
            sips(src, dst, "--resampleWidth", str(THUMB_W), quality=Q_THUMB)

    with ThreadPoolExecutor(8) as ex:
        list(ex.map(one, jobs))
    # vignettes orphelines (photo supprimée)
    for t in (ROOT / "thumbs").rglob("*.jp*g"):
        if not (ROOT / "photos" / t.relative_to(ROOT / "thumbs")).exists():
            t.unlink()


X264 = ["-c:v", "libx264", "-preset", "slow", "-pix_fmt", "yuv420p", "-profile:v", "high", "-movflags", "+faststart"]


def encode_films() -> None:
    for f in FILMS:
        src, out = SRC_VIDEOS / f["src"], ROOT / f["out"]
        out.parent.mkdir(parents=True, exist_ok=True)
        if not src.exists():
            print(f"  ! source vidéo introuvable : {src}")
            continue
        if not out.exists() or src.stat().st_mtime > out.stat().st_mtime:
            print(f"• film : {out.relative_to(ROOT)}")
            run(["ffmpeg", "-y", "-loglevel", "error", "-i", str(src),
                 "-vf", f"fps=25,scale={f.get('size', '1080:1920')}:flags=lanczos", *X264, "-level", "4.1",
                 "-crf", "23", "-maxrate", "5M", "-bufsize", "10M",
                 "-c:a", "aac", "-b:a", "128k", str(out)])
        for suffix, start, dur in f["loops"]:
            lp = out.with_name(f"{out.stem}-{suffix}.mp4")
            if not lp.exists() or src.stat().st_mtime > lp.stat().st_mtime:
                print(f"• boucle : {lp.relative_to(ROOT)}")
                run(["ffmpeg", "-y", "-loglevel", "error", "-ss", str(start), "-t", str(dur), "-i", str(src),
                     "-vf", "fps=25,scale=720:1280:flags=lanczos", *X264, "-level", "4.0",
                     "-crf", "27", "-maxrate", "2M", "-bufsize", "4M", "-an", str(lp)])
                run(["ffmpeg", "-y", "-loglevel", "error", "-ss", str(start + 0.4), "-i", str(src), "-frames:v", "1",
                     "-vf", "scale=720:1280:flags=lanczos", "-q:v", "4", str(lp.with_suffix(".jpg"))])


def video_info(p: Path) -> dict:
    out = subprocess.run(["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries",
                          "stream=width,height:format=duration", "-of", "json", str(p)], capture_output=True, text=True).stdout
    j = json.loads(out)
    return dict(w=j["streams"][0]["width"], h=j["streams"][0]["height"], d=round(float(j["format"]["duration"]), 1))


def make_posters(videos: dict) -> None:
    film_posters = {f["out"]: f["poster_at"] for f in FILMS}
    for rel, info in videos.items():
        if rel.endswith(("-loop.mp4", "-loop-2.mp4")):
            continue
        dst = ROOT / "posters" / (rel[len("videos/"):].replace("/", "-").rsplit(".", 1)[0] + ".jpg")
        src = ROOT / rel
        if dst.exists() and dst.stat().st_mtime >= src.stat().st_mtime:
            continue
        at = film_posters.get(rel, POSTER_AT.get(rel, round(info["d"] * 0.25, 1)))
        dst.parent.mkdir(parents=True, exist_ok=True)
        long_side = "scale=-2:1920" if info["h"] > info["w"] else "scale=1600:-2"
        run(["ffmpeg", "-y", "-loglevel", "error", "-ss", str(at), "-i", str(src), "-frames:v", "1",
             "-vf", long_side + ":flags=lanczos", "-q:v", "4", str(dst)])
        print(f"• affiche : {dst.relative_to(ROOT)} (à {at}s)")


def write_index() -> None:
    photos = {}
    for p in all_photos():
        w, h = jpeg_size(p)
        photos[p.relative_to(ROOT).as_posix()] = [w, h]
    videos = {}
    for p in sorted((ROOT / "videos").rglob("*.mp4")):
        videos[p.relative_to(ROOT).as_posix()] = video_info(p)
    make_posters(videos)
    (ROOT / "bin" / "media-index.json").write_text(json.dumps(dict(photos=photos, videos=videos), ensure_ascii=False, indent=0), encoding="utf-8")
    print(f"• index : {len(photos)} photos, {len(videos)} vidéos")


if __name__ == "__main__":
    if not shutil.which("ffmpeg") or not shutil.which("sips"):
        sys.exit("ffmpeg et sips sont nécessaires.")
    import_new_photos()
    shrink_existing()
    make_thumbs()
    encode_films()
    write_index()
    print("ok")
