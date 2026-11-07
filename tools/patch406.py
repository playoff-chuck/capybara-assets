#!/usr/bin/env python3
# V406: Lob-Staffelung – jede 5. Welle ohne Durchbruch (Boss-Wellen) bekommt die Spitzenstufe
# (Legendary / Unstoppable / Flawless, nie zweimal gleich) statt immer «Flawless!».
import sys
src, dst = sys.argv[1], sys.argv[2]
s = open(src, encoding="utf-8").read()
def rep(a, b, n=1):
    global s
    assert s.count(a) == n, (s.count(a), a[:80])
    s = s.replace(a, b)
rep('const GAME_VER = "V405";', 'const GAME_VER = "V406";')
rep('if (S.wave % 5 === 0) praise(`WAVE ${S.wave}!`, S.waveLeaks === 0 ? 3 : 2, S.waveLeaks === 0 ? "Flawless!" : "Keep going!");',
    'if (S.wave % 5 === 0) { if (S.waveLeaks === 0) { const w = lobWord(5); praise(w.toUpperCase(), 4, w); } else praise(`WAVE ${S.wave}!`, 2, "Keep going!"); }   /* V406: Spitzenlob ohne Durchbruch */')
open(dst, "w", encoding="utf-8").write(s)
print("ok")
