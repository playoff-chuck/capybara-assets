#!/usr/bin/env python3
# V426 (Martin 07.11. 23:33): Unkraut-Wellen immer am Anfang eines Ortes (genug Wellen zum Wachsen), Unkraut lebt bis zum nächsten Ort.
# Unkraut: W81 ×1 (Ice Port; Sonar IV dafür von W81 → W86), W106 ×3 (Great Lakes), W126 ×4 (Penguin Bay), W131 ×5 (Glacier) – jeweils Orte ohne Sidewinder.
# Bei 3/4/5 Samen fällt vorher ein Gratis-Ten-ton (V425).
import sys
src, dst = sys.argv[1], sys.argv[2]
s = open(src, encoding="utf-8").read()
def rep(a, b, n=1):
    global s
    assert s.count(a) == n, (s.count(a), a[:80])
    s = s.replace(a, b)
rep('const GAME_VER = "V425";', 'const GAME_VER = "V426";')
rep("81: [4, 4]", "86: [4, 4]")
rep("  const WEEDN = { 110: 3, 124: 4, 130: 5 };   /* V425 */", "  const WEEDN = { 106: 3, 126: 4, 131: 5 };   /* V426: am Ortsanfang */")
rep('if (k === "weed") return [86, 110, 124, 130].includes(w) && ', 'if (k === "weed") return [81, 106, 126, 131].includes(w) && ')
rep("if (D.weed && (++D.weed.waves > 2 || (S.wave - 1) % 30 === 0 || ROT_BASES.includes(specBase())))",
    "if (D.weed && ((S.wave - 1) % 5 === 0 || ROT_BASES.includes(specBase())))   /* V426: lebt bis zum nächsten Ort */")
rep("const map = { blk: 65, mag: 80, weed: 86, weed3: 110, weed4: 124, weed5: 130,", "const map = { blk: 65, mag: 80, weed: 81, weed3: 106, weed4: 126, weed5: 131,")
open(dst, "w", encoding="utf-8").write(s)
print("ok")
