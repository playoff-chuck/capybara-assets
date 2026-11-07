#!/usr/bin/env python3
# V408 (t12 Nr. 9): Trophäenregal im Squad File – 5 Wahrzeichen (Jungle Temple, The Pyramid, Ice Palace, Bear Cave, Ice Fortress)
# als Ausschnitt der vorhandenen Boss-Hintergründe in Goldrahmen; freigeschaltet, sobald der Boss-Ort Sterne hat. Keine neuen Bilder (0 $).
import sys
src, dst = sys.argv[1], sys.argv[2]
s = open(src, encoding="utf-8").read()
def rep(a, b, n=1):
    global s
    assert s.count(a) == n, (s.count(a), a[:80])
    s = s.replace(a, b)
rep('const GAME_VER = "V407";', 'const GAME_VER = "V408";')
CSS = """.trGrid{display:grid;grid-template-columns:repeat(5,1fr);gap:5px}.trCup{text-align:center}.trCup i{display:block;aspect-ratio:1;border-radius:50%;border:3px solid #d9a93a;box-shadow:0 0 0 2px #7a4b12,0 3px 0 #7a4b12,inset 0 0 0 2px rgba(255,240,180,.5);background:#9ab 50% 10%/170% auto no-repeat}.trCup small{display:block;font:700 8.5px/1.1 var(--f-ui);letter-spacing:.02em;margin-top:4px;color:#3a2a14;text-transform:uppercase}.trCup.off i{filter:grayscale(1) brightness(.45);border-color:#8a8a80;box-shadow:0 0 0 2px #55554c,0 3px 0 #55554c}.trCup.off small{color:#7a7a70}
</style>"""
rep(".sqLv small{display:block;font-size:11px;opacity:.85}\n</style>", ".sqLv small{display:block;font-size:11px;opacity:.85}\n" + CSS)
JS = r'''
/* V408: Trophäenregal – Wahrzeichen aus den Boss-Hintergründen (t12 Nr. 9) */
const TROPHY = [["samerica", "Jungle Temple", "40% 5%"], ["africa", "The Pyramid", "36% 7%"], ["asia", "Ice Palace", "50% 2%"], ["namerica", "Bear Cave", "48% 9%"], ["antarctica", "Ice Fortress", "52% 5%"]];
function trophyHtml() { const st = starsAll(); let got = 0;
  const cups = TROPHY.map((t, i) => { const on = (+st[i * 6 + 5] || 0) > 0; if (on) got++;
    return `<div class="trCup ${on ? "" : "off"}"><i style="background-image:url(bg/pl_${t[0]}_5.webp);background-position:${t[2]}"></i><small>${on ? t[1] : "???"}</small></div>`; }).join("");
  return `<div class="albSec">TROPHIES<span>${got} / ${TROPHY.length}</span></div><div class="trGrid">${cups}</div>`; }
'''
rep('/* V395: ein Auszeichnungs-Icon – Pokal öffnet Medaillen, Reiter zu Hall of fame und Squad */', JS + '/* V395: ein Auszeichnungs-Icon – Pokal öffnet Medaillen, Reiter zu Hall of fame und Squad */')
rep('let h = sqHtml() + `<div class="albSec">CAREER</div>', 'let h = sqHtml() + trophyHtml() + `<div class="albSec">CAREER</div>')
open(dst, "w", encoding="utf-8").write(s)
print("ok")
