from PIL import Image, ImageDraw, ImageFont, ImageFilter
import os, sys, json

W, H = 1080, 1350
# First serif font found is used (Linux, Windows, macOS). Add your own path to the front to change it.
FONT_CANDIDATES = [
    "/usr/share/fonts/truetype/liberation/LiberationSerif-Regular.ttf",
    "C:/Windows/Fonts/times.ttf",
    "/System/Library/Fonts/Supplemental/Times New Roman.ttf",
    "/Library/Fonts/Times New Roman.ttf",
]
FONT = next((f for f in FONT_CANDIDATES if os.path.exists(f)), FONT_CANDIDATES[0])
SIZE = 92
MARGIN = 90
GREEN = (196, 236, 176, 255)
TEXT = (20, 20, 20)

def render(text, out):
    # text with [highlighted part]
    words, hl, inside = [], [], False
    for tok in text.split(" "):
        s = tok
        if s.startswith("["): inside = True; s = s[1:]
        end = s.endswith("]") or s.endswith("],") or s.endswith("].")
        s = s.replace("]", "")
        words.append(s); hl.append(inside)
        if end: inside = False
    font = ImageFont.truetype(FONT, SIZE)
    space = font.getlength(" ")
    lines, cur, w = [], [], 0
    for i, wd in enumerate(words):
        l = font.getlength(wd)
        if cur and w + space + l > W - 2 * MARGIN:
            lines.append(cur); cur, w = [], 0
        w = w + (space if cur else 0) + l
        cur.append(i)
    lines.append(cur)
    lh = int(SIZE * 1.45)
    y0 = (H - lh * len(lines)) // 2
    img = Image.new("RGBA", (W, H), (255, 255, 255, 255))
    layer = Image.new("RGBA", (W, H), (196, 236, 176, 0))
    hd = ImageDraw.Draw(layer)
    pos = []
    for li, line in enumerate(lines):
        x, y = MARGIN, y0 + li * lh
        for k, i in enumerate(line):
            l = font.getlength(words[i])
            pos.append((i, x, y))
            if hl[i]:
                nxt = line[k + 1] if k + 1 < len(line) else None
                ext = space if nxt is not None and hl[nxt] else 0
                hd.rounded_rectangle([x - 8, y + 4, x + l + ext + 8, y + SIZE * 1.12], 10, fill=GREEN)
            x += l + space
    layer = layer.filter(ImageFilter.GaussianBlur(2.5))
    img = Image.alpha_composite(img, layer)
    d = ImageDraw.Draw(img)
    for i, x, y in pos:
        d.text((x, y), words[i], font=font, fill=TEXT)
    img.convert("RGB").save(out, quality=95)

if __name__ == "__main__":
    # usage: python make_posts.py week.json output_folder
    #   week.json is a list of strings (or [quote, caption] pairs); wrap the highlighted words in [brackets]
    posts = json.load(open(sys.argv[1]))
    os.makedirs(sys.argv[2], exist_ok=True)
    for n, p in enumerate(posts, 1):
        p = p[0] if isinstance(p, list) else p
        render(p, os.path.join(sys.argv[2], f"post_{n:02d}.jpg"))
