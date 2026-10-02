"""Brand renderer for the AI news page.

Black background, white text, key words in yellow. Mark them with [square brackets]:
    "OpenAI ships [GPT-6] to everyone"

Every post covers ONE story. Slides are 1080 x 1350 (4:5). Two templates:

  card      "post card": logo + name + handle at the top, one or two sentences, then the picture
            filling the rest of the slide. Without a picture the text sits centred, larger.
            Used for single posts and for the inside slides of a carousel.
  headline  carousel cover: picture on top, brand line, big centred ALL-CAPS headline, "SWIPE FOR MORE".

Either template can hold a video instead of a picture (see video.py): same layout, the clip plays
where the picture would be.

Typography: Inter Tight (headlines + card text), Geist (handle), Geist Mono (small labels). All OFL.
"""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
import json

HERE = Path(__file__).resolve().parent
F = HERE / "fonts"
CONFIG = json.loads((HERE / "config.json").read_text())

W, H = 1080, 1350
MIN_MEDIA = int(H * 0.40)                # a picture always gets at least 40% of the slide

BG = (0, 0, 0)
WHITE = (255, 255, 255)
YELLOW = (255, 214, 10)                  # #FFD60A
GREY = (140, 140, 140)
RULE = (70, 70, 70)

HANDLE = CONFIG["handle"]
NAME = CONFIG.get("display_name", "AI News")
PAD = 64

# (file, {axis: value}, tracking in em)
HEAD = ("InterTight.ttf", {"Weight": 900}, -0.01)        # cover headline, upper case
CARD = ("InterTight.ttf", {"Weight": 500}, -0.012)       # card sentence
CARD_HL = ("InterTight.ttf", {"Weight": 700}, -0.012)    # highlighted words in the card
NAME_F = ("InterTight.ttf", {"Weight": 700}, -0.01)
HANDLE_F = ("Geist.ttf", {"Weight": 400}, 0)
LABEL = ("GeistMono.ttf", {"Weight": 600}, 0.12)

_cache = {}


def _axis(a):
    return a["name"].decode() if isinstance(a["name"], bytes) else a["name"]


def font(spec, size):
    file, axes, trk = spec
    key = (file, tuple(sorted(axes.items())), size)
    if key not in _cache:
        f = ImageFont.truetype(str(F / file), size)
        if axes:
            cur = {_axis(a): a["default"] for a in f.get_variation_axes()}
            cur.update(axes)
            f.set_variation_by_axes([cur[_axis(a)] for a in f.get_variation_axes()])
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


