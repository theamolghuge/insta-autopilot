"""Brand renderer for @peak.wellness.lab: the fin.ance18 renderer with the peak.wellness.lab colors and type.
Colors: plate #FBF1EA ground, navy #1E2A38 ink, tomato #E5533D accent (tomato-deep #B23A27 for small text),
tomato-soft #FBDCD3 highlighter. Type: DM Serif Display (headlines, numbers, quotes) + DM Sans (everything else).
Text markup: wrap highlighted words in [square brackets]. dark=True gives the navy "night" version."""
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import re, random

W, H = 1080, 1350
from pathlib import Path
F = str(Path(__file__).resolve().parent / "fonts") + "/"
HANDLE = "@peak.wellness.lab"

LIGHT = dict(BG=(251, 241, 234), INK=(30, 42, 56), ACCENT=(178, 58, 39), BIG=(229, 83, 61),
             MUTED=(90, 100, 114), HL=(251, 220, 211), RULE=(227, 211, 199))
NIGHT = dict(BG=(30, 42, 56), INK=(251, 241, 234), ACCENT=(246, 164, 147), BIG=(242, 118, 95),
             MUTED=(185, 192, 200), HL=(63, 43, 46), RULE=(58, 71, 88))
BG, INK, ACCENT, BIG, MUTED, HL, RULE = (LIGHT[k] for k in ("BG", "INK", "ACCENT", "BIG", "MUTED", "HL", "RULE"))


def theme(dark=False):
    """Switch every color for the next slides: light 'plate' ground or navy 'night' ground."""
    global BG, INK, ACCENT, BIG, MUTED, HL, RULE
    t = NIGHT if dark else LIGHT
    BG, INK, ACCENT, BIG, MUTED, HL, RULE = (t[k] for k in ("BG", "INK", "ACCENT", "BIG", "MUTED", "HL", "RULE"))
M = 96                      # side margin


def font(kind, size):
    if kind == "display":
        return ImageFont.truetype(F + "DMSerifDisplay-Regular.ttf", size)
    # "serif" (quotes, headings) = DM Serif Display; body text = DM Sans
    if kind in ("serif", "serif_semi"):
        return ImageFont.truetype(F + "DMSerifDisplay-Regular.ttf", size)
    wght = {"sans": 500, "body": 400, "sans_bold": 700}[kind]
    f = ImageFont.truetype(F + "DMSans-Variable.ttf", size)
    f.set_variation_by_axes([14, wght]); return f


def parse(text):
    out, inside = [], False
    for tok in text.split():
        start = tok.startswith("[")
        if start: inside = True
        end = "]" in tok
        out.append((tok.replace("[", "").replace("]", ""), inside))
        if end: inside = False
    return out


def layout(text, f, maxw, lh_mult=1.38):
    words = parse(text)
    sp = f.getlength(" ")
    lines, cur, w = [], [], 0
    for wd, h in words:
        l = f.getlength(wd)
        if cur and w + sp + l > maxw:
            lines.append(cur); cur, w = [], 0
        w += (sp if cur else 0) + l
        cur.append((wd, h, l))
    if cur: lines.append(cur)
    return lines, int(f.size * lh_mult)


