#!/usr/bin/env python3
"""V535 (Martin 09.11. 20:58): Tutorial-Knopf kleiner (40 px), näher am rosa Knopf, liegt unter der Bedienkapsel
(sitzt jetzt im Steuerbereich unterhalb der Tasten-Ebene statt darüber). Knopf schaltet das Tutorial ein und wieder aus
(bleibt sichtbar, solange das Tutorial läuft).
Aufruf: python3 tools/patch535.py site/index.html"""
import sys
p = sys.argv[1]; s = open(p, encoding="utf-8").read()
def rep(a, b, n=1):
    global s
    c = s.count(a); assert c == n, (c, a[:80]); s = s.replace(a, b)
rep('const GAME_VER = "V534";', 'const GAME_VER = "V535";')
rep('if (b.hidden === show) b.hidden = !show; if (show) { b.style.left = Math.round(r.right + 10) + "px"; b.style.top = Math.round(r.top + r.height / 2 - 26) + "px"; }',
    'const dk = document.querySelector(".deck"); if (dk && b.parentNode !== dk) dk.appendChild(b);\n      if (b.hidden === show) b.hidden = !show; if (show && dk) { const q = dk.getBoundingClientRect(); b.style.left = Math.round(r.right + 4 - q.left) + "px"; b.style.top = Math.round(r.top + r.height / 2 - 20 - q.top) + "px"; }')
rep('#bTut{position:fixed;z-index:58;width:52px;height:52px;', '#bTut{position:absolute;z-index:2;width:40px;height:40px;')
rep('#bTut svg{width:28px;height:28px;margin-top:2px}#bTut b{font:400 9px/1', '#bTut svg{width:21px;height:21px;margin-top:1px}#bTut b{font:400 7px/1')
rep('box-shadow:0 4px 0 #3a2414;display:flex;flex-direction:column;align-items:center;justify-content:center;gap:0}#bTut[hidden]', 'box-shadow:0 3px 0 #3a2414;display:flex;flex-direction:column;align-items:center;justify-content:center;gap:0;border-width:2.5px}#bTut[hidden]')
rep('if (!S || !S.started || S.over || TUT.on) return; S.paused = false; tutStart(); b.hidden = true; });', 'if (!S || !S.started || S.over) return; if (TUT.on) { tutEnd(true); return; } S.paused = false; tutStart(); });')
rep('(S.wave || 1) <= 10 && !TUT.on && !S.paused && !ovOpen);', '(S.wave || 1) <= 10 && !S.paused && !ovOpen); b.classList.toggle("on", !!TUT.on);')
rep('#bTut[hidden]{display:none!important}', '#bTut[hidden]{display:none!important}#bTut.on{background:#ffd34a}')
open(p, "w", encoding="utf-8").write(s); print("ok V535")
