"""V219: Boss gewinnt den Hack → statt lila Platzhalter ein gezeichnetes Monster (je Kontinent passend), das triumphiert."""
import sys
src, dst = sys.argv[1], sys.argv[2]
s = open(src, encoding='utf-8').read()
def rep(a, b, cnt=1):
    global s
    n = s.count(a); assert n == cnt, (n, a[:70]); s = s.replace(a, b)
rep('const GAME_VER = "V218";', 'const GAME_VER = "V219";')
rep('} else $("hkArt").innerHTML = HK_ART_LOSE;',
    '} else { const w = S.wave || 1, k = w > 120 ? "bear" : w > 90 ? "bear" : w > 60 ? "tiger" : w > 30 ? "mummy" : w > 20 ? "kiefer" : "heavy", src = (typeof MON_SPR_SRC !== "undefined" && MON_SPR_SRC[k]) || "";\n    $("hkArt").innerHTML = src ? `<div class="hkWinMon"><img src="${src}" alt=""><span class="hkCoin">$</span></div>` : HK_ART_LOSE; }')
css = '''<style id="v219">
.hkWinMon{position:relative;width:150px;height:150px;margin:0 auto}
.hkWinMon img{width:100%;height:100%;object-fit:contain;filter:drop-shadow(0 4px 0 rgba(58,36,20,.45));animation:hkGloat 1s ease-in-out infinite;transform-origin:50% 90%}
.hkWinMon .hkCoin{position:absolute;right:6px;top:10px;width:34px;height:34px;border-radius:50%;background:linear-gradient(#ffe57a,#f2b51e);border:3px solid #3a2414;display:grid;place-items:center;font:800 18px/1 "Baloo 2",sans-serif;color:#3a2414;animation:hkCoinJ .8s ease-in-out infinite}
@keyframes hkGloat{0%,100%{transform:rotate(-4deg) scale(1)}50%{transform:rotate(4deg) scale(1.05)}}
@keyframes hkCoinJ{0%,100%{transform:translateY(0)}50%{transform:translateY(-8px)}}
@media (prefers-reduced-motion:reduce){.hkWinMon img,.hkWinMon .hkCoin{animation:none}}
</style>
'''
i = s.rfind('</body>'); s = s[:i] + css + s[i:]
open(dst, 'w', encoding='utf-8').write(s); print('ok')
