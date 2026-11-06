"""V339 (Martin 06.11. 23:43): Unkraut-Same landet mit einem kleinen, leisen «Plumps» (statt Lock-Klang).
Blüte wächst mit der Pflanze mit, wird aber nie breiter als ein Kästchen.
Test-Links (?test=… und Dev-Liste): die Welle läuft mind. 3 Minuten (Monster kommen nach), damit man in Ruhe testen kann.
Magnet-Brummen −50 % (0,14 → 0,07)."""
import sys
src, dst = sys.argv[1], sys.argv[2]
s = open(src, encoding='utf-8').read()
def rep(a, b, cnt=1):
    global s
    n = s.count(a); assert n == cnt, (n, a[:70]); s = s.replace(a, b)
rep('const GAME_VER = "V338";', 'const GAME_VER = "V339";')
rep('if (w.seedY >= ly) { w.root = ly; w.h = 1; snd("lock"); }',
    'if (w.seedY >= ly) { w.root = ly; w.h = 1; try { tone(260, 110, 0.11, 0.035, 0, "sine", 900); tone(140, 90, 0.08, 0.02, 0.02, "triangle", 500); } catch (e) {} }')
rep('br = s * 0.13 * Math.min(1, hv);', 'br = s * (0.07 + 0.19 * Math.min(1, Math.max(0, hv - 1) / 8));   /* V339: wächst mit, max. ~1 Kästchen breit (Durchmesser ≈ 3,7·br ≤ 0,96 Kästchen) */')
rep('if (DK.includes(kind)) { S.snipes = (S.snipes || 0) + 2; S.teslas = (S.teslas || 0) + 2; S.waveCD = 3;',
    'if (DK.includes(kind)) { S.snipes = (S.snipes || 0) + 2; S.teslas = (S.teslas || 0) + 2; S.waveCD = 3; S.testLongW = w; S.testLongUntil = performance.now() + 180000;')
rep('hum.g.gain.setTargetAtTime(on ? 0.14 : 0,', 'hum.g.gain.setTargetAtTime(on ? 0.07 : 0,')
JS = r'''
/* V339: Test-Wellen laufen mind. 3 Minuten */
try { (() => {
  setInterval(() => { try { if (!S || !S.started || S.over || !S.testRun || !S.testLongUntil) return;
    if (S.wave !== S.testLongW || performance.now() > S.testLongUntil) { S.testLongUntil = 0; return; }
    if (S.inWave && S.toSpawn < 5) S.toSpawn += 5; } catch (e) {} }, 250);
})(); } catch (e) { console.error("v339", e); }
'''
anchor = '})();\n</script>'
p = s.rindex(anchor); s = s[:p] + JS + s[p:]
open(dst, 'w', encoding='utf-8').write(s)
print("ok")
