import sys
# V709: Ausrüstungs-Angebot (ovAd) hält das Spiel immer selbst an – auch wenn show() ohne vorheriges S.intro aufgerufen wird (Megatest D8, Martin 14.11.2026).
src, dst = sys.argv[1], sys.argv[2]
s = open(src, encoding="utf-8").read()
def rep(a, b, n=1):
    global s
    c = s.count(a); assert c == n, (a[:60], c); s = s.replace(a, b)
rep('const GAME_VER = "V708";', 'const GAME_VER = "V709";')
rep('function show(k, sale) { try { if (typeof TUT !== "undefined" && TUT.on) return; } catch (e) {} const free = sale === "free";',
    'function show(k, sale) { try { if (typeof TUT !== "undefined" && TUT.on) return; } catch (e) {} if (!S.intro) { late = true; S.intro = true; S.adOpen = true; }   /* V709: Angebot hält das Spiel immer an */ const free = sale === "free";')
open(dst, "w", encoding="utf-8").write(s)
print("ok")
