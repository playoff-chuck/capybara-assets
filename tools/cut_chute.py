"""Schneidet ein 3x2-Fallschirm-Blatt auf Grün in 6 freigestellte WebP (240x300 wie chute_1..6).
Aufruf: cut_chute.py blatt.png ausgabeordner prefix"""
import sys, numpy as np
from PIL import Image
src, outd, pre = sys.argv[1:4]
im = np.asarray(Image.open(src).convert("RGB")).astype(np.float32); H, W, _ = im.shape
CW, CH = 240, 300
cells = []
for r in range(2):
    for c in range(3):
        cell = im[r * H // 2:(r + 1) * H // 2, c * W // 3:(c + 1) * W // 3]
        R, G, B = cell[..., 0], cell[..., 1], cell[..., 2]
        g = G - np.maximum(R, B); a = np.clip(1 - (g - 40) / 80, 0, 1)
        sp = np.minimum(G, np.maximum(R, B)); cell = cell.copy(); cell[..., 1] = np.where(g > 0, sp, G)
        rgba = np.dstack([cell, a * 255]).astype(np.uint8); m = a > 0.5; yy, xx = np.where(m)
        cells.append((rgba, yy.min(), yy.max(), xx.min(), xx.max()))
hs = [c[2] - c[1] + 1 for c in cells]; scale = (CH - 16) / float(max(hs))
for i, (rgba, ya, yb, xa, xb) in enumerate(cells):
    crop = Image.fromarray(rgba[ya:yb + 1, xa:xb + 1]); w, h = crop.size
    crop = crop.resize((max(1, int(w * scale)), max(1, int(h * scale))), Image.LANCZOS)
    out = Image.new("RGBA", (CW, CH), (0, 0, 0, 0)); out.paste(crop, ((CW - crop.width) // 2, CH - 8 - crop.height), crop)
    out.save(f"{outd}/{pre}_{i + 1}.webp", "WEBP", quality=90, method=6); print(i + 1, crop.size)
