"""Renderer for @peak.wellness.lab: plain black slides with normal text centred in the middle, @handle at the bottom.
Normal text only: DM Sans Regular, white, one size per slide. No bold or display fonts.
Wrap important words in [square brackets] to colour them tomato."""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

W, H = 1080, 1350
F = str(Path(__file__).resolve().parent / "fonts") + "/"
HANDLE = "@peak.wellness.lab"
HANDLE_POS = "center"       # "left", "center" or "right"

BG = (0, 0, 0)              # plain black
INK = (245, 245, 242)       # all text
ACCENT = (242, 118, 95)    # tomato: [important words] and the number on stat / point slides
MUTED = (140, 140, 136)     # handle, source notes
M = 96                      # side margin
TEXT_W = W - 2 * M
TOP, BOTTOM = 110, H - 150  # text area (keeps clear of the handle)
LH, PARA_GAP = 1.4, 0.9     # line height and space between paragraphs (x font size)
CTA_LINE2 = "Follow for one simple [energy fix] a day."
CTA_LINE3 = "Share it with a friend who needs more energy."


def theme(dark=False):
    """Kept so older batch scripts still run; every slide is black now."""


def font(size):
    f = ImageFont.truetype(F + "DMSans-Variable.ttf", size)
    f.set_variation_by_axes([14, 400]); return f

# ---------------------------------------------------------------- shared layout (same in both brands' brand.py)
# Normal text: one regular font and one size per slide. [Bracketed] words are drawn in the accent colour.


def clean(text):
    return " ".join(text.replace("[", "").replace("]", "").split())


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


def wrap(text, f, maxw):
    """Lines of (word, highlighted, width)."""
    sp = f.getlength(" ")
    lines, cur, w = [], [], 0
    for wd, hl in parse(text):
        l = f.getlength(wd)
        if cur and w + sp + l > maxw:
            lines.append(cur); cur, w = [], 0
        w += (sp if cur else 0) + l
        cur.append((wd, hl, l))
    if cur:
        lines.append(cur)
    return lines


def _plan(paras, size):
    """paras: list of (text, small). Returns [(lines, font, line_h, gap_after, colour)] and total height."""
    out, total = [], 0
    for i, (text, small) in enumerate(paras):
        s = int(size * 0.62) if small else size
        f = font(s)
        lh = int(s * LH)
        lines = wrap(text, f, TEXT_W)
        gap = int(size * PARA_GAP) if i < len(paras) - 1 else 0
        out.append((lines, f, lh, gap, MUTED if small else INK))
        total += len(lines) * lh + gap
    return out, total


def render(paras, path, sizes=(64, 58, 52, 48, 44, 40, 36)):
    """Plain black slide: paragraphs centred in the middle at the biggest size that fits, handle at the bottom."""
    paras = [(t, sm) for t, sm in paras if t and clean(t)]
    for size in sizes:
        plan, total = _plan(paras, size)
        if total <= BOTTOM - TOP:
            break
    img = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(img)
    y = (TOP + BOTTOM - total) / 2
    for lines, f, lh, gap, colour in plan:
        sp = f.getlength(" ")
        for line in lines:
            x = (W - sum(l for _, _, l in line) - sp * (len(line) - 1)) / 2
            for wd, hl, l in line:
                d.text((x, y), wd, font=f, fill=ACCENT if hl else colour, anchor="la")
                x += l + sp
            y += lh
        y += gap
    hx = {"left": M, "center": W / 2, "right": W - M}[HANDLE_POS]
    anchor = {"left": "ls", "center": "ms", "right": "rs"}[HANDLE_POS]
    d.text((hx, H - 78), HANDLE, font=font(30), fill=MUTED, anchor=anchor)
    img.save(path, quality=95)


# ---------------------------------------------------------------- slide templates
# Signatures are unchanged so every batch script still works; kicker / page / seed are accepted but not drawn.

def quote(text, path, kicker=None, seed=0, page=None):
    render([(text, False)], path)


def stat(number, text, path, note=None, kicker=None, seed=0):
    render([(f"[{clean(number)}]", False), (text, False), (note, True)], path)


def cover(title, sub, path, kicker=None, seed=0):
    render([(title, False), (sub, False)], path)


def point(num, heading, body, path, kicker=None, page=None, seed=0):
    render([(f"[{clean(num)}]", False), (heading, False), (body, False)], path)


def cta(path, kicker=None, page=None, line1="Save this for later.", line2=CTA_LINE2, line3=CTA_LINE3):
    render([(line1, False), (line2, False), (line3, False)], path)
