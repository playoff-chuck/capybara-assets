#!/usr/bin/env python3
# V601 (Martin 11.11. 08:07): Auch in Lektion 7 «MONSTERS RUN THE RING» kommen die Steine über dem rechten Rand zu den Monstern,
# damit man sieht, wie ein Monster stirbt (wie Lektion 8, V599).
import sys
src, dst = sys.argv[1], sys.argv[2]
s = open(src, encoding="utf-8").read()
def rep(a, b, n=1):
    global s
    c = s.count(a); assert c == n, (c, a[:90]); s = s.replace(a, b)
rep('const GAME_VER = "V600";', 'const GAME_VER = "V601";')
rep('''setInterval(() => { try { if (!(TUT.on && S && S.piece && TUT_STEPS[TUT.step] && /SPLAT THEM/.test(TUT_STEPS[TUT.step].t) && !S.rotMode)) return;''',
    '''setInterval(() => { try { if (!(TUT.on && S && S.piece && TUT_STEPS[TUT.step] && /SPLAT THEM|MONSTERS RUN THE RING/.test(TUT_STEPS[TUT.step].t) && !S.rotMode)) return;   /* V601: auch Lektion 7 */''')
rep('''  try { if (TUT.on && TUT_STEPS[TUT.step] && /SPLAT THEM/.test(TUT_STEPS[TUT.step].t) && !S.rotMode) {''',
    '''  try { if (TUT.on && TUT_STEPS[TUT.step] && /SPLAT THEM|MONSTERS RUN THE RING/.test(TUT_STEPS[TUT.step].t) && !S.rotMode) {''')
open(dst, "w", encoding="utf-8").write(s)
print("ok", dst)