# ------------------------------------------------------------------ text engine
class Canvas:
    def __init__(self):
        self.img = Image.new("RGB", (W, H), BG)
        self.d = ImageDraw.Draw(self.img)
        self.alpha = None            # set by hole(): this slide is an overlay for a video
        self._credit = None

    def word(self, x, y, s, f, trk, fill):
        if abs(trk) < 0.01:
            self.d.text((x, y), s, font=f, fill=fill)
            return
        for i, ch in enumerate(s):                       # tracking that keeps kerning
            self.d.text((x + f.getlength(s[:i]) + trk * i, y), ch, font=f, fill=fill)

    def lines(self, text, spec, hl_spec, size, maxw, upper=False):
        f, trk = font(spec, size)
        fh, trkh = font(hl_spec or spec, size)
        sp = f.getlength(" ")
        out, cur, w = [], [], 0
        for wd, h in parse(text):
            wd = wd.upper() if upper else wd
            ff, tt = (fh, trkh) if h else (f, trk)
            l = wlen(ff, tt, wd)
            if cur and w + sp + l > maxw:
                out.append(cur); cur, w = [], 0
            w += (sp if cur else 0) + l
            cur.append((wd, h, l, ff, tt))
        if cur:
            out.append(cur)
        return out, sp

    def block_h(self, text, spec, hl_spec, size, lead, maxw, upper=False):
        ls, _ = self.lines(text, spec, hl_spec, size, maxw, upper)
        return len(ls) * int(size * lead), len(ls)

    def draw(self, text, spec, hl_spec, size, lead, x, y, maxw, upper=False, center=False, color=WHITE):
        ls, sp = self.lines(text, spec, hl_spec, size, maxw, upper)
        step = int(size * lead)
        for i, line in enumerate(ls):
            lw = sum(t[2] for t in line) + sp * (len(line) - 1)
            cx = x + (maxw - lw) / 2 if center else x
            for wd, h, l, ff, tt in line:
                self.word(cx, y + i * step, wd, ff, tt, YELLOW if h else color)
                cx += l + sp
        return y + len(ls) * step

    def label(self, text, x, y, size=20, color=GREY, anchor="la", spec=LABEL):
        f, trk = font(spec, size)
        tw = wlen(f, trk, text)
        x = x - tw if anchor == "ra" else x - tw / 2 if anchor == "ma" else x
        self.word(x, y, text, f, trk, color)
        return tw

    # ---------------------------------------------------------- brand pieces
    def avatar(self, x, y, d=88):
        """Round profile mark: 'AI' + yellow dot, same as the Instagram profile picture."""
        self.d.ellipse([x, y, x + d, y + d], fill=(14, 14, 14), outline=(60, 60, 60), width=2)
        f, _ = font(("InterTight.ttf", {"Weight": 800}, 0), int(d * 0.40))
        tw = f.getlength("AI")
        r = d * 0.075
        total = tw + d * 0.05 + 2 * r
        x0 = x + (d - total) / 2
        self.d.text((x0, y + d / 2), "AI", font=f, fill=WHITE, anchor="lm")
        cx, cy = x0 + tw + d * 0.05 + r, y + d / 2 + d * 0.10
        self.d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=YELLOW)

    def header(self, y=PAD):
        self.avatar(PAD, y)
        f, trk = font(NAME_F, 34)
        self.word(PAD + 110, y + 6, NAME, f, trk, WHITE)
        f2, trk2 = font(HANDLE_F, 28)
        self.word(PAD + 110, y + 50, HANDLE, f2, trk2, GREY)
        return y + 88

    def brand_line(self, y):
        """—— AI NEWS • ——  centred rule with the wordmark."""
        f, trk = font(("InterTight.ttf", {"Weight": 800}, 0.14), 22)
        txt = "AI NEWS"
        tw = wlen(f, trk, txt) + 18
        x0 = (W - tw) / 2
        self.word(x0, y - 13, txt, f, trk, WHITE)
        self.d.ellipse([x0 + tw - 10, y - 4, x0 + tw, y + 6], fill=YELLOW)
        self.d.line([(PAD, y), (x0 - 22, y)], fill=RULE, width=2)
        self.d.line([(x0 + tw + 22, y), (W - PAD, y)], fill=RULE, width=2)

    def credit(self, text, x1, y1):
        self._credit = (text, x1, y1)            # drawn last, on top of picture or video

    def _draw_credit(self, img):
        text, x1, y1 = self._credit
        f, trk = font(LABEL, 16)
        text = text.upper()[:40]
        tw = wlen(f, trk, text)
        layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        ld = ImageDraw.Draw(layer)
        ld.rounded_rectangle([x1 - tw - 28, y1 - 34, x1 - 1, y1 - 1], 17, fill=(0, 0, 0, 165))
        tmp = Canvas.__new__(Canvas); tmp.d = ld
        Canvas.word(tmp, x1 - tw - 14, y1 - 27, text, f, trk, (210, 210, 210, 255))
        return Image.alpha_composite(img.convert("RGBA"), layer)

    def hole(self, y0, y1, fade_top=0, fade_bottom=0):
        """Make rows y0..y1 transparent (a video plays there), fading to black at the edges."""
        if self.alpha is None:
            self.alpha = Image.new("L", (W, H), 255)
        h = y1 - y0
        col = Image.new("L", (1, h), 0)
        for yy in range(h):
            a = 0
            if fade_top and yy < fade_top:
                t = 1 - yy / fade_top; a = max(a, int(255 * t * t * (3 - 2 * t)))
            if fade_bottom and yy > h - fade_bottom:
                t = 1 - (h - yy) / fade_bottom; a = max(a, int(255 * t * t * (3 - 2 * t)))
            col.putpixel((0, yy), a)
        self.alpha.paste(col.resize((W, h)), (0, y0))

    def save(self, path):
        img = self.img
        if self.alpha is not None:                # overlay PNG for the video renderer
            img = img.convert("RGBA"); img.putalpha(self.alpha)
        if self._credit:
            img = self._draw_credit(img)
        if self.alpha is not None:
            img.save(str(path).rsplit(".", 1)[0] + ".png")
        else:
            img.convert("RGB").save(path, quality=90, optimize=True)


# ------------------------------------------------------------------ media helpers
def cover_crop(img, w, h, focus=0.35):
    img = img.convert("RGB")
    s = max(w / img.width, h / img.height)
    r = img.resize((max(w, int(img.width * s + 0.5)), max(h, int(img.height * s + 0.5))), Image.LANCZOS)
    x, y = (r.width - w) // 2, int((r.height - h) * focus)
    return r.crop((x, y, x + w, y + h))


