"""V263 (Martin 05.11. 14:30): Flugzeug ruckelt → flüssig.
- Teure Filter (zwei drop-shadow auf dem fliegenden, innen animierten Flugzeug) entfernt; Schatten jetzt als weiche Ellipse
  (Verlauf, kein Filter) – muss nicht mehr jedes Bild neu gerechnet werden.
- Flugzeug eigene Ebene (translateZ/backface), Spiegelung nach Flugrichtung und Schaukeln wieder auf den neuen Aufbau (V262) gelegt.
- Bewegung mit sanfterer Kurve (ease-in-out sinus) und ohne Sprünge am Anfang."""
import sys
src, dst = sys.argv[1], sys.argv[2]
s = open(src, encoding='utf-8').read()
def rep(a, b, cnt=1):
    global s
    n = s.count(a); assert n == cnt, (n, a[:70]); s = s.replace(a, b)
rep('const GAME_VER = "V262";', 'const GAME_VER = "V263";')
rep('e = t < .5 ? 2 * t * t : 1 - Math.pow(-2 * t + 2, 2) / 2, x = a[0]', 'e = 0.5 - Math.cos(Math.PI * t) / 2, x = a[0]')
css = r'''
<style id="v263plane">
#ovMap .mapPlane{filter:none!important;backface-visibility:hidden}
#ovMap .mapPlane .biPlane{transform:scaleX(var(--fx,1)) translateZ(0);filter:none!important;animation:biBob 1.4s ease-in-out infinite;will-change:transform}
#ovMap .mapPlane .biPlane::before{content:"";position:absolute;left:14%;right:10%;bottom:-16%;height:20%;border-radius:50%;background:radial-gradient(ellipse at center,rgba(0,0,0,.28),rgba(0,0,0,0) 70%)}
@media (prefers-reduced-motion:reduce){#ovMap .mapPlane .biPlane{animation:none}}
</style>
'''
i = s.rfind('</body>'); s = s[:i] + css + s[i:]
open(dst, 'w', encoding='utf-8').write(s); print('ok')
# Nachtrag 14:31: keine zwei Anzeigen direkt hintereinander (mind. 45 s Abstand)
s = open(dst, encoding='utf-8').read()
rep('lastW = why(k); paint(); $("ovIntro").hidden = true; ov.hidden = false;', 'lastW = why(k); paint(); window.__adLast = performance.now(); $("ovIntro").hidden = true; ov.hidden = false;')
rep('if (q.k === "ton") { show("ton", false); S.adDue.ton = 1; }', 'const recent = performance.now() - (window.__adLast || -1e9) < 45000;\n          if (q.k === "ton") { if (!recent) show("ton", false); S.adDue.ton = 1; }')
rep('else if (!why(q.k)) show(q.k, true);', 'else if (!why(q.k) && !recent) show(q.k, true);')
rep('setInterval(() => { try { if (!S || !S.adDue || !calm()) return;', 'setInterval(() => { try { if (!S || !S.adDue || !calm() || performance.now() - (window.__adLast || -1e9) < 45000) return;')
# Flugzeug: Position vor dem Einblenden setzen (kein Sprung im ersten Bild)
rep('requestAnimationFrame(step); try { window.__planeSnd && window.__planeSnd(ms, a[0] > 1 || a[0] < 0); } catch (e) {} }', 'step(t0); try { window.__planeSnd && window.__planeSnd(ms, a[0] > 1 || a[0] < 0); } catch (e) {} }')
rep('function flyPlane(a, b, ms) { plane.classList.add("on"); const t0 = performance.now(),', 'function flyPlane(a, b, ms) { const t0 = performance.now(),')
rep('if (t < 1) requestAnimationFrame(step); else plane.classList.remove("on"); };', 'plane.classList.add("on"); if (t < 1) requestAnimationFrame(step); else plane.classList.remove("on"); };')
open(dst, 'w', encoding='utf-8').write(s); print('ok2')
