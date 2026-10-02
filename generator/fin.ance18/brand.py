"""Brand renderer for a US personal-finance Instagram page.
Text markup: wrap highlighted words in [square brackets]."""
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import re, random

W, H = 1080, 1350
from pathlib import Path
F = str(Path(__file__).resolve().parent / "fonts") + "/"
HANDLE = "@fin.ance18"

BG = (246, 241, 231)        # warm paper
INK = (22, 33, 27)          # green-black
ACCENT = (31, 77, 58)       # deep money green
MUTED = (104, 110, 100)
HL = (190, 232, 170)        # mint highlighter
M = 96                      # side margin


def font(kind, size):
    if kind == "display":
        return ImageFont.truetype(F + "DMSerifDisplay-Regular.ttf", size)
    if kind == "serif":
        f = ImageFont.truetype(F + "SourceSerif4%5Bopsz,wght%5D.ttf", size)
        f.set_variation_by_axes([420, 30]); return f
    if kind == "serif_semi":
        f = ImageFont.truetype(F + "SourceSerif4%5Bopsz,wght%5D.ttf", size)
        f.set_variation_by_axes([600, 30]); return f
    if kind == "sans":
        f = ImageFont.truetype(F + "Inter%5Bopsz,wght%5D.ttf", size)
        f.set_variation_by_axes([14, 500]); return f
    if kind == "sans_bold":
        f = ImageFont.truetype(F + "Inter%5Bopsz,wght%5D.ttf", size)
        f.set_variation_by_axes([14, 700]); return f


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
        self.img = Image.new("RGBA", (W, H), BG + (255,))
        self.hl = Image.new("RGBA", (W, H), HL + (0,))
        self.texts = []  # deferred so text sits above highlight
        self.rng = random.Random(seed)

    def rich(self, text, kind, size, y, maxw=W - 2 * M, color=INK, x=M, center=False, lh=1.38):
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

    def label(self, text, x, y, kind="sans_bold", size=26, color=ACCENT, spacing=3, anchor="la"):
        self.texts.append(("label", x, y, text, font(kind, size), color, spacing, anchor))

    def chrome(self, kicker=None, page=None, swipe=False, disclaimer=True):
        if kicker:
            self.label(kicker.upper(), M, 92)
            self.line = (M, 140)
        # footer
        self.label(HANDLE, M, H - 92, kind="sans", size=26, color=INK, spacing=0)
        if page:
            self.label(page, W - M, H - 92, kind="sans", size=26, color=MUTED, spacing=0, anchor="ra")
        elif swipe:
            self.label("Swipe  →", W - M, H - 92, kind="sans_bold", size=26, color=ACCENT, spacing=1, anchor="ra")
        if disclaimer:
            self.label("Educational content, not financial advice.", M, H - 52, kind="sans", size=19, color=MUTED, spacing=0)

    def save(self, path):
        img = Image.alpha_composite(self.img, self.hl.filter(ImageFilter.GaussianBlur(2.2)))
        d = ImageDraw.Draw(img)
        d.line([(M, H - 120), (W - M, H - 120)], fill=(214, 207, 192), width=2)
        if hasattr(self, "line"):
            d.line([(M, 140), (M + 60, 140)], fill=ACCENT, width=4)
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


def quote(text, path, kicker="Money habits", seed=0, page=None):
    c = Canvas(seed); c.chrome(kicker, page=page)
    s = fit_size(c, text, "serif", [96, 88, 80, 72, 64], 820)
    h = c.measure(text, "serif", s)
    c.rich(text, "serif", s, (H - h) // 2 - 10)
    c.save(path)


def stat(number, text, path, note=None, kicker="The math", seed=0):
    c = Canvas(seed); c.chrome(kicker)
    nh = c.measure(number, "display", 170, lh=1.1)
    th = c.measure(text, "serif", 56)
    total = nh + 30 + th + (90 if note else 0)
    y = (H - total) // 2
    y = c.rich(number, "display", 170, y, color=ACCENT, lh=1.1) + 30
    y = c.rich(text, "serif", 56, y)
    if note:
        c.rich(note, "sans", 26, y + 40, color=MUTED, lh=1.45)
    c.save(path)


def cover(title, sub, path, kicker, seed=0):
    c = Canvas(seed); c.chrome(kicker, swipe=True, disclaimer=False)
    s = fit_size(c, title, "display", [120, 108, 96, 88], 640, lh=1.15)
    th = c.measure(title, "display", s, lh=1.15)
    sh = c.measure(sub, "serif", 42)
    y = (H - th - 50 - sh) // 2
    y = c.rich(title, "display", s, y, lh=1.15) + 50
    c.rich(sub, "serif", 42, y, color=(60, 70, 62))
    c.save(path)


def point(num, heading, body, path, kicker, page, seed=0):
    c = Canvas(seed); c.chrome(kicker, page=page)
    hs = fit_size(c, heading, "display", [84, 76, 68], 300, lh=1.18)
    hh = c.measure(heading, "display", hs, lh=1.18)
    bh = c.measure(body, "serif", 44, lh=1.45)
    total = 150 + hh + 50 + bh
    y = max(220, (H - total) // 2)
    c.label(num, M, y, kind="display", size=110, color=ACCENT, spacing=0)
    y += 150
    y = c.rich(heading, "display", hs, y, lh=1.18) + 50
    c.rich(body, "serif", 44, y, lh=1.45)
    c.save(path)


def cta(path, kicker, page, line1="Save this for later.", line2="Follow for one money habit a day, [built to last.]"):
    c = Canvas(9); c.chrome(kicker, page=page)
    h = c.measure(line1, "display", 96, lh=1.15) + 40 + c.measure(line2, "serif", 54)
    y = (H - h) // 2
    y = c.rich(line1, "display", 96, y, lh=1.15) + 40
    y = c.rich(line2, "serif", 54, y)
    c.label("Share it with a friend who's starting out.", M, y + 40, kind="sans", size=28, color=MUTED, spacing=0)
    c.save(path)
