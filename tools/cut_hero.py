"""Stellt einen Helden auf Grün frei → 512x512 WebP wie outfit_*.webp.
Aufruf: cut_hero.py quelle.png ziel.webp"""
import sys, numpy as np
from PIL import Image
src, dst = sys.argv[1:3]
im = np.asarray(Image.open(src).convert("RGB")).astype(np.float32)
R, G, B = im[..., 0], im[..., 1], im[..., 2]
g = G - np.maximum(R, B); a = np.clip(1 - (g - 40) / 80, 0, 1)
sp = np.minimum(G, np.maximum(R, B)); im = im.copy(); im[..., 1] = np.where(g > 0, sp, G)
rgba = np.dstack([im, a * 255]).astype(np.uint8); yy, xx = np.where(a > 0.5)
crop = Image.fromarray(rgba[yy.min():yy.max() + 1, xx.min():xx.max() + 1]); w, h = crop.size
k = min(470 / h, 480 / w); crop = crop.resize((int(w * k), int(h * k)), Image.LANCZOS)
out = Image.new("RGBA", (512, 512), (0, 0, 0, 0)); out.paste(crop, ((512 - crop.width) // 2, 498 - crop.height), crop)
out.save(dst, "WEBP", quality=90, method=6); print(dst, crop.size)
