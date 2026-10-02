"""Branded Reels for the AI news page (needs ffmpeg + ffprobe).

  clip_reel()    an official video clip plays inside the post card, where the picture normally sits
  motion_reel()  no clip available: the article picture slowly zooms inside the post card

Output: 1080 x 1350, H.264 + AAC, 30 fps, faststart, under ~14 MB (fits Instagram and jsDelivr).
"""
import json, subprocess, tempfile
from pathlib import Path
from PIL import Image

import brand

FPS = 30
MAX_MB = 14


def has_ffmpeg():
    try:
        subprocess.run(["ffmpeg", "-version"], capture_output=True, check=True)
        subprocess.run(["ffprobe", "-version"], capture_output=True, check=True)
        return True
    except Exception:
        return False


def probe(path):
    """(duration_s, width, height, has_audio) or None if it isn't a playable video."""
    try:
        out = subprocess.run(["ffprobe", "-v", "error", "-show_streams", "-show_format", "-of", "json", str(path)],
                             capture_output=True, text=True, timeout=60, check=True).stdout
        info = json.loads(out)
    except Exception:
        return None
    v = next((s for s in info.get("streams", []) if s.get("codec_type") == "video"), None)
    if not v:
        return None
    dur = float(info.get("format", {}).get("duration") or v.get("duration") or 0)
    audio = any(s.get("codec_type") == "audio" for s in info["streams"])
    return dur, int(v.get("width", 0)), int(v.get("height", 0)), audio


def _encode(args, out, crf):
    cmd = ["ffmpeg", "-y", "-v", "error"] + args + [
        "-c:v", "libx264", "-preset", "medium", "-crf", str(crf), "-profile:v", "high", "-level", "4.1",
        "-pix_fmt", "yuv420p", "-r", str(FPS), "-c:a", "aac", "-b:a", "128k", "-ar", "48000", "-ac", "2",
        "-movflags", "+faststart", str(out)]
    subprocess.run(cmd, check=True, capture_output=True, timeout=900)


def _encode_fit(args, out):
    for crf in (23, 26, 29, 32):
        _encode(args, out, crf)
        if Path(out).stat().st_size <= MAX_MB * 1024 * 1024:
            return
    # still too big: keep the smallest attempt anyway


def _overlay(slide, box_path):
    """Render the slide as an overlay PNG with a transparent video box. Returns (png, (x0,y0,x1,y1))."""
    box = brand.render_still(slide, box_path, brand.VIDEO)
    return str(box_path).rsplit(".", 1)[0] + ".png", box


def clip_reel(slide, clip, out, start=0.0, max_len=30.0):
    """Official clip inside the post card. slide: same dict as a card/headline still."""
    info = probe(clip)
    if not info:
        raise ValueError("not a playable video")
    dur, _, _, audio = info
    start = max(0.0, min(float(start or 0), max(0.0, dur - 3)))
    length = max(3.0, min(max_len, dur - start))
    with tempfile.TemporaryDirectory() as td:
        png, (x0, y0, x1, y1) = _overlay(slide, Path(td) / "ov.jpg")
        bw, bh = x1 - x0, y1 - y0
        fil = (f"[1:v]scale={bw}:{bh}:force_original_aspect_ratio=increase,crop={bw}:{bh},setsar=1,fps={FPS}[v];"
               f"color=c=black:s={brand.W}x{brand.H}:r={FPS}:d={length:.2f}[bg];"
               f"[bg][v]overlay={x0}:{y0}:shortest=1[b];[b][0:v]overlay=0:0,format=yuv420p[o]")
        args = ["-loop", "1", "-i", png, "-ss", f"{start:.2f}", "-t", f"{length:.2f}", "-i", str(clip)]
        if audio:
            args += ["-filter_complex", fil, "-map", "[o]", "-map", "1:a:0", "-t", f"{length:.2f}"]
        else:
            args += ["-f", "lavfi", "-t", f"{length:.2f}", "-i", "anullsrc=r=48000:cl=stereo",
                     "-filter_complex", fil, "-map", "[o]", "-map", "2:a", "-t", f"{length:.2f}"]
        _encode_fit(args, out)
    return out


def motion_reel(slide, image, out, seconds=9.0):
    """Slow zoom across the article picture inside the post card, silent audio track."""
    with tempfile.TemporaryDirectory() as td:
        png, (x0, y0, x1, y1) = _overlay(slide, Path(td) / "ov.jpg")
        bw, bh = x1 - x0, y1 - y0
        # oversized still so the zoom stays sharp
        big = brand.cover_crop(image, bw * 2, bh * 2)
        src = Path(td) / "pic.jpg"
        big.save(src, quality=95)
        frames = int(seconds * FPS)
        fil = (f"[1:v]zoompan=z='1+0.10*on/{frames}':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)'"
               f":d={frames}:s={bw}x{bh}:fps={FPS},setsar=1[v];"
               f"color=c=black:s={brand.W}x{brand.H}:r={FPS}:d={seconds:.2f}[bg];"
               f"[bg][v]overlay={x0}:{y0}:shortest=1[b];[b][0:v]overlay=0:0,format=yuv420p[o]")
        args = ["-loop", "1", "-i", png, "-i", str(src),
                "-f", "lavfi", "-t", f"{seconds:.2f}", "-i", "anullsrc=r=48000:cl=stereo",
                "-filter_complex", fil, "-map", "[o]", "-map", "2:a", "-t", f"{seconds:.2f}"]
        _encode_fit(args, out)
    return out
