"""Renderer for @peak.wellness.lab: plain black slides, text centred in the middle, @handle at the bottom.
Text markup: wrap the key words in [square brackets] to colour them tomato.
Fonts: DM Serif Display (quotes, headlines, numbers) + DM Sans (body, notes, handle)."""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

W, H = 1080, 1350
F = str(Path(__file__).resolve().parent / "fonts") + "/"
HANDLE = "@peak.wellness.lab"
HANDLE_POS = "center"       # "left", "center" or "right"

BG = (0, 0, 0)              # plain black
INK = (245, 245, 242)       # main text
SOFT = (200, 200, 196)      # body text on point slides
ACCENT = (242, 118, 95)     # tomato: [highlighted] words and big numbers
MUTED = (140, 140, 136)     # handle, source notes
M = 96                      # side margin
TEXT_W = W - 2 * M
TOP, BOTTOM = 110, H - 150  # text area (keeps clear of the handle)
QUOTE_FONT, QUOTE_LH = "display", 1.15
CTA_LINE2 = "Follow for one simple [energy fix] a day."
CTA_LINE3 = "Share it with a friend who needs more energy."


def theme(dark=False):
    """Kept so older batch scripts still run; every slide is black now."""


def font(kind, size):
    if kind in ("display", "serif"):
        return ImageFont.truetype(F + "DMSerifDisplay-Regular.ttf", size)
    f = ImageFont.truetype(F + "DMSans-Variable.ttf", size)
    f.set_variation_by_axes([14, 400 if kind == "body" else 500]); return f

# ---------------------------------------------------------------- shared layout (same in both brands' brand.py)


def parse(text):
    out, inside = [], False
    for tok in text.split():
        if tok.startswith("["):
            inside = True
        end = "]" in tok
        out.append((tok.replace("[", "").replace("]", ""), inside))
        if end:
            inside = False
    return out


def layout(text, f, maxw, lh_mult):
    sp = f.getlength(" ")
    lines, cur, w = [], [], 0
    for wd, h in parse(text):
        l = f.getlength(wd)
        if cur and w + sp + l > maxw:
            lines.append(cur); cur, w = [], 0
        w += (sp if cur else 0) + l
        cur.append((wd, h, l))
    if cur:
        lines.append(cur)
    return lines, int(f.size * lh_mult)


class Block:
    """One centred paragraph: text, font kind, size, colour, line height, gap after."""
    def __init__(self, text, kind, size, color=None, lh=1.25, gap=0, maxw=TEXT_W):
        self.text, self.kind, self.size, self.color, self.lh, self.gap, self.maxw = text, kind, size, color, lh, gap, maxw
        self.f = font(kind, size)
        self.lines, self.lhp = layout(text, self.f, maxw, lh)

    @property
    def height(self):
        return len(self.lines) * self.lhp


def fit(text, kind, sizes, max_h, lh=1.25, maxw=TEXT_W):
    """Biggest size from `sizes` whose wrapped text fits in max_h."""
    for s in sizes:
        b = Block(text, kind, s, lh=lh, maxw=maxw)
        if b.height <= max_h:
            return s
    return sizes[-1]


def render(blocks, path):
    """Plain black slide: blocks stacked and centred in the middle, handle at the bottom."""
    img = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(img)
    total = sum(b.height + b.gap for b in blocks) - (blocks[-1].gap if blocks else 0)
    y = (TOP + BOTTOM - total) / 2
    for b in blocks:
        sp = b.f.getlength(" ")
        for line in b.lines:
            lw = sum(l for _, _, l in line) + sp * (len(line) - 1)
            x = (W - lw) / 2
            for wd, hl, l in line:
                d.text((x, y), wd, font=b.f, fill=ACCENT if hl else (b.color or INK))
                x += l + sp
            y += b.lhp
        y += b.gap
    hf = font("handle", 30)
    hx = {"left": M, "center": W / 2, "right": W - M}[HANDLE_POS]
    anchor = {"left": "ls", "center": "ms", "right": "rs"}[HANDLE_POS]
    d.text((hx, H - 78), HANDLE, font=hf, fill=MUTED, anchor=anchor)
    img.save(path, quality=95)


# ---------------------------------------------------------------- slide templates
# Signatures are unchanged from the old look so every batch script still works;
# kicker / page / seed are accepted but no longer drawn.

def quote(text, path, kicker=None, seed=0, page=None):
    s = fit(text, QUOTE_FONT, [96, 88, 80, 72, 64, 58], BOTTOM - TOP, lh=QUOTE_LH)
    render([Block(text, QUOTE_FONT, s, lh=QUOTE_LH)], path)


def stat(number, text, path, note=None, kicker=None, seed=0):
    ns = fit(number, "display", [200, 170, 140, 120], 260, lh=1.05)
    blocks = [Block(number, "display", ns, color=ACCENT, lh=1.05, gap=44),
              Block(text, QUOTE_FONT, fit(text, QUOTE_FONT, [60, 54, 48], 420, lh=1.25), lh=1.25, gap=56)]
    if note:
        blocks.append(Block(note, "small", 28, color=MUTED, lh=1.4, maxw=TEXT_W - 80))
    else:
        blocks[-1].gap = 0
    render(blocks, path)


def cover(title, sub, path, kicker=None, seed=0):
    ts = fit(title, "display", [120, 108, 96, 88, 80], 620, lh=1.12)
    render([Block(title, "display", ts, lh=1.12, gap=52),
            Block(sub, "small", 40, color=MUTED, lh=1.35)], path)


def point(num, heading, body, path, kicker=None, page=None, seed=0):
    hs = fit(heading, "display", [84, 76, 68, 60], 300, lh=1.15)
    bs = fit(body, "body", [44, 40, 36], 440, lh=1.4)
    render([Block(num, "display", 110, color=ACCENT, lh=1.0, gap=40),
            Block(heading, "display", hs, lh=1.15, gap=44),
            Block(body, "body", bs, color=SOFT, lh=1.4)], path)


def cta(path, kicker=None, page=None, line1="Save this for later.", line2=CTA_LINE2, line3=CTA_LINE3):
    render([Block(line1, "display", 96, lh=1.12, gap=44),
            Block(line2, "body", 50, lh=1.3, gap=40),
            Block(line3, "small", 32, color=MUTED, lh=1.35)], path)
