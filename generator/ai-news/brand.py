"""Brand renderer for the AI news page.

Look: black background, white text, important words in yellow.
Markup: wrap highlighted words in [square brackets], e.g. "OpenAI ships [GPT-6] today".

Fonts (all OFL, bundled in ./fonts):
  Space Grotesk Bold  -> headlines and big numbers
  Inter               -> body text
  JetBrains Mono      -> labels: category tag, date, handle, page counter

Every slide is 1080 x 1350 (4:5). Layouts:
  media_top  top 40% is a picture or video, bottom 60% is text
  text       text only (headline + body)
  point      numbered point inside a carousel
  roundup    numbered list of several headlines (cover of a roundup carousel)
  cta        last carousel slide: source + follow line
  full_media whole slide is a picture/video, text sits on a dark gradient at the bottom
"""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import json

HERE = Path(__file__).resolve().parent
F = HERE / "fonts"
CONFIG = json.loads((HERE / "config.json").read_text())

W, H = 1080, 1350
MEDIA_H = int(H * 0.40)          # 540 px: the "top 40%" media area
M = 80                           # side margin

BG = (0, 0, 0)
WHITE = (255, 255, 255)
SOFT = (214, 214, 214)           # body text, slightly softer than headlines
YELLOW = (255, 214, 10)          # #FFD60A
MUTED = (128, 128, 128)
RULE = (38, 38, 38)

HANDLE = CONFIG["handle"]
BRAND_NAME = CONFIG.get("brand_name", "AI NEWS")


# ---------------------------------------------------------------- fonts
_cache = {}


