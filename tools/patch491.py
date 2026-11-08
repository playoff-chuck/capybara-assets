#!/usr/bin/env python3
"""V491: Squad File – Outfit-Raster (5 Spalten) bleibt gleich breit, auch bei langen Wörtern (RU «Исследователь» machte Spalte 3 auf 360 px 79 statt ~58 px).
Raster mit minmax(0,1fr) statt 1fr (auch Trophäen + Album-5er), Texte in den Outfit-Karten dürfen umbrechen (hyphens/overflow-wrap). Reine Optik.
Aufruf: python3 tools/patch491.py site/index.html"""
import sys
p = sys.argv[1]; s = open(p, encoding="utf-8").read()
def rep(a, b, n=1):
    global s
    c = s.count(a); assert c == n, (c, a[:80]); s = s.replace(a, b)

rep('const GAME_VER = "V490";', 'const GAME_VER = "V491";')
rep('.ofRow{display:grid;grid-template-columns:repeat(5,1fr);', '.ofRow{display:grid;grid-template-columns:repeat(5,minmax(0,1fr));')
rep('.ofRow .mcCard.off b.ofFx{color:#a89a85}', '.ofRow .mcCard.off b.ofFx{color:#a89a85}.ofRow .mcCard i,.ofRow .mcCard small,.ofRow .mcCard b.ofFx{overflow-wrap:anywhere;hyphens:auto;-webkit-hyphens:auto}')
rep('.trGrid{display:grid;grid-template-columns:repeat(5,1fr);', '.trGrid{display:grid;grid-template-columns:repeat(5,minmax(0,1fr));')
rep('.albGrid.c5{grid-template-columns:repeat(5,1fr)}', '.albGrid.c5{grid-template-columns:repeat(5,minmax(0,1fr))}')
open(p, "w", encoding="utf-8").write(s); print("ok V491")
