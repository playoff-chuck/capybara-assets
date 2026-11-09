#!/usr/bin/env python3
"""V543 (Martin 09.11. 21:57/21:58): neuer Tipp «TURN YOUR BLOCKS!» – wie die anderen Tipp-Karten: Spiel steht,
GOT IT erst nach 3 s, gelber Pfeil auf die gelbe Drehen-Taste in der Mitte. Kommt in Welle 2 vor dem Tipp
«SPLAT THEM WITH BLOCKS!», der kurz danach folgt (frühestens 5 s nach dem Schließen).
Tipps merken sich jetzt einen festen Schlüssel statt der Listenposition (alte Schlüssel 0/1/2 bleiben gültig).
Aufruf: python3 tools/patch543.py site/index.html"""
import sys
p = sys.argv[1]; s = open(p, encoding="utf-8").read()
def rep(a, b, n=1):
    global s
    c = s.count(a); assert c == n, (c, a[:80]); s = s.replace(a, b)
rep('const GAME_VER = "V542";', 'const GAME_VER = "V543";')
rep('''    { w: 2, t: "SPLAT THEM WITH BLOCKS!", p: "Blocks squash monsters. Speed a block down onto them – tap DROP.", at: "bDrop" },
    { w: 4, t: "CANNON ON THE RIGHT EDGE",''',
    '''    { k: "rot", w: 2, t: "TURN YOUR BLOCKS!", p: "Tap the yellow button in the middle to turn the falling block.", at: "bRot" },   /* V543 */
    { k: "0", w: 2, t: "SPLAT THEM WITH BLOCKS!", p: "Blocks squash monsters. Speed a block down onto them – tap DROP.", at: "bDrop" },
    { k: "1", w: 4, t: "CANNON ON THE RIGHT EDGE",''')
rep('''    { w: 5, t: "EDGES DON'T COUNT",''', '''    { k: "2", w: 5, t: "EDGES DON'T COUNT",''')
rep('const seen = i => { try { return LS.get("tarnturm-tipb-" + i) === "1"; } catch (e) { return true; } };',
    'const seen = i => { try { return LS.get("tarnturm-tipb-" + TIPS[i].k) === "1"; } catch (e) { return true; } };   /* V543: fester Schlüssel */')
rep('function show(i) { const T = TIPS[i]; cur = T; try { LS.set("tarnturm-tipb-" + i, "1"); } catch (e) {}',
    'function show(i) { const T = TIPS[i]; cur = T; try { LS.set("tarnturm-tipb-" + T.k, "1"); } catch (e) {}')
open(p, "w", encoding="utf-8").write(s); print("ok V543")