def fade(img, top=0, bottom=0):
    """Fade the top/bottom edge of a picture into black."""
    w, h = img.size
    m = Image.new("L", (1, h), 255)
    for yy in range(h):
        a = 255
        if top and yy < top:
            t = yy / top; a = min(a, int(255 * t * t * (3 - 2 * t)))
        if bottom and yy > h - bottom:
            t = (h - yy) / bottom; a = min(a, int(255 * t * t * (3 - 2 * t)))
        m.putpixel((0, yy), a)
    return Image.composite(img, Image.new("RGB", (w, h), BG), m.resize((w, h)))


# ------------------------------------------------------------------ templates
VIDEO = "video"     # pass as `media` to get a transparent overlay PNG + the video box, for video.py


def card(s, path, media=None):
    """Post card. s: text, credit, source (shown when there's no picture), page."""
    c = Canvas()
    text = s["text"]
    maxw = W - 2 * PAD
    if media is not None:
        y = c.header() + 40
        # text as large as possible while the picture keeps >= 40% of the slide
        for size in (48, 46, 44, 42, 40, 38):
            th, n = c.block_h(text, CARD, CARD_HL, size, 1.27, maxw)
            if y + th + 44 <= H - MIN_MEDIA and n <= 6:
                break
        y = c.draw(text, CARD, CARD_HL, size, 1.27, PAD, y, maxw) + 44
        box = (0, y, W, H)
        if media is VIDEO:
            c.hole(y, H, fade_top=18)
        else:
            c.img.paste(fade(cover_crop(media, W, H - y), top=18), (0, y))
        if s.get("credit"):
            c.credit(s["credit"], W - 28, H - 28)
    else:
        for size in (60, 56, 52, 48, 44):
            th, n = c.block_h(text, CARD, CARD_HL, size, 1.25, maxw)
            if th <= 760 and n <= 9:
                break
        block = 88 + 56 + th + (70 if s.get("source") else 0)
        y0 = max(PAD, (H - block) // 2 - 20)
        y = c.header(y0) + 56
        if s.get("page"):
            c.label(s["page"], W - PAD, y0 + 30, size=20, anchor="ra")
        y = c.draw(text, CARD, CARD_HL, size, 1.25, PAD, y, maxw)
        if s.get("source"):
            c.label("SOURCE: " + s["source"].upper(), PAD, y + 44, size=22)
        c.save(path)
        return
    if s.get("page"):
        c.label(s["page"], W - PAD, PAD + 30, size=20, anchor="ra")
    c.save(path)
    return box


def headline(s, path, media=None):
    """Carousel cover. s: headline, swipe (bool), credit."""
    c = Canvas()
    maxw = W - 2 * 44
    bottom = H - 64
    swipe_h = 54 if s.get("swipe", True) else 0
    for size in (84, 78, 72, 66, 60, 56):
        th, n = c.block_h(s["headline"], HEAD, HEAD, size, 1.02, maxw, upper=True)
        if n <= 5 and th <= H - MIN_MEDIA - 140 - swipe_h:
            break
    text_top = bottom - swipe_h - th
    if media is None:                                    # no picture: centre the block
        text_top = (H - (46 + th + swipe_h)) // 2 + 46
    line_y = text_top - 46
    box = None
    if media is not None:
        mh = line_y - 30
        box = (0, 0, W, mh)
        if media is VIDEO:
            c.hole(0, mh, fade_bottom=150)
        else:
            c.img.paste(fade(cover_crop(media, W, mh, focus=0.3), bottom=150), (0, 0))
        if s.get("credit"):
            c.credit(s["credit"], W - 28, 28 + 34)
    c.brand_line(line_y)
    c.draw(s["headline"], HEAD, HEAD, size, 1.02, 44, text_top, maxw, upper=True, center=True)
    if swipe_h:
        c.label("SWIPE FOR MORE", W / 2, text_top + th + 26, size=22, color=WHITE, anchor="ma",
                spec=("InterTight.ttf", {"Weight": 700}, 0.06))
    c.save(path)
    return box


def render_still(s, path, media=None):
    """Render a slide. With media=VIDEO, writes <path>.png as a transparent overlay and returns the
    (x0, y0, x1, y1) box the video should fill."""
    return {"card": card, "headline": headline}[s["layout"]](s, path, media)
