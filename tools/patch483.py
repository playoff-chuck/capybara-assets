#!/usr/bin/env python3
"""V483 – Tutorial: Steine fallen in allen 5 Schritten weiter (Martin 08.11. 23:24: «solange man Schritt 5 nicht wegdrückt, fallen keine Steine – damit sieht man nicht, wie das Spiel läuft»).
Vorher: Schritte 1–4 setzten gravT zurück (Block wartete), Schritt 5 hielt das ganze Spiel an (coachHold). Jetzt: Blöcke fallen immer; die Welle wartet weiter bis Schritt 5
(dann Start nach 2 s, Karte bleibt mit «Got it» offen, Spiel läuft). Nutzung: python3 tools/patch483.py src dst"""
import sys, re
src, dst = sys.argv[1], sys.argv[2]
s = open(src, encoding="utf-8").read()
def rep(a, b, n=1):
    global s
    c = s.count(a); assert c == n, (c, a[:80]); s = s.replace(a, b)
m = re.search(r'const GAME_VER = "V(\d+)";', s); v = int(m.group(1))
rep(m.group(0), f'const GAME_VER = "V{v + 1}";')
rep('''  if (TUT.step < 4) { S.waveCD = Math.max(S.waveCD, 6); S.inWave = false; S.gravT = 0; }   /* V320: Block wartet im Tutorial */''',
    '''  if (TUT.step < 4) { S.waveCD = Math.max(S.waveCD, 6); S.inWave = false; }   /* V320: Welle wartet im Tutorial · V483: Blöcke fallen weiter (Martin 08.11.) */''')
rep('''const last = TUT.step === TUT_STEPS.length - 1; S.coachHold = last; $("coachSkip").textContent = last ? "Got it" : "Skip tutorial";''',
    '''const last = TUT.step === TUT_STEPS.length - 1; S.coachHold = false; $("coachSkip").textContent = last ? "Got it" : "Skip tutorial";   /* V483: Spiel läuft auch bei Schritt 5 weiter */''')
rep('''  { t: "HOLD THE RING", s: "Monsters run the lane. Full laps cost lives. Clear rows for gold. Good luck, squad!", at: "board", done: () => false },   /* V367: endet mit «Got it», Spiel steht bis dahin */''',
    '''  { t: "HOLD THE RING", s: "Monsters run the lane. Full laps cost lives. Clear rows for gold. Good luck, squad!", at: "board", done: () => false },   /* V367: endet mit «Got it» · V483: Spiel läuft dabei weiter */''')
open(dst, "w", encoding="utf-8").write(s); print("ok", v + 1)
