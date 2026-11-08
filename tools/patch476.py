#!/usr/bin/env python3
"""V476 – Tutorial hing im Nuts-Abstecher (Martin 08.11. 20:51, Screenshot DE «BAU EINEN TURM» in der Höhle):
?test=nuts (und jeder Test-/Dev-Sprung) startete erst ein normales Spiel; dort wurde das Tutorial für 0,7 s später geplant,
dann kam der Sprung in die Höhle – das Tutorial lief dort weiter, konnte aber keinen Turm kaufen (0 Gold).
Fix: (1) Tutorial-Start prüft beim Auslösen noch einmal Testlauf/Nuts; (2) startDetour beendet ein laufendes Tutorial
(ohne es als erledigt zu merken, damit es beim nächsten normalen Spiel kommt).
Nutzung: python3 tools/patch476.py src dst"""
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

rep('  if (LS.get("tarnturm-tut") !== "1" && !fromWave && !S.testRun) { S.ff = false; S.waveCD = 60; setTimeout(tutStart, 700); }',
    '  if (LS.get("tarnturm-tut") !== "1" && !fromWave && !S.testRun) { S.ff = false; S.waveCD = 60; setTimeout(() => { if (S && S.started && !S.over && !S.testRun && !S.nuts && !S.replay) tutStart(); }, 700); }   /* V476: nicht nach Test-/Nuts-Sprung */')
rep('function startDetour(c) {\n  const fr = buildSave(); if (!fr) return;',
    'function startDetour(c) {\n  if (TUT.on) { try { TUT.on = false; S.coachHold = false; $("coach").hidden = true; coachHi(null); } catch (e) {} }   /* V476: Tutorial gehört nicht in die Höhle (bleibt für das nächste normale Spiel offen) */\n  const fr = buildSave(); if (!fr) return;')
open(dst, "w", encoding="utf-8").write(s); print("ok", v + 1)
