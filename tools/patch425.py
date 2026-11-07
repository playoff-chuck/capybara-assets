#!/usr/bin/env python3
# V425 (Martin 07.11. 23:28): Unkraut – W86 bleibt 1 Samen; W110 = 3, W124 = 4, W130 = 5 Samen in verschiedenen Spalten.
# In diesen Wellen fällt zuerst ein Gratis-Ten-ton (drückt den Stapel), die Samen fallen 3 s danach.
import sys
src, dst = sys.argv[1], sys.argv[2]
s = open(src, encoding="utf-8").read()
def rep(a, b, n=1):
    global s
    assert s.count(a) == n, (s.count(a), a[:80])
    s = s.replace(a, b)
rep('const GAME_VER = "V424";', 'const GAME_VER = "V425";')
rep("  const WEED5 = 124;", "  const WEEDN = { 110: 3, 124: 4, 130: 5 };   /* V425 */")
rep('if (k === "weed") return (w === WEED5 || [86, 110, 130].includes(w)) && ', 'if (k === "weed") return [86, 110, 124, 130].includes(w) && ')
rep('if (k === "weed") { const n = S.wave === WEED5 ? 5 : 1, pool = [];', 'if (k === "weed") { const n = WEEDN[S.wave] || 1, pool = [];')
rep("      D.weeds = xs.map(x => ({ x, root: null, h: 0, seedY: -1, growT: Math.random() * 1.5, waves: 0 })); }",
    "      const dl = n > 1 ? 3 : 0; if (n > 1) { try { if (!S.ton) { S.tons = (S.tons || 0) + 1; startTon(); } } catch (e) {} }   /* V425: erst Ten-ton, dann Samen */\n"
    "      D.weeds = xs.map(x => ({ x, root: null, h: 0, seedY: -1, growT: Math.random() * 1.5, waves: 0, delay: dl + Math.random() * 0.4 })); }")
rep('weed5: ["WEED FIELD!", "Five seeds at once · Tesla or Sniper cut them"]', 'weed5: ["WEED FIELD!", "Seeds after the drop · Tesla or Sniper cut them"]')
rep("      if (w.root == null) { w.seedY += dt * 6;", "      if (w.delay > 0) { w.delay -= dt; } else if (w.root == null) { w.seedY += dt * 6;")
rep("      for (const w of D.weeds) drawWeed(w, s);", "      for (const w of D.weeds) if (!(w.delay > 0)) drawWeed(w, s);")
rep("const map = { blk: 65, mag: 80, weed: 92, weed5: 124,", "const map = { blk: 65, mag: 80, weed: 86, weed3: 110, weed4: 124, weed5: 130,")
open(dst, "w", encoding="utf-8").write(s)
print("ok")
