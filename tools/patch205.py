"""V205: Shop-Banner – kürzere Untertitel (nichts abgeschnitten), Preis wird klarer Kauf-Knopf «BUY NOW · 99 GOLD»."""
import sys
src, dst = sys.argv[1], sys.argv[2]
s = open(src, encoding='utf-8').read()
def rep(a, b, cnt=1):
    global s
    n = s.count(a); assert n == cnt, (n, a[:70]); s = s.replace(a, b)
rep('const GAME_VER = "V204";', 'const GAME_VER = "V205";')
rep('"TRAIN WITH OLLIE", "Coach Ollie shows you the tricks"]', '"TRAIN WITH OLLIE", "Learn the boss tricks"]')
rep('"BEAT THE BOSS", "10 practice duels · zero risk"]', '"BEAT THE BOSS", "10 duels · no risk"]')
rep('"WIN MORE GOLD", "Tips after every round"]', '"WIN MORE GOLD", "Tips every round"]')
rep('<span class="p"><b>99</b><i>GOLD</i></span>`; }', '<span class="p cta"><em>BUY NOW</em><b>99</b><i>GOLD</i></span>`; }')
css = '''<style id="v205">
.coachAd .ad.ad3 .txt{right:104px!important}
.coachAd .ad.ad3 .p.cta{right:8px!important;min-width:84px!important;padding:5px 8px 6px!important;border-radius:14px!important;background:linear-gradient(#ffb04a,#ee6a1c)!important;color:#fff!important;border:2px solid #3a2414!important;box-shadow:0 3px 0 #3a2414!important;animation:ctaPulse 1.6s ease-in-out infinite!important}
.coachAd .ad.ad3 .p.cta em{display:block;font:800 10px/1 "Baloo 2",sans-serif;letter-spacing:.08em;font-style:normal;color:#fff;margin-bottom:2px}
.coachAd .ad.ad3 .p.cta b{color:#fff!important;font-size:24px!important;text-shadow:0 2px 0 rgba(58,36,20,.5)}
.coachAd .ad.ad3 .p.cta i{color:#fff!important;font-size:10px!important}
.coachAd.poor .ad.ad3 .p.cta{background:linear-gradient(#d9cbb4,#b8a483)!important;animation:none!important;filter:none!important}
@keyframes ctaPulse{0%,100%{transform:translateY(-50%) scale(1)}50%{transform:translateY(-50%) scale(1.06)}}
@media (prefers-reduced-motion:reduce){.coachAd .ad.ad3 .p.cta{animation:none!important}}
</style>
'''
i = s.rfind('</body>'); s = s[:i] + css + s[i:]
open(dst, 'w', encoding='utf-8').write(s); print('ok')
