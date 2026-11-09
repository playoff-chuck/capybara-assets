#!/usr/bin/env python3
"""V536: App-Icons aus Logo C1 (site/img/logo_main.webp) auf grünem Verlauf. Aufruf: python3 tools/icons536.py site"""
import sys, numpy as np
from PIL import Image, ImageFilter
site = sys.argv[1]
logo = Image.open(site + '/img/logo_main.webp').convert('RGBA')
def bg(S):
    y, x = np.mgrid[0:S, 0:S] / (S - 1)
    d = np.clip(np.hypot(x - .5, y - .42) / 0.72, 0, 1)
    c0 = np.array([205, 216, 126.]); c1 = np.array([118, 163, 60.])
    a = c0 + (c1 - c0) * (d ** 1.4)[..., None]
    return Image.fromarray(a.astype('uint8'), 'RGB').convert('RGBA')
def make(S, frac, out):
    b = bg(S); w = int(S * frac); h = int(logo.height * w / logo.width)
    L = logo.resize((w, h), Image.LANCZOS)
    sh = Image.new('RGBA', L.size, (0, 0, 0, 0)); a = L.split()[3].point(lambda v: int(v * 0.35)); sh.putalpha(a); sh = sh.filter(ImageFilter.GaussianBlur(S / 100))
    x = (S - w) // 2; y = (S - h) // 2
    b.alpha_composite(sh, (x, y + S // 90)); b.alpha_composite(L, (x, y))
    b.convert('RGB').save(out, optimize=True)
make(512, .86, site + '/icons/icon-512.png')
make(192, .86, site + '/icons/icon-192.png')
make(512, .66, site + '/icons/icon-maskable-512.png')
print("ok icons")
