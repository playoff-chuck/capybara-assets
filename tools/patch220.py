"""V220: Betonmischer neu (Nano Banana Pro) – im Shop/Guide und als fahrender Mischer im Spiel."""
import sys
src, dst = sys.argv[1], sys.argv[2]
s = open(src, encoding='utf-8').read()
def rep(a, b, cnt=1):
    global s
    n = s.count(a); assert n == cnt, (n, a[:70]); s = s.replace(a, b)
rep('const GAME_VER = "V219";', 'const GAME_VER = "V220";')
rep('mix:"img/5be956d26c.webp"', 'mix:"img/mixer_icon.webp"')
css = '''<style id="v220">
#mixer{width:104px!important;height:81px!important;background:url(img/mixer_big.webp) center/contain no-repeat;filter:drop-shadow(0 3px 0 rgba(58,36,20,.45)) drop-shadow(0 6px 6px rgba(0,0,0,.3))!important;transform-origin:50% 90%;transition:transform .3s ease}
#mixer svg{display:none!important}
#mixer.flip{transform:scaleX(-1)}
#mixer.pour{transform:rotate(-6deg)}
#mixer.flip.pour{transform:scaleX(-1) rotate(-6deg)}
#mixer:not([hidden]){animation:mixBob .35s ease-in-out infinite alternate}
@keyframes mixBob{from{translate:0 0}to{translate:0 -2px}}
@media (prefers-reduced-motion:reduce){#mixer:not([hidden]){animation:none}}
</style>
'''
i = s.rfind('</body>'); s = s[:i] + css + s[i:]
pre = '<link rel="preload" as="image" href="img/mixer_big.webp">'
k = s.find('<title>'); s = s[:k] + pre + s[k:]
open(dst, 'w', encoding='utf-8').write(s); print('ok')
