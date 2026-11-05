"""V259: Flugzeug auf der Weltkarte ist jetzt ein rosa Doppeldecker (Nano Banana Pro, img/biplane.webp) in Seitenansicht –
passend zum Propeller-Geräusch und zum Ankunftsbild. Er schaut immer in Flugrichtung (gespiegelt, wenn er nach rechts fliegt),
neigt sich leicht mit der Steigung (max. ±25°) und schaukelt sanft."""
import sys
src, dst = sys.argv[1], sys.argv[2]
s = open(src, encoding='utf-8').read()
def rep(a, b, cnt=1):
    global s
    n = s.count(a); assert n == cnt, (n, a[:70]); s = s.replace(a, b)
rep('const GAME_VER = "V258";', 'const GAME_VER = "V259";')
rep('<div class="mapPlane"><svg viewBox="0 0 24 24" width="46" height="46" aria-hidden="true"><path d="M21 16v-2l-8-5V3.5c0-.83-.67-1.5-1.5-1.5S10 2.67 10 3.5V9l-8 5v2l8-2.5V19l-2 1.5V22l3.5-1 3.5 1v-1.5L13 19v-5.5l8 2.5z" fill="#ff6fb5" stroke="#3a2414" stroke-width="1.3" stroke-linejoin="round"/><path d="M11.5 4v4.2" stroke="#fff" stroke-width="1.1" stroke-linecap="round" opacity=".9"/></svg></div>',
    '<div class="mapPlane"><img class="biPlane" src="img/biplane.webp" alt=""></div>')
rep('plane.style.setProperty("--a", (ang - Math.cos(Math.PI * e) * 18) + "deg");',
    '{ const dx = b[0] - a[0], dy = (b[1] - a[1]) * MAP_AR - Math.cos(Math.PI * e) * 0.12 * Math.PI * MAP_AR, right = dx >= 0, tilt = Math.max(-25, Math.min(25, Math.atan2(dy, Math.abs(dx) + 1e-6) * 180 / Math.PI));\n          plane.style.setProperty("--a", (right ? tilt : -tilt) + "deg"); plane.style.setProperty("--fx", right ? -1 : 1); }')
css = r'''
<style id="v259plane">
#ovMap .mapPlane{left:0!important;top:0!important;transform:translate3d(var(--px,0),var(--py,0),0) translate(-50%,-50%) scale(var(--ik,1)) rotate(var(--a,0deg))!important;will-change:transform}
#ovMap .mapPlane img.biPlane{display:block;width:86px;height:auto;transform:scaleX(var(--fx,1));filter:drop-shadow(0 8px 5px rgba(0,0,0,.28));animation:biBob .9s ease-in-out infinite}
@keyframes biBob{0%,100%{translate:0 0}50%{translate:0 -3px}}
@media (prefers-reduced-motion:reduce){#ovMap .mapPlane img.biPlane{animation:none}}
</style>
'''
i = s.rfind('</body>'); s = s[:i] + css + s[i:]
open(dst, 'w', encoding='utf-8').write(s); print('ok')
