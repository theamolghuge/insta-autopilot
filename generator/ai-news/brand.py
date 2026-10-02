"""Brand renderer for the AI news page.

Black background, white text, important words in yellow. Mark them with [square brackets]:
    "OpenAI ships [GPT-6] to everyone"

Every post covers ONE story. Slides are 1080 x 1350 (4:5):
  media_top  picture on the top 40%, text on the bottom 60%   (single post / carousel cover)
  text       text only                                         (single post without a picture)
  point      numbered point                                    (carousel inside)
  cta        sources + follow                                  (carousel end)

The look is a THEME (config.json -> "theme"). All themes share colours and rules; they differ in
typefaces, how the picture sits and how highlights are drawn.
"""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
import json

HERE = Path(__file__).resolve().parent
F = HERE / "fonts"
CONFIG = json.loads((HERE / "config.json").read_text())

W, H = 1080, 1350
MEDIA_H = int(H * 0.40)                  # 540 px

BG = (0, 0, 0)
WHITE = (255, 255, 255)
YELLOW = (255, 214, 10)                  # #FFD60A
GREY = (168, 168, 168)                   # body text
DIM = (110, 110, 110)                    # meta text
RULE = (40, 40, 40)

HANDLE = CONFIG["handle"]

# ------------------------------------------------------------------ themes
# font spec: (file, {axis: value}, tracking in em)
THEMES = {
    # Bold, condensed, all-caps headlines. Feels like a newsroom ticker.
    "newsroom": {
        "margin": 72,
        "head": ("Archivo.ttf", {"Weight": 800, "Width": 68}, -0.005), "head_case": "upper",
        "head_hl": None, "head_lead": 0.98, "head_sizes": [84, 78, 72, 66, 60, 56],
        "hl_style": "text",
        "body": ("Inter.ttf", {"Optical size": 24, "Weight": 400}, 0), "body_size": 40, "body_lead": 1.4,
        "label": ("Archivo.ttf", {"Weight": 700, "Width": 100}, 0.08), "label_size": 25,
        "mark": ("Archivo.ttf", {"Weight": 900, "Width": 100}, 0.04),
        "num": ("Archivo.ttf", {"Weight": 900, "Width": 62}, 0), "num_size": 180,
        "media": "hard",
    },
    # Clean product-launch look: tight sans, rounded inset picture, mono metadata.
    "minimal": {
        "margin": 64,
        "head": ("InterTight.ttf", {"Weight": 700}, -0.028), "head_case": None,
        "head_hl": None, "head_lead": 1.08, "head_sizes": [68, 64, 60, 56, 52, 48],
        "hl_style": "text",
        "body": ("Geist.ttf", {"Weight": 400}, -0.005), "body_size": 40, "body_lead": 1.42,
        "label": ("GeistMono.ttf", {"Weight": 500}, 0.02), "label_size": 24,
        "mark": ("InterTight.ttf", {"Weight": 800}, -0.01),
        "num": ("GeistMono.ttf", {"Weight": 600}, -0.02), "num_size": 30,
        "media": "inset",
    },
    # Magazine look: big serif headline, highlighted words in yellow italic.
    "editorial": {
        "margin": 80,
        "head": ("InstrumentSerif.ttf", {}, -0.012), "head_case": None,
        "head_hl": ("InstrumentSerif-Italic.ttf", {}, -0.01), "head_lead": 1.0,
        "head_sizes": [90, 84, 78, 72, 66, 62],
        "hl_style": "text",
        "body": ("Inter.ttf", {"Optical size": 24, "Weight": 400}, 0), "body_size": 40, "body_lead": 1.42,
        "label": ("InterTight.ttf", {"Weight": 600}, 0.14), "label_size": 23,
        "mark": ("InterTight.ttf", {"Weight": 700}, 0.16),
        "num": ("InstrumentSerif-Italic.ttf", {}, 0), "num_size": 170,
        "media": "fade",
    },
}
THEME_NAME = CONFIG.get("theme", "newsroom")
T = THEMES[THEME_NAME]
M = T["margin"]


