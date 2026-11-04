"""V238: Held-Kreis und Flugzeug zittern nicht mehr beim Fliegen. Ursache: Position per left/top in % wurde auf
ganze Pixel gerundet und danach mit dem Karten-Zoom (×2–4) vergrößert → sichtbare Sprünge, dazu ein schnelles
Kipp-Wackeln (±8°, 0,45 s). Jetzt: Position per transform (Subpixel, GPU), sanftes Schweben ohne Kippen."""
import sys
src, dst = sys.argv[1], sys.argv[2]
s = open(src, encoding='utf-8').read()
def rep(a, b, cnt=1):
    global s
    n = s.count(a); assert n == cnt, (n, a[:70]); s = s.replace(a, b)
rep('const GAME_VER = "V237";', 'const GAME_VER = "V238";')
P = lambda el, x, y: f'{el}.style.setProperty("--px", ({x}) * BW + "px"); {el}.style.setProperty("--py", ({y}) * BW * MAP_AR + "px");'
rep('me.style.left = pt[0] * 100 + "%"; me.style.top = pt[1] * 100 + "%";', P('me', 'pt[0]', 'pt[1]'))
rep('me.style.left = x * 100 + "%"; me.style.top = y * 100 + "%";', P('me', 'x', 'y'))
rep('plane.style.left = x * 100 + "%"; plane.style.top = y * 100 + "%";', P('plane', 'x', 'y'))
css = '''<style id="v238">
#ovMap .mapMe{left:0!important;top:0!important;transform:translate3d(var(--px,0),var(--py,0),0) scale(var(--ik,1))!important;transform-origin:0 0!important;will-change:transform}
#ovMap .mapPlane{left:0!important;top:0!important;transform:translate3d(var(--px,0),var(--py,0),0) translate(-50%,-50%) scale(var(--ik,1)) rotate(calc(var(--a,0deg) + 90deg))!important;will-change:transform}
#ovMap .mapMe.fly img,#ovMap .mapMe.hop img{animation:mFloat 1.1s ease-in-out infinite alternate!important}
@keyframes mFloat{from{transform:translateY(0)}to{transform:translateY(-5px)}}
</style>
'''
i = s.rfind('</body>'); s = s[:i] + css + s[i:]
open(dst, 'w', encoding='utf-8').write(s); print('ok')
