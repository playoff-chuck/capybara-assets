#!/usr/bin/env python3
# V417 (Martin 07.11. 22:12): Sterne für absolvierte Orte auch in Antarktis und überall – bisher gab es keine Sterne in Testläufen
# (Dev-Sprung GO ▶ / 5·15·31·61·91·121, «Test from 0») und nach einem Weiterspielen mitten im Ort (Zähler fehlte bis zum nächsten Ortsanfang).
# Jetzt: Ort-Zähler wird bei jedem Wellenstart angelegt, wenn er fehlt oder zum falschen Ort gehört; Testläufe zählen mit.
import sys
src, dst = sys.argv[1], sys.argv[2]
s = open(src, encoding="utf-8").read()
def rep(a, b, n=1):
    global s
    assert s.count(a) == n, (s.count(a), a[:80])
    s = s.replace(a, b)
rep('const GAME_VER = "V416";', 'const GAME_VER = "V417";')
rep("  if (!S.nuts && !S.testRun && (S.wave - 1) % 5 === 0) S.pl = { g: Math.floor((S.wave - 1) / 5), lives: S.lives, lines: S.lines || 0, splat: S.splatN || 0, med: S.medGot || 0, kills: S.kills || 0 };   /* V374: Sterne je Ort · V402: Splats je Ort */",
    "  if (!S.nuts && ((S.wave - 1) % 5 === 0 || !S.pl || S.pl.g !== Math.floor((S.wave - 1) / 5))) S.pl = { g: Math.floor((S.wave - 1) / 5), lives: S.lives, lines: S.lines || 0, splat: S.splatN || 0, med: S.medGot || 0, kills: S.kills || 0 };   /* V374: Sterne je Ort · V402: Splats je Ort · V417: auch Testlauf / Einstieg mitten im Ort */")
rep("if (S.wave % 5 === 0 && !S.nuts && !S.testRun && S.pl && S.pl.g === Math.floor((S.wave - 1) / 5)) { const p = S.pl, st = [true,",
    "if (S.wave % 5 === 0 && !S.nuts && S.pl && S.pl.g === Math.floor((S.wave - 1) / 5)) { const p = S.pl, st = [true,")
open(dst, "w", encoding="utf-8").write(s)
print("ok")
