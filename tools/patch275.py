"""V275: alter Dev-Schalter «Intros off» (seit V264 ohne Knopf) wird ignoriert und gelöscht –
sonst unterdrückt ein gespeichertes Flag dauerhaft alle Neuheiten-Fenster und Waffen-Anzeigen.
Martin 16:07: Flugzeuggeräusch nur bei der allerersten Sequenz (Welttour-Start, Flug von außerhalb) +25 %."""
import sys
src, dst = sys.argv[1], sys.argv[2]
s = open(src, encoding='utf-8').read()
def rep(a, b, cnt=1):
    global s
    n = s.count(a); assert n == cnt, (n, a[:70]); s = s.replace(a, b)
rep('const GAME_VER = "V274";', 'const GAME_VER = "V275";')
rep('const introsOff = () => LS.get("tarnturm-dev") === "1" && LS.get("tarnturm-devnointro") === "1";',
    'try { LS.del("tarnturm-devnointro"); } catch (er) {} const introsOff = () => false;')
rep('const ac = AU.ac(), out = AU.out(); if (!ac || !out) return; const T = ac.currentTime + 0.02, D = Math.max(1.2, ms / 1000);',
    'const ac = AU.ac(), out0 = AU.out(); if (!ac || !out0) return; let out = out0;   /* V275: erste Sequenz +25 % */\n'
    '      if (fromOff && !window.__planeFirstDone) { window.__planeFirstDone = true; const bo = ac.createGain(); bo.gain.value = 1.25; bo.connect(out0); out = bo; }\n'
    '      const T = ac.currentTime + 0.02, D = Math.max(1.2, ms / 1000);')
open(dst, 'w', encoding='utf-8').write(s)
