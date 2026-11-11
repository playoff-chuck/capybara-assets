#!/usr/bin/env python3
# V635 (Martin 11.11. 16:06): Einsatz-Screen des Boss-Hacks (ab dem 2. Hack) im violetten Design der Boss-Werbung;
# nur drei Einsätze: 25 % · 50 % · 100 % des Goldes (kein Schieber), Standard 25 %, gewählter Knopf leuchtet.
import sys, os
site = sys.argv[1]; p = os.path.join(site, "index.html"); s = open(p, encoding="utf-8").read()
def rep(a, b, n=1):
    global s
    c = s.count(a); assert c == n, (c, a[:90]); s = s.replace(a, b)
rep('const GAME_VER = "V634";', 'const GAME_VER = "V635";')
rep('<div class="hkChips"><button data-p="0.1">10 %</button><button data-p="0.25">25 %</button><button data-p="0.5">50 %</button><button data-p="1">ALL IN</button></div>',
    '<div class="hkChips"><button data-p="0.25">25 %</button><button data-p="0.5">50 %</button><button data-p="1">100 %</button></div>')
CSS = '''
/* V635: Einsatz-Screen violett wie die Boss-Werbung */
#hackBet.hackBet{background:#fff7ee!important;border:3px solid #17150c!important;box-shadow:0 14px 0 rgba(0,0,0,.35)!important}
#hackBet .hkBetPic{border-bottom:3px solid #17150c!important}
#hackBet .alTag,#hackBet .hackTag{background:linear-gradient(180deg,#d6409f,#7a1f60)!important;color:#fff!important;border:2.5px solid #17150c!important;border-radius:10px!important;font-family:Bangers,var(--f-display),sans-serif!important;letter-spacing:1px}
#hackBet h2{color:#d6409f!important;-webkit-text-stroke:1.4px #17150c;font-family:Bangers,var(--f-display),sans-serif!important;letter-spacing:1px}
#hackBet p{color:#3a2a1a!important}
#hackBet .hkStake small{color:#b0328c!important;letter-spacing:.14em}
#hackBet .hkStake b{color:#d6409f!important;-webkit-text-stroke:1px #17150c}
#hackBet #hkRange{display:none!important}
#hackBet .hkChips{gap:8px}
#hackBet .hkChips button{background:#fff!important;color:#b0328c!important;border:2.5px solid #d6409f!important;border-radius:12px!important;font:400 22px/1 Bangers,system-ui!important;letter-spacing:1px;box-shadow:0 3px 0 #7a1f60!important}
#hackBet .hkChips button.on{background:linear-gradient(180deg,#e04aa8,#8a2470)!important;color:#fff!important;border-color:#17150c!important;text-shadow:0 2px 0 #4d1240}
#hackBet #hkGo{font-family:Bangers,system-ui!important;font-size:26px!important;letter-spacing:1px;color:#fff!important;background:linear-gradient(180deg,#e04aa8,#8a2470)!important;border:3px solid #17150c!important;text-shadow:0 2px 0 #4d1240;box-shadow:0 4px 0 #4d1240!important}
#hackBet #hkSkip{color:#7a6a55!important;background:transparent!important;border:2px solid #e2d3bc!important;box-shadow:none!important}
'''
assert '</style>' in s; s = s.replace('</style>', CSS + '</style>', 1)
rep('function hkStakeUI() { const v = +$("hkRange").value || 0;',
    'function hkStakeUI() { const v = +$("hkRange").value || 0; try { const mx = +$("hkRange").max || 0; document.querySelectorAll("#hackBet .hkChips button").forEach(b => b.classList.toggle("on", mx > 0 && v === Math.round(mx * +b.dataset.p / 10) * 10)); } catch (e) {}')
open(p, "w", encoding="utf-8").write(s)
print("ok V635")
