#!/usr/bin/env python3
"""V507: Kein kurzes Vorab-Aufblitzen derselben Überschrift vor dem Air-Drop-Fenster (Martin 09.11. 15:45):
- SQUAD INCOMING: Banner entfällt, das Fenster kommt direkt (Horn bleibt).
- CLEAN SWEEP: großer Stempel entfällt, wenn danach das CLEAN-SWEEP-Fenster kommt (Klang + Stimme bleiben).
Aufruf: python3 tools/patch507.py site/index.html"""
import sys
p = sys.argv[1]; s = open(p, encoding="utf-8").read()
def rep(a, b, n=1):
    global s
    c = s.count(a); assert c == n, (c, a[:80]); s = s.replace(a, b)
rep('const GAME_VER = "V506";', 'const GAME_VER = "V507";')
rep('wowSet("ton"); WOW.tonT = performance.now(); S.wowTon = true; wowBanner("SQUAD INCOMING!", `${heroKey() === "rosie" ? "Blue" : "Rosie"} sends a free Ten-ton drop`);\n      snd("horn"); setTimeout(() => { if (!S.over) { S.tons = (S.tons || 0) + 1; if (window.__dropAd) window.__dropAd("squad"); else startTon(); } }, 1500); }',
    'wowSet("ton"); WOW.tonT = performance.now(); S.wowTon = true; if (!window.__dropAd) wowBanner("SQUAD INCOMING!", `${heroKey() === "rosie" ? "Blue" : "Rosie"} sends a free Ten-ton drop`);   /* V507: kein Vorab-Banner, das Fenster sagt es */\n      snd("horn"); setTimeout(() => { if (!S.over) { S.tons = (S.tons || 0) + 1; if (window.__dropAd) window.__dropAd("squad"); else startTon(); } }, window.__dropAd ? 300 : 1500); }')
rep('addMedal(2, true); praise("CLEAN SWEEP!", 4, "Clean sweep!"); setTimeout(() => airDrop("CLEAN SWEEP",',
    'addMedal(2, true); if (window.__dropAd && !S.nuts) { snd("stinger", 4); try { SFX.say("Clean sweep!"); } catch (e) {} } else praise("CLEAN SWEEP!", 4, "Clean sweep!");   /* V507: kein Stempel vor dem gleichnamigen Fenster */\n      setTimeout(() => airDrop("CLEAN SWEEP",')
open(p, "w", encoding="utf-8").write(s); print("ok V507")
