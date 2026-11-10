#!/usr/bin/env python3
# V550: Tutorial-Ende mit zu hohem Stapel → Ten-ton-Air-Drop-Karte, fällt nach Bestätigung sofort (Martin 10.11. 12:08)
# ersetzt das stille Zusammendrücken aus V548.
import sys
src, dst = sys.argv[1], sys.argv[2]
s = open(src, encoding="utf-8").read()
def rep(a, b, n=1):
    global s
    c = s.count(a); assert c == n, (c, a[:80]); s = s.replace(a, b)
rep('const GAME_VER = "V549";', 'const GAME_VER = "V550";')
rep('''                 weed: { img: "img/ad_drop_free.webp", name: "WEED DEFENSE DROP",''',
    '''                 tut: { img: "img/ad_drop_free.webp", name: "TEN-TON DROP", line: "Your stack is too high! HQ sends a Ten-ton. Confirm and it falls right now – it flattens the stack.", met: ["+1 Ten-ton", "Drops now"], btn: "DROP IT ▶" },   /* V550 */
                 weed: { img: "img/ad_drop_free.webp", name: "WEED DEFENSE DROP",''')
rep('''if (window.__dropKind === "squad") { window.__dropKind = null;''', '''if (window.__dropKind === "squad" || window.__dropKind === "tut") { window.__dropKind = null;''')
rep('''const vl = { ton: "ad_drop", friend: "ad_drop", squad: "ad_drop",''', '''const vl = { ton: "ad_drop", friend: "ad_drop", squad: "ad_drop", tut: "ad_drop",''')
rep('''if (kind === "sweep" || kind === "ton" || kind === "friend" || kind === "squad") [0.5, 0.8]''', '''if (kind === "sweep" || kind === "ton" || kind === "friend" || kind === "squad" || kind === "tut") [0.5, 0.8]''')
rep('''    try { if (S && S.started && !S.over) { let k = 0; while (k < 3 && stackHeight() >= GH - 8) { tonCompress(); k++; } if (k) { snd("tonFall"); toast("STACK SQUEEZED · fresh start", "HQ", 2200); } } } catch (e) {}''',
    '''    try { if (S && S.started && !S.over && !S.nuts && stackHeight() >= GH - 8 && window.__TT && window.__TT.ad) { S.tons = (S.tons || 0) + 1;   /* V550: Air-Drop statt stillem Zusammendrücken */
      setTimeout(() => { try { if (!S || !S.started || S.over) return; const ov = document.getElementById("ovAd"); if (ov && ov.hidden) window.__TT.ad.showDrop("tut"); else if (window.__dropAd) window.__dropAd("tut"); } catch (e) {} }, 700); } } catch (e) {}''')
rep('''$a("adTag").textContent = "✈ AIR DROP"; $a("adWave").textContent = `WAVE ${S.wave}`;''',
    '''$a("adTag").textContent = "✈ AIR DROP"; $a("adWave").textContent = S.wave ? `WAVE ${S.wave}` : "TUTORIAL";''')
open(dst, "w", encoding="utf-8").write(s)
print("ok")
