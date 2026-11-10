#!/usr/bin/env python3
# V551: Tutorial-Schritt «HOLD THE RING» entfernt (Martin 10.11. 12:21: «versteht niemand»). Tutorial hat jetzt 5 Schritte,
# «TURN YOUR BLOCKS!» ist Schritt 5; die Welle startet weiterhin 2 s nach «ARM IT».
import sys
src, dst = sys.argv[1], sys.argv[2]
s = open(src, encoding="utf-8").read()
def rep(a, b, n=1):
    global s
    c = s.count(a); assert c == n, (c, a[:80]); s = s.replace(a, b)
rep('const GAME_VER = "V550";', 'const GAME_VER = "V551";')
rep('''  { t: "HOLD THE RING", s: "Monsters run the lane. Full laps cost lives. Clear rows for gold. Good luck, squad!", at: "board", done: () => TUT.t >= 10 },\n''', '')
rep('''        if (k === 5) return vis(document.getElementById("bRot"));   /* V545 */''', '''        if (k === 4) return vis(document.getElementById("bRot"));   /* V545 · V551: jetzt Schritt 5 (Index 4) */''')
rep('''  if (!wowDone("ton") && wowOk() && S.inWave && WOW.wt > 18 && !S.ton) {''', '''  if (false && !wowDone("ton") && wowOk() && S.inWave && WOW.wt > 18 && !S.ton) {   /* V551: SQUAD INCOMING abgeschaltet (Martin 10.11. 12:23) */''')
open(dst, "w", encoding="utf-8").write(s)
print("ok")
