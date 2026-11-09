#!/usr/bin/env python3
"""V496: neues Logo C1 (Schrift im engen Bogen hinter dem Capybara, Martin 09.11. 11:26) überall: Menü, Share-Bild, Einladungs-Bild.
Bild: img/logo_main.webp ersetzt (separat kopieren). Aufruf: python3 tools/patch496.py site/index.html"""
import sys
p = sys.argv[1]; s = open(p, encoding="utf-8").read()
def rep(a, b, n=1):
    global s
    c = s.count(a); assert c == n, (c, a[:80]); s = s.replace(a, b)
rep('const GAME_VER = "V495";', 'const GAME_VER = "V496";')
rep('const MAIN_LOGO = "img/logo_main.webp?v=258";', 'const MAIN_LOGO = "img/logo_main.webp?v=496";')
rep('href="img/logo_main.webp?v=227"', 'href="img/logo_main.webp?v=496"')
rep('if (logo) { const lw = 600, lh = logo.naturalHeight * lw / logo.naturalWidth; g.drawImage(logo, (W - lw) / 2, 24, lw, Math.min(lh, 380)); }',
    'if (logo) { const k = Math.min(600 / logo.naturalWidth, 380 / logo.naturalHeight), lw = logo.naturalWidth * k, lh = logo.naturalHeight * k; g.drawImage(logo, (W - lw) / 2, 24, lw, lh); }   /* V496: Seitenverhältnis halten */')
rep('if (logo) { const lw = 280, lh = logo.naturalHeight * lw / logo.naturalWidth; g.drawImage(logo, 36, 30, lw, Math.min(lh, 170)); }',
    'if (logo) { const k = Math.min(280 / logo.naturalWidth, 250 / logo.naturalHeight), lw = logo.naturalWidth * k, lh = logo.naturalHeight * k; g.drawImage(logo, 36, 26, lw, lh); }   /* V496 */')
open(p, "w", encoding="utf-8").write(s); print("ok V496")