class Canvas:
    def __init__(self, seed=0):
        self.ink = INK
        self.img = Image.new("RGBA", (W, H), BG + (255,))
        self.hl = Image.new("RGBA", (W, H), HL + (0,))
        self.texts = []  # deferred so text sits above highlight
        self.rng = random.Random(seed)

    def rich(self, text, kind, size, y, maxw=W - 2 * M, color=None, x=M, center=False, lh=1.38):
        color = color or INK
        f = font(kind, size)
        lines, lhp = layout(text, f, maxw, lh)
        hd = ImageDraw.Draw(self.hl)
        sp = f.getlength(" ")
        asc, desc = f.getmetrics()
        for li, line in enumerate(lines):
            lw = sum(l for _, _, l in line) + sp * (len(line) - 1)
            cx = x + (maxw - lw) / 2 if center else x
            yy = y + li * lhp
            j = self.rng.uniform(-3, 3)
            for k, (wd, h, l) in enumerate(line):
                if h:
                    nxt = line[k + 1][1] if k + 1 < len(line) else False
                    ext = sp if nxt else 0
                    top = yy + asc * 0.30 + j
                    bot = yy + asc + desc * 0.55 + j
                    hd.rounded_rectangle([cx - 10, top, cx + l + ext + 10, bot], 8, fill=HL + (255,))
                self.texts.append((cx, yy, wd, f, color))
                cx += l + sp
        return y + len(lines) * lhp  # bottom

    def measure(self, text, kind, size, maxw=W - 2 * M, lh=1.38):
        lines, lhp = layout(text, font(kind, size), maxw, lh)
        return len(lines) * lhp

    def label(self, text, x, y, kind="sans_bold", size=28, color=None, spacing=4, anchor="la"):
        color = color or ACCENT
        self.texts.append(("label", x, y, text, font(kind, size), color, spacing, anchor))

    def chrome(self, kicker=None, page=None, swipe=False, disclaimer=False):
        if kicker:
            self.label(kicker.upper(), M, 92)
            self.line = (M, 140)
        # footer
        self.label(HANDLE, M, H - 82, kind="sans", size=28, color=MUTED, spacing=0)
        if page:
            self.label(page, W - M, H - 82, kind="sans", size=28, color=MUTED, spacing=0, anchor="ra")
        elif swipe:
            self.label("Swipe  →", W - M, H - 82, kind="sans_bold", size=28, color=ACCENT, spacing=1, anchor="ra")

    def save(self, path):
        img = Image.alpha_composite(self.img, self.hl.filter(ImageFilter.GaussianBlur(2.2)))
        d = ImageDraw.Draw(img)
        d.line([(M, H - 120), (W - M, H - 120)], fill=RULE, width=2)
        if hasattr(self, "line"):
            d.line([(M, 140), (M + 60, 140)], fill=BIG, width=4)
        for t in self.texts:
            if t[0] == "label":
                _, x, y, s, f, c, spc, anchor = t
                if spc:
                    total = sum(f.getlength(ch) + spc for ch in s) - spc
                    cx = x - total if anchor == "ra" else x
                    for ch in s:
                        d.text((cx, y), ch, font=f, fill=c); cx += f.getlength(ch) + spc
                else:
                    d.text((x, y), s, font=f, fill=c, anchor=anchor)
            else:
                x, y, s, f, c = t
                d.text((x, y), s, font=f, fill=c)
        img.convert("RGB").save(path, quality=95)


# ---------- slide templates ----------

def fit_size(c, text, kind, sizes, max_h, maxw=W - 2 * M, lh=1.38):
    for s in sizes:
        if c.measure(text, kind, s, maxw, lh) <= max_h:
            return s
    return sizes[-1]


def quote(text, path, kicker="Energy", seed=0, page=None):
    c = Canvas(seed); c.chrome(kicker, page=page)
    s = fit_size(c, text, "serif", [104, 96, 88, 80, 72], 820, lh=1.15)
    h = c.measure(text, "serif", s, lh=1.15)
    c.rich(text, "serif", s, (H - h) // 2 - 10, lh=1.15)
    c.save(path)


def stat(number, text, path, note=None, kicker="By the numbers", seed=0):
    c = Canvas(seed); c.chrome(kicker)
    nh = c.measure(number, "display", 170, lh=1.1)
    th = c.measure(text, "serif", 64, lh=1.15)
    total = nh + 30 + th + (90 if note else 0)
    y = (H - total) // 2
    y = c.rich(number, "display", 170, y, color=BIG, lh=1.1) + 30
    y = c.rich(text, "serif", 64, y, lh=1.15)
    if note:
        c.rich(note, "body", 28, y + 40, color=MUTED, lh=1.4)
    c.save(path)


def cover(title, sub, path, kicker, seed=0):
    c = Canvas(seed); c.chrome(kicker, swipe=True, disclaimer=False)
    s = fit_size(c, title, "display", [120, 108, 96, 88], 640, lh=1.15)
    th = c.measure(title, "display", s, lh=1.15)
    sh = c.measure(sub, "sans", 42)
    y = (H - th - 50 - sh) // 2
    y = c.rich(title, "display", s, y, lh=1.15) + 50
    c.rich(sub, "sans", 42, y, color=MUTED, lh=1.3)
    c.save(path)


def point(num, heading, body, path, kicker, page, seed=0):
    c = Canvas(seed); c.chrome(kicker, page=page)
    hs = fit_size(c, heading, "display", [84, 76, 68], 300, lh=1.18)
    hh = c.measure(heading, "display", hs, lh=1.18)
    bh = c.measure(body, "body", 40, lh=1.4)
    total = 150 + hh + 50 + bh
    y = max(220, (H - total) // 2)
    c.label(num, M, y, kind="display", size=110, color=BIG, spacing=0)
    y += 150
    y = c.rich(heading, "display", hs, y, lh=1.18) + 50
    c.rich(body, "body", 40, y, lh=1.4)
    c.save(path)


def cta(path, kicker, page, line1="Save this for later.", line2="Follow for one simple [energy fix] a day."):
    c = Canvas(9); c.chrome(kicker, page=page)
    h = c.measure(line1, "display", 96, lh=1.15) + 40 + c.measure(line2, "sans", 48, lh=1.3)
    y = (H - h) // 2
    y = c.rich(line1, "display", 96, y, lh=1.15) + 40
    y = c.rich(line2, "sans", 48, y, lh=1.3)
    c.label("Share it with a friend who needs more energy.", M, y + 40, kind="body", size=30, color=MUTED, spacing=0)
    c.save(path)
