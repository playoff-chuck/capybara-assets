#!/usr/bin/env python3
# V437 (/neu-Chat, Befund Video-Analyse W61–120): Boss-Hack-Angebot kam in W79 (Siberia-Sturmwelle) – Regel «Boss-Hack nie mit Sonderwelle».
# Ursache: das Angebot «nach W78» war aufgehalten und landete in der laufenden Sonderwelle. Jetzt: kein Angebot, solange eine Sonderwelle läuft
# oder die nächste Welle eine Sonderwelle ist (dann erst in der Pause danach); die Überfällig-Regel (+2 Wellen) bleibt.
import sys
src, dst = sys.argv[1], sys.argv[2]
s = open(src, encoding="utf-8").read()
def rep(a, b, n=1):
    global s
    assert s.count(a) == n, (s.count(a), a[:80])
    s = s.replace(a, b)
rep('const GAME_VER = "V436";', 'const GAME_VER = "V437";')
rep('if (S.hackPending && !S.drop && !S.ordersOpen && !S.duel && !S.paused && !S.intro && !S.mapShow && !S.ordDue && !hkSignFirst() && !(S.inWave && (S.wave || 0) % 30 === 0) &&',
    'if (S.hackPending && !S.drop && !S.ordersOpen && !S.duel && !S.paused && !S.intro && !S.mapShow && !S.ordDue && !hkSignFirst() && !(S.inWave && (S.wave || 0) % 30 === 0) && !(S.inWave && specBase() !== 0) && !(!S.inWave && specBase((S.wave || 0) + 1) !== 0) /* V437: nie in/vor einer Sonderwelle */ &&')
open(dst, "w", encoding="utf-8").write(s)
print("ok")
