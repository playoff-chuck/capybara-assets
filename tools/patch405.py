#!/usr/bin/env python3
# V405: W8 – Gear-Vorstellung Ten-ton und Air-Drop-Fenster nicht mehr nacheinander.
# Wenn die Vorstellung in derselben Welle schon lief (oder noch aussteht), kein zweites Fenster;
# das «WAVE CLEARED»-Banner zeigt den +1 Ten-ton ohnehin. Kein doppelter Eintrag in introQ.
import sys
src, dst = sys.argv[1], sys.argv[2]
s = open(src, encoding="utf-8").read()
def rep(a, b, n=1):
    global s
    assert s.count(a) == n, (s.count(a), a[:80])
    s = s.replace(a, b)
rep('const GAME_VER = "V404";', 'const GAME_VER = "V405";')
rep('if (!S.seen["g:ton"]) S.introQ.push({ t: "gear", k: "ton" }); else if (window.__dropAd) window.__dropAd("ton"); }',
    'if (!S.seen["g:ton"]) { if (!S.introQ.some(x => x && x.k === "ton")) S.introQ.push({ t: "gear", k: "ton" }); } else if (window.__dropAd && S.introWave !== S.wave) window.__dropAd("ton"); }   /* V405: kein Doppelfenster in W8 */')
open(dst, "w", encoding="utf-8").write(s)
print("ok")
