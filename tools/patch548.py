#!/usr/bin/env python3
# V548: Anfänger-Hilfen (Natascha 10.11.): Reihen-Tipp, frühe Stapel-Warnung, Gold-Tipp + Shop-Puls,
# Turm-verloren-Tipp, Stapel nach Tutorial-Ende zusammendrücken.
import sys
src, dst = sys.argv[1], sys.argv[2]
s = open(src, encoding="utf-8").read()
def rep(a, b, n=1):
    global s
    c = s.count(a); assert c == n, (c, a[:80]); s = s.replace(a, b)
rep('const GAME_VER = "V547";', 'const GAME_VER = "V548";')
rep('''  const TIPS = [
    { k: "rot",''', '''  const TIPS = [
    { k: "stack", c: () => S.wave <= 40 && GH - stackHeight() <= 4, t: "YOUR STACK IS TOO HIGH!", p: "If the blocks reach the top, the game is over. Fill rows to clear them – drop blocks into the gaps." },   /* V548 */
    { k: "rot",''')
rep('''    { k: "2", w: 5, t: "EDGES DON'T COUNT", p: "The outer squares on the left and right don't need blocks – a row clears without them." }];''',
'''    { k: "2", w: 5, t: "EDGES DON'T COUNT", p: "The outer squares on the left and right don't need blocks – a row clears without them." },
    { k: "row", c: () => S.wave >= 2 && S.wave <= 12 && !(S.lines | 0) && stackHeight() >= 4, t: "FILL A ROW – IT DISAPPEARS!", p: "Fill a whole row with blocks and it clears. You get gold and room to breathe." },   /* V548 */
    { k: "gold", c: () => S.wave >= 2 && S.wave <= 15 && (S.gold | 0) >= 300 && S.towers.size <= 2, t: "SPEND YOUR GOLD!", p: "You have gold to spare. Tap the shop and build more towers – you can have several at once.", at: "bBuild" },   /* V548 */
    { k: "lost", c: () => !!S.towerLost && S.wave <= 40, t: "TOWER LOST? NO PROBLEM!", p: "A tower can fall when its block disappears. Just build a new one – you can have several towers at the same time." }];   /* V548 */''')
rep('''const i = TIPS.findIndex((T, k) => !seen(k) && S.wave >= T.w && S.wave <= T.w + 3);''',
    '''const i = TIPS.findIndex((T, k) => !seen(k) && (T.c ? T.c() : S.wave >= T.w && S.wave <= T.w + 3));''')
rep('''/* V325: keine «soldier»-Sprüche */''', '''/* V548: Anfänger-Hilfen */
try { (() => {
  const _snd = snd; snd = function (k) { try { if (k === "towerLost" && S && S.started && !S.nuts) S.towerLost = 1; } catch (e) {} return _snd.apply(this, arguments); };
  let warnW = -1;
  setInterval(() => { try {
    const bb = document.getElementById("bBuild");
    const pulse = !!(S && S.started && !S.over && !S.nuts && !S.testRun && S.wave >= 1 && S.wave <= 10 && (S.gold | 0) >= 300 && !S.shop && !S.mode);
    if (bb) bb.classList.toggle("goldPulse", pulse);
    if (!S || !S.started || S.over || S.nuts || !S.inWave || S.wave > 40) return;
    if (GH - stackHeight() <= 4 && warnW !== S.wave && LS.get("tarnturm-tipb-stack") === "1" && !(window.__tipBulb && window.__tipBulb.open)) { warnW = S.wave; toast("STACK TOO HIGH · fill rows to clear them", "HQ", 2600); }
  } catch (e) {} }, 500);
  const _te = tutEnd; tutEnd = function () { const r = _te.apply(this, arguments);
    try { if (S && S.started && !S.over) { let k = 0; while (k < 3 && stackHeight() >= GH - 8) { tonCompress(); k++; } if (k) { snd("tonFall"); toast("STACK SQUEEZED · fresh start", "HQ", 2200); } } } catch (e) {}
    return r; };
})(); } catch (e) { console.error("v548", e); }

/* V325: keine «soldier»-Sprüche */''')
rep('''#tipBulb.on{opacity:1;''', '''#bBuild.goldPulse{animation:goldPulse 1.1s ease-in-out infinite}@keyframes goldPulse{50%{box-shadow:0 0 0 4px #ffd23a,0 0 14px 4px #ffd23a;transform:scale(1.06)}}
#tipBulb.on{opacity:1;''')
open(dst, "w", encoding="utf-8").write(s)
print("ok")
