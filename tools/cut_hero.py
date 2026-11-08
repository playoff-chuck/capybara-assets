"""Stellt einen Helden auf Grün frei → 512x512 WebP wie outfit_*.webp.
Nur Grün, das mit dem Rand verbunden ist und kaum Rot hat, wird entfernt (neongrüne Kleidung bleibt).
Aufruf: cut_hero.py quelle.png ziel.webp  (braucht numpy, scipy, Pillow)"""
import sys, numpy as np
from PIL import Image
from scipy import ndimage
src, dst = sys.argv[1:3]
im = np.asarray(Image.open(src).convert("RGB")).astype(np.float32)
R, G, B = im[..., 0], im[..., 1], im[..., 2]
g = G - np.maximum(R, B)
cand = (g > 25) & (R < 95)
lab, n = ndimage.label(cand)
border = set(np.unique(np.concatenate([lab[0], lab[-1], lab[:, 0], lab[:, -1]]))) - {0}
bg = np.isin(lab, list(border)); edge = ndimage.binary_dilation(bg, iterations=2) & ~bg & (g > 0) & (R < 110)
a = np.ones_like(G); a[bg] = np.clip(1 - (g[bg] - 40) / 80, 0, 1); a[edge] = np.minimum(a[edge], np.clip(1 - (g[edge] - 10) / 90, 0.35, 1))
near = ndimage.binary_dilation(bg, iterations=3) & (R < 110)
sp = np.minimum(G, np.maximum(R, B)); im = im.copy(); im[..., 1] = np.where(near & (g > 0), sp, G)
rgba = np.dstack([im, a * 255]).astype(np.uint8); yy, xx = np.where(a > 0.5)
crop = Image.fromarray(rgba[yy.min():yy.max() + 1, xx.min():xx.max() + 1]); w, h = crop.size
k = min(470 / h, 480 / w); crop = crop.resize((int(w * k), int(h * k)), Image.LANCZOS)
out = Image.new("RGBA", (512, 512), (0, 0, 0, 0)); out.paste(crop, ((512 - crop.width) // 2, 498 - crop.height), crop)
out.save(dst, "WEBP", quality=90, method=6); print(dst, crop.size)
