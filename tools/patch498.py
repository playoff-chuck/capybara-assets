#!/usr/bin/env python3
"""V498: Tutorial-, Hinweis- und Tipp-Fenster oben ins Spielfeld statt in die Mitte/unten – Landestelle und Stapel bleiben sichtbar (Martin 09.11. 11:52).
Aufruf: python3 tools/patch498.py site/index.html"""
import sys
p = sys.argv[1]; s = open(p, encoding="utf-8").read()
def rep(a, b, n=1):
    global s
    c = s.count(a); assert c == n, (c, a[:80]); s = s.replace(a, b)
rep('const GAME_VER = "V497";', 'const GAME_VER = "V498";')
rep('br.height * 0.5 - 70', '6', 4)
rep('br.height * 0.5 - 90', '6')
# Tipp-Karte: oben am Spielfeld statt fest 190 px über dem Boden
rep('card.hidden = false; requestAnimationFrame(() => card.classList.add("on"));',
    'try { const bd = document.getElementById("board"); if (bd) { const br = bd.getBoundingClientRect(); card.style.top = Math.max(6, br.top + 6) + "px"; card.style.bottom = "auto"; } } catch (e) {}   /* V498: oben ins Feld */\n    card.hidden = false; requestAnimationFrame(() => card.classList.add("on"));')
open(p, "w", encoding="utf-8").write(s); print("ok V498")