def use_theme(name):
    global T, M, THEME_NAME
    THEME_NAME, T, M = name, THEMES[name], THEMES[name]["margin"]


# ------------------------------------------------------------------ fonts
_cache = {}


def _axis_name(a):
    return a["name"].decode() if isinstance(a["name"], bytes) else a["name"]


def font(spec, size):
    file, axes, trk = spec
    key = (file, tuple(sorted(axes.items())), size)
    if key not in _cache:
        f = ImageFont.truetype(str(F / file), size)
        if axes:
            cur = {_axis_name(a): a["default"] for a in f.get_variation_axes()}
            cur.update(axes)
            f.set_variation_by_axes([cur[_axis_name(a)] for a in f.get_variation_axes()])
        _cache[key] = f
    return _cache[key], trk * size


def clean(text):
    rep = {"‘": "'", "’": "'", "“": '"', "”": '"', "…": "...", " ": " "}
    for a, b in rep.items():
        text = text.replace(a, b)
    return " ".join(text.split())


def parse(text):
    """'a [b c] d' -> [(a, False), (b, True), (c, True), (d, False)]"""
    out, inside = [], False
    for tok in clean(text).split(" "):
        if tok.startswith("["):
            inside = True
        end = "]" in tok
        w = tok.replace("[", "").replace("]", "")
        if w:
            out.append((w, inside))
        if end:
            inside = False
    return out


def plain(text):
    return " ".join(w for w, _ in parse(text))


def wlen(f, trk, s):
    return f.getlength(s) + trk * max(0, len(s) - 1)


