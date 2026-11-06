"""Schneidet ein 4x2-Laufzyklus-Blatt auf Grün in 8 freigestellte Einzelbilder (WebP, 247x252 wie thief_1..7).
Aufruf: cut_walk.py blatt.png ausgabeordner vorschau.jpg"""
import sys, numpy as np
from PIL import Image
src, outd, prev = sys.argv[1:4]
im = np.asarray(Image.open(src).convert("RGB")).astype(np.float32)
H, W, _ = im.shape
ref = np.asarray(Image.open("/srv/capy-assets/site/img/thief_1.webp").convert("RGBA"))
ra = ref[..., 3] > 128; ys = np.where(ra.any(1))[0]; ref_h = ys[-1] - ys[0] + 1
CW, CH = 247, 252
cells = []
for r in range(2):
    for c in range(4):
        x0, x1, y0, y1 = c * W // 4, (c + 1) * W // 4, r * H // 2, (r + 1) * H // 2
        cell = im[y0:y1, x0:x1]
        R, G, B = cell[..., 0], cell[..., 1], cell[..., 2]
        g = G - np.maximum(R, B)                       # Grünüberschuss
        a = np.clip(1 - (g - 40) / 80, 0, 1)            # weicher Rand
        sp = np.minimum(G, np.maximum(R, B))            # Grünstich entfernen
        cell = cell.copy(); cell[..., 1] = np.where(g > 0, sp, G)
        rgba = np.dstack([cell, a * 255]).astype(np.uint8)
        m = a > 0.5
        # kleine Reste am Zellrand entfernen: nur größte Fläche behalten (grob über Zeilen/Spalten)
        yy, xx = np.where(m)
        cells.append((rgba, yy.min(), yy.max(), xx.min(), xx.max(), m))
hs = [c[2] - c[1] + 1 for c in cells]
scale = ref_h / float(np.median(hs))
out = []
for i, (rgba, ya, yb, xa, xb, m) in enumerate(cells):
    # Mitte nach Kopf/Rumpf (obere 55 %) statt Beine/Schwanz
    top = m[ya:ya + int((yb - ya) * 0.55)]
    cx = np.where(top)[1].mean() if top.any() else (xa + xb) / 2
    crop = Image.fromarray(rgba[ya:yb + 1, :]).resize((int(rgba.shape[1] * scale), int((yb - ya + 1) * scale)), Image.LANCZOS)
    canvas = Image.new("RGBA", (CW, CH), (0, 0, 0, 0))
    # Bezug: in thief_1 liegt die Kopf/Rumpf-Mitte bei rcx
    if i == 0:
        rt = ra[ys[0]:ys[0] + int(ref_h * 0.55)]; out_rcx = np.where(rt)[1].mean()
    px = int(round(out_rcx - cx * scale)); py = CH - 2 - crop.height
    canvas.paste(crop, (px, py), crop)
    canvas.save(f"{outd}/thief_w{i + 1}.webp", quality=88, method=6)
    out.append(canvas)
strip = Image.new("RGBA", (CW * 9 + 80, CH), (60, 70, 50, 255)); x = 0
for c in [Image.open("/srv/capy-assets/site/img/thief_1.webp").convert("RGBA")] + out:
    strip.alpha_composite(c, (x, 0)); x += CW + 10
strip.convert("RGB").save(prev, quality=88)
print("ok scale", round(scale, 3), "heights", hs)
