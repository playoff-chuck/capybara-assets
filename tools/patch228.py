"""V228: Offline-Knopf zeigt statt «OFFLINE» ein rosa Comic-Flugzeug (fertig gespeichert: grüner Haken-Punkt)."""
import sys
src, dst = sys.argv[1], sys.argv[2]
s = open(src, encoding='utf-8').read()
def rep(a, b, cnt=1):
    global s
    n = s.count(a); assert n == cnt, (n, a[:70]); s = s.replace(a, b)
rep('const GAME_VER = "V227";', 'const GAME_VER = "V228";')
PLANE = ('<svg class="pl" viewBox="-1 -1 26 26" width="40" height="40" aria-hidden="true"><g transform="rotate(45 12 12)">'
  '<path d="M21 16v-2l-8-5V3.5c0-.83-.67-1.5-1.5-1.5S10 2.67 10 3.5V9l-8 5v2l8-2.5V19l-2 1.5V22l3.5-1 3.5 1v-1.5L13 19v-5.5l8 2.5z" transform="translate(.5 0)" fill="#ff6fb5" stroke="#3a2414" stroke-width="1.35" stroke-linejoin="round"/>'
  '<path d="M11.3 4v4.2" stroke="#fff" stroke-width="1.1" stroke-linecap="round" opacity=".9"/></g></svg>')
a = s.index("const draw = (pct) => { b.classList.toggle(\"ok\", state === \"ready\"); b.innerHTML = ")
e = s.index("; };", a) + 4
s = s[:a] + ("const PLANE = '" + PLANE + "';\n    const draw = (pct) => { b.classList.toggle(\"ok\", state === \"ready\"); b.innerHTML = state === \"busy\" ? `<b>${pct || 0}%</b>` + PLANE.replace('class=\"pl\"', 'class=\"pl fly\"') : PLANE + (state === \"ready\" ? '<i class=\"okDot\"></i>' : ''); };") + s[e:]
css = '''<style id="v228">
#btnOffline{position:fixed!important}
#btnOffline,#btnMap{border-radius:50%!important}
#btnMap svg{width:32px!important;height:32px!important}
#btnOffline .pl{width:36px!important;height:36px!important;max-width:none!important;display:block;filter:drop-shadow(0 2px 0 rgba(58,36,20,.35))}
#btnOffline .pl.fly{position:absolute;inset:0;margin:auto;opacity:.28;animation:plFly 1.2s ease-in-out infinite alternate}
@keyframes plFly{to{transform:translate(3px,-3px) rotate(-4deg)}}
#btnOffline b{position:relative;z-index:1;font:800 15px/1 "Baloo 2",sans-serif;color:#d94c8c}
#btnOffline .okDot{position:absolute;right:3px;bottom:3px;width:17px;height:17px;border-radius:50%;background:#5cbf4a;border:2px solid #3a2414;box-sizing:border-box}
#btnOffline .okDot::after{content:"";position:absolute;left:3.5px;top:1.5px;width:4px;height:7px;border:solid #fff;border-width:0 2px 2px 0;transform:rotate(40deg)}
#btnOffline small{display:none!important}
</style>
'''
i = s.rfind('</body>'); s = s[:i] + css + s[i:]
open(dst, 'w', encoding='utf-8').write(s); print('ok')
