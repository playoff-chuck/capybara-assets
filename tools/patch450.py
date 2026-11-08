#!/usr/bin/env python3
"""V450: Karten-Kopf – jede Information in einer eigenen Zeile (kein Umbruch mitten im Satz), gilt für alle Karten-Meldungen (Martin 08.11. 13:04).
Nutzung: python3 tools/patch450.py src dst"""
import sys
src, dst = sys.argv[1], sys.argv[2]
s = open(src, encoding="utf-8").read()

def rep(a, b, n=1):
    global s
    c = s.count(a)
    assert c == n, (c, a[:80])
    s = s.replace(a, b)

rep('GAME_VER = "V449"', 'GAME_VER = "V450"')
rep('function label(cont, place, sub) { ov.querySelector(".mapCont").textContent = cont || ""; ov.querySelector(".mapPlace").textContent = place || ""; ov.querySelector(".mapSub").textContent = sub || ""; }',
    'function label(cont, place, sub) { ov.querySelector(".mapCont").textContent = cont || ""; ov.querySelector(".mapPlace").textContent = place || ""; const esc = t => String(t).replace(/[&<>]/g, ch => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;" }[ch])); ov.querySelector(".mapSub").innerHTML = String(sub || "").split(" · ").filter(Boolean).map(p => `<span class="mapLn">${esc(p)}</span>`).join(""); }   /* V450: eine Information je Zeile */')
rep('.mapSub{font:700 12.5px/1.2 "Baloo 2",sans-serif;color:#7a5a3c;min-height:15px}',
    '.mapSub{font:700 12.5px/1.2 "Baloo 2",sans-serif;color:#7a5a3c;min-height:15px}.mapSub .mapLn{display:block;text-wrap:balance}')
open(dst, "w", encoding="utf-8").write(s)
print("ok", dst)
