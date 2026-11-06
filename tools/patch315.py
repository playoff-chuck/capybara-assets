"""V315: Lucky Supply darf auch mitten in der Welle kommen – frühestens 30 s nach Wellenbeginn
(Martin 06.11. 12:39: «Lucky supply, geht 30 sek nach Wellenbeginn?»).
Bisher nur in der kurzen Wellenpause (waveCD > 2,5 s) und nie, solange ein Boss-Hack vorgemerkt war (!S.hackPending).
Mit V314 wartet der Boss-Hack auf Lucky Supply – beide Bedingungen zusammen blockierten Lucky Supply oft über viele Wellen.
Jetzt: Wellenpause wie bisher ODER Welle läuft schon ≥ 30 s; vorgemerkter Boss-Hack blockiert nicht mehr (er hat seine
eigene Ausnahme nach 2 Wellen). Alle übrigen Bedingungen (95-s-Takt, 30 s nach Fenster, nur Spielscreen) bleiben."""
import sys
src, dst = sys.argv[1], sys.argv[2]
s = open(src, encoding='utf-8').read()
def rep(a, b, cnt=1):
    global s
    n = s.count(a); assert n == cnt, (n, a[:70]); s = s.replace(a, b)

rep('const GAME_VER = "V314";', 'const GAME_VER = "V315";')
rep('&& (S.playT || 0) >= 60 && window.__offerOK() && !S.inWave && (S.waveCD || 0) > 2.5',
    '&& (S.playT || 0) >= 60 && window.__offerOK() && (!S.inWave ? (S.waveCD || 0) > 2.5 : performance.now() - (window.__waveStartAt || 1e18) >= 30000)   /* V315: auch ab 30 s in der Welle */')
rep('&& !(typeof hkOfferOn === "function" && hkOfferOn()) && !S.hackPending && (typeof inPlay !== "function" || inPlay()) && !document.hi',
    '&& !(typeof hkOfferOn === "function" && hkOfferOn()) && (typeof inPlay !== "function" || inPlay()) && !document.hi')
JS = r'''
/* V315: Wellenbeginn merken (für Lucky Supply ab 30 s in der Welle) */
try { let was = false; setInterval(() => { try { const on = !!(S && S.started && S.inWave); if (on && !was) window.__waveStartAt = performance.now(); if (!on) window.__waveStartAt = 0; was = on; } catch (e) {} }, 200); } catch (e) {}
'''
anchor = '})();\n</script>'
p = s.rindex(anchor); s = s[:p] + JS + s[p:]
open(dst, 'w', encoding='utf-8').write(s)
print("ok")
