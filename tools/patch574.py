#!/usr/bin/env python3
# V574 (Martin 11.11. 00:11): Coach-Werbung kompakter und spannender, ohne Scrollen:
# Titel, ein Satz wozu, Olli groß auf dem Hintergrund, 2 Vorteile, großer Kaufen-Knopf, kleiner «Später».
import sys
src, dst = sys.argv[1], sys.argv[2]
s = open(src, encoding="utf-8").read()
def rep(a, b, n=1):
    global s
    c = s.count(a); assert c == n, (c, a[:90]); s = s.replace(a, b)
rep('const GAME_VER = "V573";', 'const GAME_VER = "V574";')
a = s.index("  ov.innerHTML = '<div class=\"caBg\"></div>"); b = s.index("  document.body.appendChild(ov);", a)
s = s[:a] + '''  ov.innerHTML = '<div class="caBg"></div><div class="caTop"><span class="caK">BOSS HACK · TRAINING</span><h2>COACH OLLIE</h2><p class="caSub">Bosses challenge you to a wire duel – train and take their stake!</p></div>'
    + '<div class="caMid"><img class="caOllie" alt=""></div>'
    + '<div class="caCard"><div class="caPros"><div><b>10</b><span>practice duels without risk</span></div><div><b>💡</b><span>a tip after every round</span></div></div>'
    + '<button type="button" class="caBuy" disabled><span class="caBuyT">BOOK FOR 99 GOLD</span></button><button type="button" class="caLater" disabled>LATER</button><div class="caLock"><i></i><span>3</span></div></div>';   /* V574: kompakt */
''' + s[b:]
CSS = '''<style id="v574">
#ovCoachAd .caTop{padding-top:max(18px,env(safe-area-inset-top))!important}
#ovCoachAd h2{margin:8px 0 4px!important;font-size:clamp(38px,12vw,54px)!important}
#ovCoachAd .caSub{max-width:330px;margin:0 auto!important;font-size:15px!important;line-height:1.25!important}
#ovCoachAd .caMid{position:relative;flex:1 1 auto;min-height:0;display:flex;align-items:flex-end;justify-content:center;padding-top:6px}
#ovCoachAd .caMid .caOllie{position:static!important;width:auto!important;height:auto!important;max-height:100%;max-width:62vw;object-fit:contain;filter:drop-shadow(0 8px 10px rgba(0,0,0,.55));margin-bottom:-26px;animation:caBob 2.4s ease-in-out infinite}
@keyframes caBob{0%,100%{transform:translateY(0)}50%{transform:translateY(-6px)}}
#ovCoachAd .caCard{padding:30px 14px 12px!important;flex:0 0 auto}
#ovCoachAd .caPros{display:grid;grid-template-columns:1fr 1fr;gap:8px;margin-bottom:12px}
#ovCoachAd .caPros>div{display:flex;align-items:center;gap:8px;background:#f3e3b8;border-radius:12px;padding:8px;font:800 13px/1.15 "Baloo 2",sans-serif}
#ovCoachAd .caPros b{flex:0 0 32px;height:32px;display:grid;place-items:center;border-radius:50%;background:#58cc02;color:#fff;font:400 18px/1 Bangers,sans-serif;border:2px solid #2f7d0a}
#ovCoachAd .caBuy{padding:16px 10px 14px!important;font-size:27px!important;animation:caPulse 1.4s ease-in-out infinite}
#ovCoachAd .caBuy:disabled{animation:none}
@keyframes caPulse{0%,100%{transform:scale(1)}50%{transform:scale(1.035)}}
#ovCoachAd .caLater{margin-top:6px!important;font-size:13px!important;padding:6px 10px!important;background:none!important;border:0!important;box-shadow:none!important}
#ovCoachAd .caLock{top:10px;bottom:auto!important;right:10px}
</style>
'''
rep("</body>", CSS + "</body>")
open(dst, "w", encoding="utf-8").write(s)
print("ok")
