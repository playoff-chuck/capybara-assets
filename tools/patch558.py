#!/usr/bin/env python3
# V558: Air-Drop vor den Unkraut-Wellen ohne Unkraut-Kommentar (Martin 10.11. 16:06): einfach «TEN-TON DROP», fällt sofort.
# Auch der Laden-Text der Zehntonne erwähnt die Samen nicht mehr.
import sys
src, dst = sys.argv[1], sys.argv[2]
s = open(src, encoding="utf-8").read()
def rep(a, b, n=1):
    global s
    c = s.count(a); assert c == n, (c, a[:80]); s = s.replace(a, b)
rep('const GAME_VER = "V557";', 'const GAME_VER = "V558";')
rep('weed: { img: "img/ad_drop_free.webp", name: "WEED DEFENSE DROP", line: "Weed seeds are about to land. HQ sent a Ten-ton drop – use it NOW to flatten the field before they sprout!", met: ["+1 Ten-ton", "Use it now"], btn: "DROP IT ▶" }',
    'weed: { img: "img/ad_drop_free.webp", name: "TEN-TON DROP", line: "HQ sends you a Ten-ton drop. Confirm and it falls right now.", met: ["+1 Ten-ton", "Drops now"], btn: "DROP IT ▶" }')
rep('squeezes all blocks to half. HQ drops a free one before weed seeds land.`', 'squeezes all blocks to half.`')
open(dst, "w", encoding="utf-8").write(s)
print("ok")