# ------------------------------------------------------------------ canvas
class Slide:
    def __init__(self, transparent=False):
        self.img = Image.new("RGBA", (W, H), (0, 0, 0, 0) if transparent else BG + (255,))
        self.d = ImageDraw.Draw(self.img)

    def word(self, x, y, s, f, trk, fill):
        if abs(trk) < 0.01:
            self.d.text((x, y), s, font=f, fill=fill)
            return
        for i, ch in enumerate(s):                       # keeps kerning: position by prefix width
            self.d.text((x + f.getlength(s[:i]) + trk * i, y), ch, font=f, fill=fill)

    def _lines(self, words, spec, hl_spec, size, maxw, case):
        f, trk = font(spec, size)
        fh, trkh = font(hl_spec, size) if hl_spec else (f, trk)
        sp = f.getlength(" ")
        lines, cur, w = [], [], 0
        for wd, h in words:
            if case == "upper":
                wd = wd.upper()
            ff, tt = (fh, trkh) if h else (f, trk)
            l = wlen(ff, tt, wd)
            if cur and w + sp + l > maxw:
                lines.append(cur); cur, w = [], 0
            w += (sp if cur else 0) + l
            cur.append((wd, h, l, ff, tt))
        if cur:
            lines.append(cur)
        return lines, sp

    def rich(self, text, spec, size, y, lead, x=None, maxw=None, color=WHITE, hl_spec=None, case=None,
             max_lines=None, hl_style="text", center=False):
        x = M if x is None else x
        maxw = W - 2 * M if maxw is None else maxw
        lines, sp = self._lines(parse(text), spec, hl_spec, size, maxw, case)
        if max_lines and len(lines) > max_lines:
            lines = lines[:max_lines]
            wd, h, l, ff, tt = lines[-1][-1]
            lines[-1][-1] = (wd.rstrip(".,;:") + "...", h, l, ff, tt)
        step = int(size * lead)
        f0, _ = font(spec, size)
        asc, desc = f0.getmetrics()
        for i, line in enumerate(lines):
            lw = sum(t[2] for t in line) + sp * (len(line) - 1)
            cx = x + (maxw - lw) / 2 if center else x
            yy = y + i * step
            if hl_style == "marker":                     # yellow block behind runs of highlighted words
                k = 0
                while k < len(line):
                    if line[k][1]:
                        j, x0 = k, cx + sum(t[2] for t in line[:k]) + sp * k
                        while j + 1 < len(line) and line[j + 1][1]:
                            j += 1
                        x1 = cx + sum(t[2] for t in line[:j + 1]) + sp * j
                        self.d.rectangle([x0 - size * 0.12, yy + asc * 0.12, x1 + size * 0.12,
                                          yy + asc + desc * 0.25], fill=YELLOW + (255,))
                        k = j + 1
                    else:
                        k += 1
            for wd, h, l, ff, tt in line:
                col = (BG if hl_style == "marker" else YELLOW) if h else color
                self.word(cx, yy, wd, ff, tt, col + (255,))
                cx += l + sp
        return y + len(lines) * step

    def measure(self, text, spec, size, lead, maxw=None, hl_spec=None, case=None):
        maxw = W - 2 * M if maxw is None else maxw
        lines, _ = self._lines(parse(text), spec, hl_spec, size, maxw, case)
        return len(lines) * int(size * lead), len(lines)

    def fit_head(self, text, max_h, max_lines=5, maxw=None):
        for s in T["head_sizes"]:
            h, n = self.measure(text, T["head"], s, T["head_lead"], maxw, T["head_hl"], T["head_case"])
            if h <= max_h and n <= max_lines:
                return s
        return T["head_sizes"][-1]

    def head(self, text, size, y, maxw=None):
        return self.rich(text, T["head"], size, y, T["head_lead"], maxw=maxw, hl_spec=T["head_hl"],
                         case=T["head_case"], hl_style=T["hl_style"])

    def body(self, text, y, max_y, size=None):
        size = size or T["body_size"]
        lead = T["body_lead"]
        n = max(1, int((max_y - y) // (size * lead)))
        return self.rich(text, T["body"], size, y, lead, color=GREY, max_lines=n)

    def label(self, text, x, y, color=WHITE, spec=None, size=None, anchor="la", upper=True):
        spec = spec or T["label"]
        f, trk = font(spec, size or T["label_size"])
        text = text.upper() if upper else text
        tw = wlen(f, trk, text)
        x = x - tw if anchor == "ra" else x
        self.word(x, y, text, f, trk, color + (255,))
        return tw

    def mark(self, x, y, on_media=False):
        """Brand mark: AI NEWS with the yellow square / dot."""
        if THEME_NAME == "newsroom":
            f, trk = font(T["mark"], 26)
            tw = wlen(f, trk, "AI NEWS")
            if on_media:
                self.d.rectangle([x - 14, y - 12, x + 34 + tw + 14, y + 40], fill=BG + (255,))
            self.d.rectangle([x, y + 4, x + 20, y + 24], fill=YELLOW + (255,))
            self.word(x + 34, y - 1, "AI NEWS", f, trk, WHITE + (255,))
        elif THEME_NAME == "minimal":
            f, trk = font(T["mark"], 26)
            tw = wlen(f, trk, "AI News")
            if on_media:
                self.d.rounded_rectangle([x - 16, y - 12, x + 30 + tw + 18, y + 42], 27, fill=(0, 0, 0, 190))
            self.d.ellipse([x, y + 7, x + 16, y + 23], fill=YELLOW + (255,))
            self.word(x + 28, y - 2, "AI News", f, trk, WHITE + (255,))
        else:
            f, trk = font(T["mark"], 22)
            tw = wlen(f, trk, "AI NEWS")
            self.word(x, y, "AI NEWS", f, trk, WHITE + (255,))
            self.d.ellipse([x + tw + 10, y + 6, x + tw + 22, y + 18], fill=YELLOW + (255,))

    def footer(self, right=None, right_color=DIM):
        y = H - 84
        self.d.line([(M, y - 30), (W - M, y - 30)], fill=RULE + (255,), width=2)
        self.label(HANDLE, M, y, color=WHITE, upper=THEME_NAME != "minimal")
        if right:
            self.label(right, W - M, y, color=right_color, anchor="ra", upper=THEME_NAME != "minimal")


# ------------------------------------------------------------------ media
def cover_crop(img, w, h):
    img = img.convert("RGB")
    s = max(w / img.width, h / img.height)
    r = img.resize((int(img.width * s + 0.5), int(img.height * s + 0.5)), Image.LANCZOS)
    x, y = (r.width - w) // 2, int((r.height - h) * 0.35)   # bias up: faces/products sit high
    return r.crop((x, y, x + w, y + h))


def ramp(h, start, end):
    m = Image.new("L", (1, h), 0)
    for y in range(h):
        t = 0 if y <= start else 1 if y >= end else (y - start) / (end - start)
        m.putpixel((0, y), int(255 * t * t * (3 - 2 * t)))
    return m.resize((W, h))


def place_media(base, media):
    style = T["media"]
    if style == "inset":
        pad = M - 16
        w, h = W - 2 * pad, MEDIA_H - pad
        pic = cover_crop(media, w, h)
        mask = Image.new("L", (w, h), 0)
        ImageDraw.Draw(mask).rounded_rectangle([0, 0, w - 1, h - 1], 30, fill=255)
        base.paste(pic, (pad, pad), mask)
        return
    pic = cover_crop(media, W, MEDIA_H)
    base.paste(pic, (0, 0))
    if style == "fade":
        black = Image.new("RGB", (W, MEDIA_H), BG)
        region = base.crop((0, 0, W, MEDIA_H))
        base.paste(Image.composite(black, region, ramp(MEDIA_H, MEDIA_H - 220, MEDIA_H)), (0, 0))
    # soft top shade so the brand mark reads on bright photos
    top = Image.new("RGB", (W, 160), BG)
    region = base.crop((0, 0, W, 160))
    m = ramp(160, 0, 160).point(lambda v: int((255 - v) * 0.55))
    base.paste(Image.composite(top, region, m), (0, 0))


# ------------------------------------------------------------------ slides
def _meta(sl, s, y):
    """Category + source line above the headline. Returns y below it."""
    cat, src = s.get("kicker") or "", s.get("source") or ""
    if THEME_NAME == "minimal":
        f, trk = font(T["label"], 24)
        tw = wlen(f, trk, cat)
        sl.d.rounded_rectangle([M, y, M + tw + 36, y + 50], 25, outline=YELLOW + (255,), width=2)
        sl.word(M + 18, y + 9, cat, f, trk, YELLOW + (255,))
        if src:
            sl.label(src + (" · " + s["date"].title() if s.get("date") else ""), M + tw + 56, y + 10,
                     color=DIM, upper=False)
        return y + 50 + 34
    sl.label(cat, M, y, color=YELLOW)
    if src:
        f, trk = font(T["label"], T["label_size"])
        sep = "  /  " if THEME_NAME == "newsroom" else "  —  "
        sl.label(sep + src, M + wlen(f, trk, cat.upper()), y, color=DIM)
    return y + T["label_size"] + (30 if THEME_NAME == "newsroom" else 36)


def _right(s):
    if s.get("page"):
        return (s["page"],)
    if s.get("swipe"):
        return ("Swipe  →" if THEME_NAME == "minimal" else "SWIPE  →", YELLOW)
    return (s.get("date") or "",)


def _media_top(sl, s):
    sl.mark(M, 48 if T["media"] != "inset" else 84, on_media=True)
    if s.get("credit"):                                  # who the photo belongs to, on the photo
        f, trk = font(T["label"], 17)
        txt = s["credit"][:40].upper()
        tw = wlen(f, trk, txt)
        x1, y1 = W - M - 4, MEDIA_H - 40
        sl.d.rounded_rectangle([x1 - tw - 24, y1 - 8, x1, y1 + 26], 17, fill=(0, 0, 0, 170))
        sl.word(x1 - tw - 12, y1 - 1, txt, f, trk, (200, 200, 200, 255))
    y = MEDIA_H + (54 if T["media"] != "inset" else 40)
    y = _meta(sl, s, y)
    bottom = H - 148
    body = s.get("body") or ""
    room = bottom - y - (240 if body else 0)
    hs = sl.fit_head(s["headline"], room, 4)
    y = sl.head(s["headline"], hs, y) + {"newsroom": 30, "minimal": 34, "editorial": 44}[THEME_NAME]
    if body and bottom - y > T["body_size"] * 1.3:
        sl.body(body, y, bottom)
    sl.footer(*_right(s))


def _text(sl, s):
    sl.mark(M, 64)
    body = s.get("body") or ""
    top, bottom = 190, H - 160
    hs = sl.fit_head(s["headline"], int((bottom - top) * 0.66), 6)
    hh, _ = sl.measure(s["headline"], T["head"], hs, T["head_lead"], None, T["head_hl"], T["head_case"])
    bh = sl.measure(body, T["body"], T["body_size"], T["body_lead"])[0] if body else 0
    block = 70 + hh + (60 + bh if body else 0)
    y = max(top, top + (bottom - top - block) // 2 - 30)
    y = _meta(sl, s, y)
    y = sl.head(s["headline"], hs, y) + 36
    if body:
        sl.d.rectangle([M, y, M + 56, y + 5], fill=YELLOW + (255,))
        sl.body(body, y + 34, bottom)
    sl.footer(*_right(s))


def _point(sl, s):
    sl.mark(M, 64)
    num = s.get("num", "01")
    hs = min(sl.fit_head(s["headline"], 260, 3), T["head_sizes"][1])
    hh, _ = sl.measure(s["headline"], T["head"], hs, T["head_lead"], None, T["head_hl"], T["head_case"])
    bsize = T["body_size"] + 2
    bh = sl.measure(s.get("body") or "", T["body"], bsize, T["body_lead"])[0] if s.get("body") else 0
    num_h = 80 if THEME_NAME == "minimal" else int(T["num_size"] * 1.05)
    block = num_h + hh + 40 + bh
    y = max(170, (H - block) // 2 - 40)
    if THEME_NAME == "minimal":
        f, trk = font(T["num"], 30)
        sl.word(M, y, num, f, trk, YELLOW + (255,))
        sl.word(M + wlen(f, trk, num) + 8, y, "/ " + s.get("of", "03"), f, trk, DIM + (255,))
    else:
        f, trk = font(T["num"], T["num_size"])
        sl.word(M - (6 if THEME_NAME == "newsroom" else 0), y, num, f, trk, YELLOW + (255,))
    y += num_h
    y = sl.head(s["headline"], hs, y) + 40
    if s.get("body"):
        sl.body(s["body"], y, H - 160, size=bsize)
    sl.footer(*_right(s))


def _cta(sl, s):
    sl.mark(M, 64)
    y = 330
    y = sl.head(s.get("headline", "Follow for [AI news] every 3 hours"), T["head_sizes"][1], y) + 40
    sl.body(s.get("body", "One story at a time, sources on every post. Save this and share it with someone who builds with AI."),
            y, y + 200)
    y = H - 330
    sl.label("Sources", M, y, color=YELLOW)
    y += 46
    for src in (s.get("sources") or [])[:4]:
        sl.label(src, M, y, color=GREY, spec=T["body"], size=30, upper=False)
        y += 44
    sl.footer(*_right(s))


def render_still(s, path, media=None):
    base = Image.new("RGB", (W, H), BG)
    if media is not None and s["layout"] == "media_top":
        place_media(base, media)
    sl = Slide(transparent=True)
    {"media_top": _media_top, "text": _text, "point": _point, "cta": _cta}[s["layout"]](sl, s)
    base = base.convert("RGBA")
    base.alpha_composite(sl.img)
    base.convert("RGB").save(path, quality=90, optimize=True)
