#!/usr/bin/env python3
# V561: Laden – Ledger-Blase überdeckte den Trainings-Banner (Martin 10.11. 16:36). Blasenzeile wächst jetzt mit dem Text,
# Banner rutscht darunter. RU: kürzere Banner-Texte, Münze statt «ЗОЛОТО», CTA «КУПИТЬ».
import sys
src, dst = sys.argv[1], sys.argv[2]
s = open(src, encoding="utf-8").read()
def rep(a, b, n=1):
    global s
    c = s.count(a); assert c == n, (c, a[:80]); s = s.replace(a, b)
rep('const GAME_VER = "V560";', 'const GAME_VER = "V561";')
rep('#ovMap{position:fixed;inset:0;z-index:990;', '''#sheet #sheetIn .ledgerTop{flex-shrink:0!important;height:auto!important;max-height:none!important;min-height:0!important;margin-bottom:12px!important;align-items:flex-start!important}
html[lang=ru] .coachAd .k{letter-spacing:.06em!important;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
html[lang=ru] .coachAd .h{font-size:clamp(18px,5.4vw,23px)!important;white-space:nowrap}
html[lang=ru] .coachAd .s{white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
html[lang=ru] .coachAd .ad3 .p.cta{min-width:0!important;width:auto!important;padding:5px 9px 6px!important;display:grid!important;grid-template-columns:auto auto;align-items:center;justify-items:center;column-gap:3px}
html[lang=ru] .coachAd .ad3 .p.cta em{grid-column:1 / -1;font-size:0!important;margin-bottom:1px!important}
html[lang=ru] .coachAd .ad3 .p.cta em::after{content:"КУПИТЬ";font-size:11px;letter-spacing:.06em}
html[lang=ru] .coachAd .ad3 .p.cta b{font-size:26px!important}
html[lang=ru] .coachAd .ad3 .p.cta i{font-size:0!important;line-height:0!important}
html[lang=ru] .coachAd .ad3 .p.cta i::after{content:"";display:block;width:20px;height:20px;background:url(img/coin64.webp) center/contain no-repeat}
html[lang=ru] .coachAd .ad3 .ad, html[lang=ru] .coachAd .ad3{padding-right:96px!important}
#ovMap{position:fixed;inset:0;z-index:990;''')
open(dst, "w", encoding="utf-8").write(s)
print("ok")