def font(kind, size):
    key = (kind, size)
    if key in _cache:
        return _cache[key]
    if kind == "head":
        f = ImageFont.truetype(str(F / "SpaceGrotesk.ttf"), size); f.set_variation_by_axes([700])
    elif kind == "head_med":
        f = ImageFont.truetype(str(F / "SpaceGrotesk.ttf"), size); f.set_variation_by_axes([500])
    elif kind == "body":
        f = ImageFont.truetype(str(F / "Inter.ttf"), size); f.set_variation_by_axes([min(32, max(14, size // 2)), 400])
    elif kind == "body_bold":
        f = ImageFont.truetype(str(F / "Inter.ttf"), size); f.set_variation_by_axes([min(32, max(14, size // 2)), 650])
    elif kind == "mono":
        f = ImageFont.truetype(str(F / "JetBrainsMono.ttf"), size); f.set_variation_by_axes([500])
    elif kind == "mono_bold":
        f = ImageFont.truetype(str(F / "JetBrainsMono.ttf"), size); f.set_variation_by_axes([800])
    else:
        raise ValueError(kind)
    _cache[key] = f
    return f


def clean(text):
    """Swap characters the brand fonts may not have."""
    rep = {"‘": "'", "’": "'", "“": '"', "”": '"', "…": "...", " ": " "}
    for a, b in rep.items():
        text = text.replace(a, b)
    return " ".join(text.split())


def parse(text):
    """'a [b c] d' -> [(a, False), (b, True), (c, True), (d, False)]"""
    out, inside = [], False
    for tok in clean(text).split(" "):
        if not tok:
            continue
        if tok.startswith("["):
            inside = True
        end = "]" in tok
        word = tok.replace("[", "").replace("]", "")
        if word:
            out.append((word, inside))
        if end:
            inside = False
    return out


def plain(text):
    return " ".join(w for w, _ in parse(text))


def layout(text, f, maxw):
    words = parse(text)
    sp = f.getlength(" ")
    lines, cur, w = [], [], 0
    for wd, h in words:
        l = f.getlength(wd)
        if cur and w + sp + l > maxw:
            lines.append(cur); cur, w = [], 0
        w += (sp if cur else 0) + l
        cur.append((wd, h, l))
    if cur:
        lines.append(cur)
    return lines


class Slide:
    """Draws text onto a black (or transparent) canvas. Media is pasted separately."""

    def __init__(self, transparent=False):
        self.img = Image.new("RGBA", (W, H), (0, 0, 0, 0) if transparent else BG + (255,))
        self.d = ImageDraw.Draw(self.img)

    # text with [highlight] support. returns bottom y
    def rich(self, text, kind, size, y, x=M, maxw=W - 2 * M, color=WHITE, hl=YELLOW, lh=1.2, max_lines=None):
        f = font(kind, size)
        lines = layout(text, f, maxw)
        if max_lines and len(lines) > max_lines:
            lines = lines[:max_lines]
            last = lines[-1]
            wd, h, l = last[-1]
            last[-1] = (wd.rstrip(".,;:") + "...", h, l)
        sp = f.getlength(" ")
        step = int(size * lh)
        for i, line in enumerate(lines):
            cx = x
            for wd, h, l in line:
                self.d.text((cx, y + i * step), wd, font=f, fill=(hl if h else color) + (255,))
                cx += l + sp
        return y + len(lines) * step

    def height(self, text, kind, size, maxw=W - 2 * M, lh=1.2):
        return len(layout(text, font(kind, size), maxw)) * int(size * lh)

    def fit(self, text, kind, sizes, max_h, maxw=W - 2 * M, lh=1.2):
        for s in sizes:
            if self.height(text, kind, s, maxw, lh) <= max_h:
                return s
        return sizes[-1]

    def label(self, text, x, y, kind="mono", size=24, color=WHITE, anchor="la", tracking=2):
        f = font(kind, size)
        text = text.upper() if kind.startswith("mono") else text
        total = sum(f.getlength(c) for c in text) + tracking * (len(text) - 1)
        cx = x - total if anchor == "ra" else x
        for c in text:
            self.d.text((cx, y), c, font=f, fill=color + (255,))
            cx += f.getlength(c) + tracking
        return total

    def tag(self, text, x, y, size=22):
        """Yellow pill with black mono text: the category tag."""
        f = font("mono_bold", size)
        text = text.upper()
        tw = sum(f.getlength(c) + 2 for c in text) - 2
        self.d.rounded_rectangle([x, y, x + tw + 28, y + size + 22], 6, fill=YELLOW + (255,))
        self.label(text, x + 14, y + 9, kind="mono_bold", size=size, color=BG, tracking=2)
        return x + tw + 28

    def header(self, y=56, date=None, on_media=False):
        """Brand mark left, date right. On top of media we put a dark strip behind it."""
        if on_media:
            strip = Image.new("RGBA", (W, 190), (0, 0, 0, 0))
            sd = ImageDraw.Draw(strip)
            for i in range(190):
                t = max(0.0, (i - 70) / 120)
                sd.line([(0, i), (W, i)], fill=(0, 0, 0, int(215 * (1 - t * t))))
            self.img.alpha_composite(strip, (0, 0))
        self.d.ellipse([M, y + 6, M + 16, y + 22], fill=YELLOW + (255,))
        self.label(BRAND_NAME, M + 30, y, kind="mono_bold", size=24)
        if date:
            self.label(date, W - M, y, kind="mono", size=22, color=SOFT if on_media else MUTED, anchor="ra")

    def footer(self, source=None, page=None, swipe=False):
        y = H - 92
        self.d.line([(M, y - 26), (W - M, y - 26)], fill=RULE + (255,), width=2)
        self.label(HANDLE, M, y, kind="mono", size=22, color=WHITE, tracking=1)
        right = None
        if page:
            right = page
        elif swipe:
            right = "SWIPE  ->"
        elif source:
            right = "VIA " + source
        if right:
            col = YELLOW if swipe and not page else MUTED
            self.label(right[:34], W - M, y, kind="mono", size=22, color=col, anchor="ra", tracking=1)


# ---------------------------------------------------------------- media helpers
def cover_crop(img, w, h, zoom=1.0, pan=(0.5, 0.5)):
    """Scale img to cover w x h (times zoom) and crop around pan point."""
    img = img.convert("RGB")
    s = max(w / img.width, h / img.height) * zoom
    nw, nh = int(img.width * s + 0.5), int(img.height * s + 0.5)
    r = img.resize((nw, nh), Image.LANCZOS)
    x = int((nw - w) * pan[0]); y = int((nh - h) * pan[1])
    return r.crop((x, y, x + w, y + h))


def fade_mask(w, h, start, end, top_alpha=0, bottom_alpha=255):
    """Vertical alpha ramp: transparent above `start`, solid black below `end`."""
    m = Image.new("L", (w, h), top_alpha)
    d = ImageDraw.Draw(m)
    for y in range(h):
        if y <= start:
            a = top_alpha
        elif y >= end:
            a = bottom_alpha
        else:
            t = (y - start) / (end - start)
            a = int(top_alpha + (bottom_alpha - top_alpha) * (t * t * (3 - 2 * t)))
        d.line([(0, y), (w, y)], fill=a)
    return m


def media_frame(media, layout_name, zoom=1.0, pan=(0.5, 0.5)):
    """Black canvas with the media placed for the given layout (no text). RGB."""
    base = Image.new("RGB", (W, H), BG)
    if media is None:
        return base
    if layout_name == "full_media":
        pic = cover_crop(media, W, H, zoom, pan)
        base.paste(pic, (0, 0))
        shade = Image.new("RGB", (W, H), BG)
        base = Image.composite(shade, base, fade_mask(W, H, int(H * 0.30), int(H * 0.70), 40, 235))
    else:
        pic = cover_crop(media, W, MEDIA_H, zoom, pan)
        base.paste(pic, (0, 0))
        shade = Image.new("RGB", (W, MEDIA_H), BG)
        region = base.crop((0, 0, W, MEDIA_H))
        region = Image.composite(shade, region, fade_mask(W, MEDIA_H, MEDIA_H - 170, MEDIA_H, 0, 255))
        base.paste(region, (0, 0))
    return base


# ---------------------------------------------------------------- slide text layers
# Each returns an RGBA layer (transparent where media should show) so the same text
# can sit on a still picture or on every frame of a video.

def text_layer(s):
    L = s["layout"]
    fn = {"media_top": _media_top, "full_media": _full_media, "text": _text,
          "point": _point, "roundup": _roundup, "cta": _cta}[L]
    has_media = L in ("media_top", "full_media")
    sl = Slide(transparent=has_media)
    fn(sl, s)
    return sl.img


def _media_top(sl, s):
    sl.header(date=s.get("date"), on_media=True)
    if s.get("credit"):
        sl.label(s["credit"][:40], W - M, MEDIA_H - 34, kind="mono", size=16, color=SOFT, anchor="ra", tracking=1)
    y = MEDIA_H + 10
    if s.get("kicker"):
        sl.tag(s["kicker"], M, y)
        y += 78
    bottom_limit = H - 150
    body = s.get("body") or ""
    head = s["headline"]
    room = bottom_limit - y
    hs = sl.fit(head, "head", [76, 70, 64, 58, 52], int(room * (0.62 if body else 1.0)), lh=1.12)
    y = sl.rich(head, "head", hs, y, lh=1.12) + 24
    if body:
        bs = sl.fit(body, "body", [36, 34, 32, 30], bottom_limit - y, lh=1.42)
        sl.rich(body, "body", bs, y, color=SOFT, lh=1.42, max_lines=max(1, (bottom_limit - y) // int(bs * 1.42)))
    sl.footer(source=s.get("source"), page=s.get("page"), swipe=s.get("swipe"))


def _full_media(sl, s):
    sl.header(date=s.get("date"), on_media=True)
    body = s.get("body") or ""
    head = s["headline"]
    hs = sl.fit(head, "head", [84, 76, 70, 64, 58], 420, lh=1.1)
    hh = sl.height(head, "head", hs, lh=1.1)
    bs = 34
    bh = min(sl.height(body, "body", bs, lh=1.42), int(bs * 1.42) * 3) if body else 0
    y = H - 150 - bh - (24 if body else 0) - hh - 78
    if s.get("kicker"):
        sl.tag(s["kicker"], M, y)
    y += 78
    y = sl.rich(head, "head", hs, y, lh=1.1) + 24
    if body:
        sl.rich(body, "body", bs, y, color=SOFT, lh=1.42, max_lines=3)
    sl.footer(source=s.get("source"), page=s.get("page"), swipe=s.get("swipe"))


def _text(sl, s):
    sl.header(date=s.get("date"))
    head, body = s["headline"], s.get("body") or ""
    top, bottom = 200, H - 160
    hs = sl.fit(head, "head", [104, 96, 88, 80, 72, 64], int((bottom - top) * (0.6 if body else 0.9)), lh=1.08)
    hh = sl.height(head, "head", hs, lh=1.08)
    bs = sl.fit(body, "body", [40, 38, 36, 34], bottom - top - hh - 140, lh=1.42) if body else 0
    bh = sl.height(body, "body", bs, lh=1.42) if body else 0
    total = 78 + hh + (40 + bh if body else 0)
    y = max(top, top + (bottom - top - total) // 2 - 20)
    if s.get("kicker"):
        sl.tag(s["kicker"], M, y)
    y += 78
    y = sl.rich(head, "head", hs, y, lh=1.08) + 40
    if body:
        sl.d.line([(M, y - 14), (M + 64, y - 14)], fill=YELLOW + (255,), width=4)
        sl.rich(body, "body", bs, y + 16, color=SOFT, lh=1.42)
    sl.footer(source=s.get("source"), page=s.get("page"), swipe=s.get("swipe"))


def _point(sl, s):
    sl.header(date=s.get("date"))
    head, body = s["headline"], s.get("body") or ""
    hs = sl.fit(head, "head", [76, 70, 64, 58], 330, lh=1.12)
    hh = sl.height(head, "head", hs, lh=1.12)
    bs = sl.fit(body, "body", [40, 38, 36, 34, 32], 520, lh=1.45) if body else 0
    bh = sl.height(body, "body", bs, lh=1.45) if body else 0
    total = 150 + hh + 40 + bh
    y = max(190, (H - total) // 2 - 20)
    sl.label(s.get("num", "01"), M, y, kind="mono_bold", size=96, color=YELLOW, tracking=0)
    y += 150
    y = sl.rich(head, "head", hs, y, lh=1.12) + 40
    if body:
        sl.rich(body, "body", bs, y, color=SOFT, lh=1.45)
    sl.footer(source=s.get("source"), page=s.get("page"), swipe=s.get("swipe"))


def _roundup(sl, s):
    sl.header(date=s.get("date"))
    y = 170
    sl.tag(s.get("kicker", "AI Brief"), M, y)
    y += 92
    y = sl.rich(s["headline"], "head", 84, y, lh=1.05) + 36
    items = s.get("items", [])[:5]
    room = H - 170 - y
    each = room // max(1, len(items))
    size = 40 if each >= 170 else 36 if each >= 140 else 32
    for i, it in enumerate(items, 1):
        sl.d.line([(M, y), (W - M, y)], fill=RULE + (255,), width=2)
        sl.label(f"{i:02d}", M, y + 26, kind="mono_bold", size=30, color=YELLOW, tracking=0)
        sl.rich(it, "head_med", size, y + 20, x=M + 90, maxw=W - 2 * M - 90, lh=1.18, max_lines=3)
        y += each
    sl.footer(page=s.get("page"), swipe=s.get("swipe"))


def _cta(sl, s):
    sl.header(date=s.get("date"))
    y = 300
    sl.label("SOURCES", M, y, kind="mono_bold", size=24, color=YELLOW)
    y += 54
    for src in (s.get("sources") or [])[:5]:
        y = sl.rich(src, "body", 36, y, color=SOFT, lh=1.35) + 6
    y = max(y + 90, 720)
    y = sl.rich(s.get("headline", "Follow for [AI news every 3 hours.]"), "head", 76, y, lh=1.1) + 30
    sl.rich(s.get("body", "Save this. Share it with someone who builds with AI."), "body", 36, y, color=SOFT, lh=1.4)
    sl.footer(page=s.get("page"))


# ---------------------------------------------------------------- render a still
def render_still(s, path, media=None):
    """media: PIL image (for media_top / full_media) or None."""
    base = media_frame(media, s["layout"]).convert("RGBA")
    base.alpha_composite(text_layer(s))
    base.convert("RGB").save(path, quality=88, optimize=True)
