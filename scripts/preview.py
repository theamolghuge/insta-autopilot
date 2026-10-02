#!/usr/bin/env python3
"""Make a contact sheet of an account's queue so you can eyeball posts before they go live.

  python scripts/preview.py fin.ance18            -> preview_fin.ance18.jpg (unposted items only)
  python scripts/preview.py fin.ance18 --all      -> include already-posted items
"""
import json, sys
from pathlib import Path
from PIL import Image, ImageDraw

ROOT = Path(__file__).resolve().parent.parent
acc = sys.argv[1] if len(sys.argv) > 1 else "fin.ance18"
show_all = "--all" in sys.argv
state = {}
sp = ROOT / "state" / f"{acc}.json"
if sp.exists():
    state = json.loads(sp.read_text())
posted = set(state.get("posted", {}))
items = sorted(p for p in (ROOT / "content" / acc / "queue").iterdir() if p.is_dir())
if not show_all:
    items = [i for i in items if i.name not in posted]
TW, TH, cols = 216, 270, 10
tiles = []
for it in items:
    for j, img in enumerate(sorted(it.glob("*.jpg"))):
        tiles.append((it.name if j == 0 else "", img))
rows = (len(tiles) + cols - 1) // cols or 1
sheet = Image.new("RGB", (cols * TW, rows * (TH + 22)), "white")
d = ImageDraw.Draw(sheet)
for k, (label, img) in enumerate(tiles):
    x, y = (k % cols) * TW, (k // cols) * (TH + 22)
    sheet.paste(Image.open(img).resize((TW - 4, TH - 4)), (x + 2, y + 2))
    if label:
        d.text((x + 4, y + TH + 4), label[:30], fill=(30, 30, 30))
out = ROOT / f"preview_{acc}.jpg"
sheet.save(out, quality=85)
print(f"{len(items)} posts, {len(tiles)} images -> {out}")
