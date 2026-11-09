#!/usr/bin/env python3
"""V545 (Martin 09.11. 22:33): «TURN YOUR BLOCKS!» als 6. Tutorial-Schritt direkt nach Schritt 5 «HOLD THE RING»
(gelber Pfeil auf die gelbe Drehen-Taste; fertig, sobald gedreht wurde, mit GOT IT nach 3 s oder nach 15 s).
GOT IT bei Schritt 5 führt jetzt zu Schritt 6 statt das Tutorial zu beenden. Wer das Tutorial überspringt,
bekommt den Dreh-Tipp weiter als Tipp-Karte in Welle 2; wer Schritt 6 gesehen hat, nicht noch einmal.
Aufruf: python3 tools/patch545.py site/index.html"""
import sys
p = sys.argv[1]; s = open(p, encoding="utf-8").read()
def rep(a, b, n=1):
    global s
    c = s.count(a); assert c == n, (c, a[:80]); s = s.replace(a, b)
rep('const GAME_VER = "V544";', 'const GAME_VER = "V545";')
rep('''at: "board", done: () => TUT.t >= 10 },''',
    '''at: "board", done: () => TUT.t >= 10 },
  { t: "TURN YOUR BLOCKS!", s: "Tap the yellow button in the middle to turn the falling block.", at: "bRot", rot: 1, done: () => (TUT.rot || 0) > (TUT.rb || 0) || TUT.t >= 15 },   /* V545 */''')
rep('const TUT_STEPS = [', '{ const _rotT = rotate; rotate = function () { try { if (TUT.on) TUT.rot = (TUT.rot || 0) + 1; } catch (e) {} return _rotT.apply(this, arguments); }; }   /* V545: Drehungen zählen */\nconst TUT_STEPS = [')
rep('function tutShow() { const st = TUT_STEPS[TUT.step];', 'function tutShow() { const st = TUT_STEPS[TUT.step]; if (st.rot) { TUT.rb = TUT.rot || 0; try { LS.set("tarnturm-tipb-rot", "1"); } catch (e) {} }   /* V545 */')
rep('const last = TUT.step === TUT_STEPS.length - 1;', 'const last = TUT.step >= 4;   /* V545: Schritt 5 und 6 mit GOT IT */')
rep('if (TUT.on) tutEnd(TUT.step < TUT_STEPS.length - 1); else hintEnd(); });',
    'if (TUT.on) { if (TUT.step === 4 && TUT_STEPS.length > 5) { TUT.step = 5; TUT.t = 0; tutShow(); return; } tutEnd(TUT.step < 4); } else hintEnd(); });   /* V545 */')
rep('''        if (k === 0) return vis(document.getElementById("bDrop"));''',
    '''        if (k === 0) return vis(document.getElementById("bDrop"));
        if (k === 5) return vis(document.getElementById("bRot"));   /* V545 */''')
open(p, "w", encoding="utf-8").write(s); print("ok V545")
