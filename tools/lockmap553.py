#!/usr/bin/env python3
# V553: gesperrte Kontinente als Ebenen aus dem Nano-Banana-Entwurf (lock_v1, 2752×1536) schneiden.
# Aufruf: python3 tools/lockmap553.py <lock_v1.png> site/img
# Ergebnis: lock_asia/nam/ant/aus.webp (Ausschnitte, Position in FM_LOCKS) + fm_card.webp (Kartenbild für die Info-Karte).
import sys
import numpy as np
from PIL import Image, ImageFilter
from scipy import ndimage as nd
lock_src, out = sys.argv[1], sys.argv[2].rstrip("/")
W = Image.open(out + "/worldmap.webp").convert("RGB")
L = Image.open(lock_src).convert("RGB").resize(W.size, Image.LANCZOS)
a = np.asarray(W).astype(int); b = np.asarray(L).astype(int)
m = np.abs(a - b).sum(2) > 60
m = nd.binary_closing(m, iterations=3)
lab, n = nd.label(m); sz = nd.sum(m, lab, range(1, n + 1))
keep = np.isin(lab, [i + 1 for i, s in enumerate(sz) if s > 600]); keep = nd.binary_fill_holes(keep)
lab2, n2 = nd.label(keep); regs = {k: np.zeros_like(keep) for k in ["nam", "asia", "aus", "ant"]}
for i in range(1, n2 + 1):
    ys, xs = np.where(lab2 == i); cx, cy = xs.mean(), ys.mean()
    if cx < 640 and 380 < cy < 620: continue   # Rauschen in Südamerika
    k = "ant" if cy > 620 else "aus" if (cx > 1080 and cy > 410) else "nam" if cx < 640 else "asia"
    regs[k] |= (lab2 == i)
comp = W.convert("RGBA")
for k, r in regs.items():
    r = nd.binary_dilation(r, iterations=3)
    al = Image.fromarray((r * 255).astype("uint8")).filter(ImageFilter.GaussianBlur(1.5))
    im = L.copy().convert("RGBA"); im.putalpha(al); bb = al.getbbox()
    im.crop(bb).save(f"{out}/lock_{k}.webp", quality=88, method=6); print(k, bb)
    comp.alpha_composite(im)
comp.convert("RGB").resize((688, 384), Image.LANCZOS).save(out + "/fm_card.webp", quality=82, method=6)
print("ok")
