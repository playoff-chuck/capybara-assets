#!/usr/bin/env python3
"""V475 – Sprach-Prüfung aller Screens (Martin 08.11. 20:19, Screenshot RU):
- Ticker/Laufband (#ticker, z. B. «SQUAD KIT · 2× every special …») wurde in langen Sprachen abgeschnitten (RU +40 px):
  Schrift schrumpft jetzt bis 9 px, danach darf der Text zweizeilig werden – nie mehr Ellipse.
- Übersetzungen über lang_src/*_v475.json: «CONTINUE» (Knopf gespeicherter Lauf), «# PTS», Toast-Teile «FIRST TRY COUNTS» / «+# % MAIN SCORE PER LEVEL».
Nutzung: python3 tools/patch475.py src dst"""
import sys, re
src, dst = sys.argv[1], sys.argv[2]
s = open(src, encoding="utf-8").read()

def rep(a, b, n=1):
    global s
    c = s.count(a)
    assert c == n, (c, a[:80])
    s = s.replace(a, b)

m = re.search(r'const GAME_VER = "V(\d+)";', s); v = int(m.group(1))
rep(m.group(0), f'const GAME_VER = "V{v + 1}";')

rep('  const t = $("ticker"); $("tkTag").textContent = tagShow(tag); $("tkTxt").textContent = txt;\n'
    '  t.hidden = false; t.classList.remove("go"); void t.offsetWidth; t.classList.add("go");',
    '  const t = $("ticker"); $("tkTag").textContent = tagShow(tag); $("tkTxt").textContent = txt;\n'
    '  t.hidden = false; t.classList.remove("go"); void t.offsetWidth; t.classList.add("go");\n'
    '  { const b = $("tkTxt"); const fit = () => { try { b.style.fontSize = ""; b.style.whiteSpace = ""; let fs = parseFloat(getComputedStyle(b).fontSize) || 12; let n = 0;\n'
    '      while (b.scrollWidth > b.clientWidth + 1 && fs > 9 && n++ < 8) { fs -= 0.5; b.style.fontSize = fs + "px"; }\n'
    '      if (b.scrollWidth > b.clientWidth + 1) { b.style.whiteSpace = "normal"; b.style.textAlign = "center"; } } catch (e) {} };\n'
    '    fit(); setTimeout(fit, 60); setTimeout(fit, 400); }   /* V475: Laufband schrumpft/umbricht statt abzuschneiden (RU, PT) */')
open(dst, "w", encoding="utf-8").write(s); print("ok", v + 1)
