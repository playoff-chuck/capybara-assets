#!/usr/bin/env python3
"""V471 – t136 Rest (Karten-Intro u. a.): Texte, die vor dem Laden der Sprachtabelle entstanden (Weltkarte «tap to skip» …),
wurden als «erledigt» gemerkt und blieben englisch → vor dem Laden nichts merken. Neue Muster (tools/lang_src/<lang>_v471.json):
Karten-Intro (Welcome to Capybara World!, # continents/places/waves, Flying to @, First stop: @, the Jungle Temple waits at wave #),
Richtungs-Schild «◀ @»/«@ ▶», WORLD TILT −90° und BLIZZARD · −40° (Minus gehört zur Zahl).
Nutzung: python3 tools/patch471.py src dst"""
import sys
src, dst = sys.argv[1], sys.argv[2]
s = open(src, encoding="utf-8").read()

def rep(a, b, n=1):
    global s
    c = s.count(a)
    assert c == n, (c, a[:80])
    s = s.replace(a, b)

rep('const GAME_VER = "V470";', 'const GAME_VER = "V471";')
rep('function i18nText(n) { const d = n.data; if (!d || !d.trim()) return;',
    'function i18nText(n) { if (!I18N.dict) return;   /* V471: vor dem Laden nichts als erledigt merken */ const d = n.data; if (!d || !d.trim()) return;')
rep('function i18nAttr(el, a) { const v = el.getAttribute(a),',
    'function i18nAttr(el, a) { if (!I18N.dict) return; const v = el.getAttribute(a),')
open(dst, "w", encoding="utf-8").write(s)
print("ok V471")
