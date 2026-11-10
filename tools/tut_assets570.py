#!/usr/bin/env python3
# V570: Kurs-Grafiken aus Nano Banana Pro schneiden (Lauf mit /opt/rembg/bin/python3)
# /srv/media/tut_icons_a.png → site/img/tut_ic0..9.webp (rund, transparent)
# /srv/media/tut_cheer_a.png → site/img/tut_cheer.webp (weißer Hintergrund weg)
# /srv/media/tut_bar_a.png   → site/img/tut_plank.webp (Holzbrett-Mitte als Streifen-Hintergrund)
import numpy as np
from PIL import Image, ImageDraw
OUT = "/srv/capy-assets/site/img/"
im = Image.open("/srv/media/tut_icons_a.png").convert("RGB"); a = np.asarray(im).astype(int)
dark = (a.sum(axis=2) < 200)   # dunkelbraune Ränder
H, W = dark.shape
# Spalten/Zeilen mit Rand finden
def runs(v, thr):
    on = v > thr; out = []; s = None
    for i, x in enumerate(on):
        if x and s is None: s = i
        if not x and s is not None: out.append((s, i)); s = None
    if s is not None: out.append((s, len(on)))
    return [r for r in out if r[1] - r[0] > 40]
rows = runs(dark.sum(axis=1), 3); print("rows", rows)
k = 0
for (y0, y1) in rows:
    cols = runs(dark[y0:y1].sum(axis=0), 3); print(" cols", cols)
    for (x0, x1) in cols:
        cx, cy = (x0 + x1) / 2, (y0 + y1) / 2; r = max(x1 - x0, y1 - y0) / 2 + 2
        box = (int(cx - r), int(cy - r), int(cx + r), int(cy + r))
        c = im.crop(box).convert("RGBA"); n = c.size[0]
        m = Image.new("L", (n * 4, n * 4), 0); ImageDraw.Draw(m).ellipse((4, 4, n * 4 - 4, n * 4 - 4), fill=255); m = m.resize((n, n), Image.LANCZOS)
        c.putalpha(m); c = c.resize((112, 112), Image.LANCZOS); c.save(OUT + f"tut_ic{k}.webp", quality=85); k += 1
print("icons", k)
ch = Image.open("/srv/media/tut_cheer_a.png").convert("RGBA"); d = np.asarray(ch).astype(int)
wh = (d[..., :3].min(axis=2) > 238)
# nur zusammenhängenden Rand-Weißbereich entfernen (Flutfüllung von den Ecken)
from collections import deque
h, w = wh.shape; seen = np.zeros_like(wh); q = deque([(0, 0), (0, w - 1), (h - 1, 0), (h - 1, w - 1)])
while q:
    y, x = q.popleft()
    if y < 0 or x < 0 or y >= h or x >= w or seen[y, x] or not wh[y, x]: continue
    seen[y, x] = True; q.extend([(y + 1, x), (y - 1, x), (y, x + 1), (y, x - 1)])
al = np.where(seen, 0, 255).astype(np.uint8); d2 = np.asarray(ch).copy(); d2[..., 3] = al
ch = Image.fromarray(d2); ch = ch.crop(ch.getbbox()); ch.thumbnail((256, 256), Image.LANCZOS); ch.save(OUT + "tut_cheer.webp", quality=85)
bar = Image.open("/srv/media/tut_bar_a.png").convert("RGB"); bw, bh = bar.size
pl = bar.crop((int(bw * .27), int(bh * .2), int(bw * .73), int(bh * .78))).resize((480, 160), Image.LANCZOS); pl.save(OUT + "tut_plank.webp", quality=78)
lf = Image.open("/srv/media/tut_bar_a.png").convert("RGBA")
print("ok")
