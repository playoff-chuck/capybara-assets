#!/usr/bin/env python3
# V598 (Martin 11.11.): (1) 07:45 «immer nach der Urkunde» – 10T-Airdrop nach dem Kurs immer (nicht nur ab 7 Reihen), nicht beim Überspringen.
# (2) 07:45 Musik: vor dem Diplom 3 s ausblenden, dann Diplom; nach dem Diplom ein neues, schnelles Stück («Frostgnaw Sprint», 150 BPM),
# das bis zu seinem Ende weiterläuft (Wellenstart wechselt nicht sofort auf die Orts-Musik).
import sys
src, dst = sys.argv[1], sys.argv[2]
s = open(src, encoding="utf-8").read()
def rep(a, b, n=1):
    global s
    c = s.count(a); assert c == n, (c, a[:90]); s = s.replace(a, b)
rep('const GAME_VER = "V597";', 'const GAME_VER = "V598";')
# (1) 10T immer
rep('try { if (S && S.started && !S.over && !S.nuts && stackHeight() > 6 && window.__TT && window.__TT.ad) {   /* V565: ab 7 Reihen */',
    'try { if (S && S.started && !S.over && !S.nuts && arguments[0] !== true && window.__TT && window.__TT.ad) {   /* V565: ab 7 Reihen · V598: immer nach der Urkunde (nicht beim Überspringen) */')
# (2a) 3 s Ausblenden vor dem Diplom
rep('''    { const cr = document.getElementById("crate"), gv = document.getElementById("ovGive"); if ((cr && !cr.hidden) || (gv && !gv.hidden)) return; }
    window.__certNow();''', '''    { const cr = document.getElementById("crate"), gv = document.getElementById("ovGive"); if ((cr && !cr.hidden) || (gv && !gv.hidden)) return; }
    if (window.__certFade) return;   /* V598: Musik 3 s ausblenden, dann Diplom */
    let fade = false; try { if (TP.key && TP.el && !TP.el.paused) { tpFade(0.0001, 3); fade = true; } } catch (e) {}
    if (!fade) { window.__certNow(); return; }
    window.__certFade = 1; setTimeout(() => { window.__certFade = 0; try { if (TP.key && TP.el) TP.el.pause(); } catch (e) {} try { if (!window.__tutSumOpen && window.__tutSumPend) window.__certNow(); } catch (e) {} }, 3000);''')
# (2b) nach dem Diplom schnelles Stück
rep('''window.__tutSumOpen = false; window.__certQuietT = performance.now(); try { S.coachHold = false; snd("uiTap"); } catch (e) {}''',
    '''window.__tutSumOpen = false; window.__certQuietT = performance.now(); try { S.coachHold = false; snd("uiTap"); } catch (e) {}
    try { if (SFX.music && SFX.music.on) { TP.certHold = "frostgnaw"; tpPlay("frostgnaw"); } } catch (e) {}   /* V598: schnelles Stück nach dem Diplom */''')
rep('''  const begin = w => { if (!M.on) return; TP.wave = w; const pool = trkPool(w); TP.pool = pool;''',
    '''  const begin = w => { if (!M.on) return; TP.wave = w; const pool = trkPool(w); TP.pool = pool;
    if (TP.certHold && TP.key === TP.certHold && TP.el && !TP.el.paused && !TP.el.ended) return;   /* V598: Diplom-Stück läuft zu Ende */''')
rep("window.__TQ = () => ({ certQuiet, msgPush, buddyHelp, hint, ", "window.__TQ = () => ({ certQuiet, msgPush, buddyHelp, hint, tp: () => [TP.key, TP.el ? +TP.el.volume.toFixed(2) : -1, TP.el ? TP.el.paused : null], ")
open(dst, "w", encoding="utf-8").write(s)
print("ok", dst)
