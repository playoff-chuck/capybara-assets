"""V230: Geister-Klick-Sperre (Sonar-Fehler «Turm gekauft, aber nicht bewaffnen»).
Am Handy öffnet der Fingertipp aufs Feld (pointerdown) das Turm-Fenster; der danach vom Browser erzeugte
mousedown/mouseup/click landete an derselben Stelle im neuen Fenster (z. B. auf «Close») und schloss es sofort.
Jetzt werden diese Nachzügler-Ereignisse 650 ms lang verschluckt, wenn sie innerhalb von 40 px vom Fingertipp
und nicht auf dem Spielfeld liegen."""
import sys
src, dst = sys.argv[1], sys.argv[2]
s = open(src, encoding='utf-8').read()
def rep(a, b, cnt=1):
    global s
    n = s.count(a); assert n == cnt, (n, a[:70]); s = s.replace(a, b)
rep('const GAME_VER = "V229";', 'const GAME_VER = "V230";')
js = '''
  /* V230: Geister-Klick nach Fingertipp aufs Feld verschlucken (Turm-Fenster schloss sich sonst sofort) */
  try { let gT = 0, gX = 0, gY = 0;
    window.addEventListener("pointerdown", e => { if (e.pointerType === "mouse") return; const t = e.target; if (t && t.tagName === "CANVAS") { gT = performance.now() + 650; gX = e.clientX; gY = e.clientY; } }, true);
    const swallow = e => { if (performance.now() > gT) return; const t = e.target; if (t && t.tagName === "CANVAS") return; if (Math.hypot(e.clientX - gX, e.clientY - gY) > 40) return; e.stopImmediatePropagation(); e.preventDefault(); if (e.type === "click") gT = 0; };
    ["mousedown", "mouseup", "click"].forEach(tp => window.addEventListener(tp, swallow, true)); } catch (e) { console.error("ghost", e); }
'''
i = s.rfind('})();\n</script>'); s = s[:i] + js + s[i:]
open(dst, 'w', encoding='utf-8').write(s); print('ok')
