"""Branded fallback picture for stories without a usable article image.

Black field, faint perspective grid, a glowing yellow node network and the story's
category word set huge and dim. Deterministic per seed, so a rerun gives the same art.
"""
import math, random
from PIL import Image, ImageDraw, ImageFilter
from brand import font, YELLOW

W, H = 1080, 1350


def make_art(seed, word="AI", w=W, h=H):
    rng = random.Random(str(seed))
    img = Image.new("RGB", (w, h), (0, 0, 0))
    d = ImageDraw.Draw(img)

    # perspective floor grid
    hz = int(h * 0.62)
    vx = w // 2 + rng.randint(-120, 120)
    for i in range(-14, 15):
        d.line([(vx, hz), (vx + i * 160, h)], fill=(30, 30, 30), width=2)
    y, step = hz, 6
    while y < h:
        d.line([(0, y), (w, y)], fill=(30, 30, 30), width=2)
        step *= 1.35; y += int(step)

    # big dim word
    f = font("head", 360)
    word = word.upper()[:10]
    while f.getlength(word) > w * 1.15 and f.size > 140:
        f = font("head", f.size - 20)
    d.text((w // 2, int(h * 0.36)), word, font=f, fill=(22, 22, 22), anchor="mm")

    # node network
    nodes = [(rng.uniform(0.08, 0.92) * w, rng.uniform(0.08, 0.80) * h) for _ in range(26)]
    glow = Image.new("RGB", (w, h), (0, 0, 0))
    g = ImageDraw.Draw(glow)
    for i, a in enumerate(nodes):
        near = sorted(nodes, key=lambda b: (a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2)[1:3]
        for b in near:
            g.line([a, b], fill=(120, 100, 10), width=2)
    hubs = rng.sample(range(len(nodes)), 5)
    for i, (x, y) in enumerate(nodes):
        r = 11 if i in hubs else 5
        g.ellipse([x - r, y - r, x + r, y + r], fill=YELLOW if i in hubs else (170, 140, 10))
    from PIL import ImageChops
    img = ImageChops.add(img, glow.filter(ImageFilter.GaussianBlur(14)))
    img = ImageChops.add(img, glow)

    # soft yellow light from one corner
    light = Image.new("L", (w, h), 0)
    ld = ImageDraw.Draw(light)
    cx, cy = rng.choice([0, w]), 0
    for r in range(900, 0, -30):
        ld.ellipse([cx - r, cy - r, cx + r, cy + r], fill=int(38 * (1 - r / 900)))
    img = Image.composite(Image.new("RGB", (w, h), YELLOW), img, light)
    return img


if __name__ == "__main__":
    import sys
    make_art(sys.argv[1] if len(sys.argv) > 1 else "x", sys.argv[2] if len(sys.argv) > 2 else "MODELS").save("art_test.jpg")
