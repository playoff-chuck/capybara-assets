#!/usr/bin/env python3
# V600 (Martin 11.11. 08:00): «Monster-Rush und nach 45 Sekunden Werbung vom Boss-Hack-Trainer. Wenn nicht angenommen, nach 1 min wieder.»
# (1) Erste Welle nach dem Diplom = MONSTER RUSH: doppelt so viele Monster, 25 % langsamer, Banner (durchbricht die Ruhe nach der Urkunde).
# (2) Werbung Coach Ollie nach dem ersten Boss-Hack (W4) und, wenn nicht gebucht, noch einmal nach dem zweiten (W12) – Martin 08:03/08:04.
import sys
src, dst = sys.argv[1], sys.argv[2]
s = open(src, encoding="utf-8").read()
def rep(a, b, n=1):
    global s
    c = s.count(a); assert c == n, (c, a[:90]); s = s.replace(a, b)
rep('const GAME_VER = "V599";', 'const GAME_VER = "V600";')
# Rush in startWave
rep('''if (S.nuts) { S.toSpawn = S.waveTotal = nutsCount(S.nuts.lvl); } S.spawnT = 0; S.spawnIdx = 0; S.inWave = true; S.waveLeaks = 0;''',
    '''if (S.nuts) { S.toSpawn = S.waveTotal = nutsCount(S.nuts.lvl); } S.spawnT = 0; S.spawnIdx = 0; S.inWave = true; S.waveLeaks = 0;
  if (S.rushNext && !S.nuts && !S.testRun) { S.rushNext = 0; S.rushW = S.wave; S.toSpawn = S.waveTotal = S.toSpawn * 2; setTimeout(() => { try { snd("siren"); announce("MONSTER RUSH!", "Twice the monsters – squash them with blocks and the Ten-ton!", "ALERT", 3200); } catch (e) {} }, 600); }   /* V600: Monster-Rush nach dem Diplom */''')
rep('''  const spF = (ffOn() ? sp * 1.7 : sp) *''', '''  const spF = (S.rushW === S.wave ? 0.75 : 1) * (ffOn() ? sp * 1.7 : sp) *''')
rep('''  try { if (certQuiet()) return; } catch (e) {}   /* V595 */''', '''  try { if (certQuiet() && m.title !== "MONSTER RUSH!") return; } catch (e) {}   /* V595 · V600: Rush-Banner darf */''')
# Diplom zu: Rush vormerken + Coach-Werbung
rep('''    try { if (SFX.music && SFX.music.on) { TP.certHold = "frostgnaw"; tpPlay("frostgnaw"); } } catch (e) {}   /* V598: schnelles Stück nach dem Diplom */''',
    '''    try { if (SFX.music && SFX.music.on) { TP.certHold = "frostgnaw"; tpPlay("frostgnaw"); } } catch (e) {}   /* V598: schnelles Stück nach dem Diplom */
    try { if (!S.nuts && !S.testRun) S.rushNext = 1; } catch (e) {}   /* V600 */''')
# Coach-Werbung nach dem ersten Boss-Hack (Martin 08:03) und – falls nicht gebucht – noch einmal nach dem zweiten (W12, Martin 08:04)
rep('''if (!HK.coach && !HK.trial && S && !S.testRun && !S.nuts && LS.get("capy-coach-ad1") !== "1") window.__coachAdPend = 1;''',
    '''if (!HK.coach && !HK.trial && S && !S.testRun && !S.nuts && (LS.get("capy-coach-ad1") !== "1" || (LS.get("capy-coach-ad2") !== "1" && coachLeft() === 0 && (LS.set("capy-coach-ad2", "1"), true)))) window.__coachAdPend = 1;   /* V600: 2. Hack (W12) noch einmal, wenn nicht gebucht */''')
open(dst, "w", encoding="utf-8").write(s)
print("ok", dst)
