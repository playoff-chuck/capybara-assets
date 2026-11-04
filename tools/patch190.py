s=open('v189.html',encoding='utf-8').read()
def rep(a,b,cnt=1):
    global s
    n=s.count(a); assert n==cnt,(n,a[:70]); s=s.replace(a,b)
rep('ver: "V189", wave: S.wave','ver: "V190", wave: S.wave')
# Shop zählt auch als Vollbild (Zz/General weg)
rep('const FULL = ["ovHack",','const FULL = ["sheet", "ovHack",')
# Neues, reißerisches Banner
old_start=s.find('  const ADS = {'); old_end=s.find('  let adSeq = 0;')
assert old_start>0 and old_end>old_start
duel='''<svg class="duel" viewBox="0 0 120 80" aria-hidden="true"><rect x="1" y="1" width="118" height="78" rx="8" fill="#14102b" stroke="#ffe14d" stroke-width="2"/>${[0,1,2,3,4,5].map(i => `<path d="M6 ${10 + i * 12}h34" stroke="#ff8a1f" stroke-width="3"/><path d="M80 ${10 + i * 12}h34" stroke="#b07cff" stroke-width="3"/><rect x="${44}" y="${5 + i * 12}" width="14" height="10" rx="2" fill="${i % 3 ? "#ff8a1f" : "#b07cff"}"/><rect x="${62}" y="${5 + i * 12}" width="14" height="10" rx="2" fill="${i % 2 ? "#ff8a1f" : "#b07cff"}"/>`).join("")}<circle cx="24" cy="22" r="4" fill="#fff"/><circle cx="96" cy="46" r="4" fill="#fff"/></svg>'''
new='''  const BOLT = '<svg class="bolt" viewBox="0 0 24 40" aria-hidden="true"><path d="M14 0 2 22h9l-4 18 15-26h-9l5-14z" fill="#ffe14d" stroke="#3a2414" stroke-width="2" stroke-linejoin="round"/></svg>';
  const HEAD = [["BOSS HACK", "COACHING!", "Coach Ollie zeigt dir die Tricks"], ["BOSS HACK", "BEAT THE BOSS!", "10 Übungs-Duelle · null Risiko"], ["BOSS HACK", "WIN MORE GOLD!", "Tipps nach jeder Runde"]];
  const ADS = { vA: () => adHtml(HEAD[0]), vB: () => adHtml(HEAD[1]), vC: () => adHtml(HEAD[2]) };
  function adHtml(h) { return `<span class="flash">${BOLT}${BOLT}</span><img class="ollie" src="${COACH_IMG()}" alt=""><span class="txt"><span class="k">⚡ Limited deal ⚡</span><span class="h">${h[0]}</span><span class="h2">${h[1]}</span><span class="s">${h[2]}</span></span>DUELSVG<span class="p"><b>99</b><i>GOLD</i></span><span class="tag">10 DUELS</span>`; }
'''.replace('DUELSVG',duel).replace('Coach Ollie zeigt dir die Tricks','Coach Ollie shows you the tricks').replace('10 Übungs-Duelle · null Risiko','10 practice duels · zero risk').replace('Tipps nach jeder Runde','Tips after every round')
s=s[:old_start]+new+s[old_end:]
rep('b.innerHTML = `<span class="ad">${ADS[v](n)}</span>','b.innerHTML = `<span class="ad ad2">${ADS[v](n)}</span>')
css='''<style id="v190">
/* V190: Boss-Hack-Werbung – rot-gelb, Blitze, Coach Ollie, Mini-Duell, höher (füllt die Lücke unter Ledger) */
#sheet .coachAd{margin:2px 0 16px!important}
#sheet .shopGrid,#sheet .shopTiles{overflow:visible!important}
.coachAd .ad.ad2{position:relative;display:block;min-height:150px;padding:12px 100px 12px 100px;border:4px solid #3a2414;border-radius:18px;overflow:visible;
  background:radial-gradient(120% 140% at 30% 20%,#ffdf3d 0,#ffb21f 30%,#ff5a1f 62%,#d8141c 100%);box-shadow:0 5px 0 #3a2414,0 0 0 3px #ffe14d inset;animation:adGlow 1.2s ease-in-out infinite}
.coachAd .ad.ad2::before{content:"";position:absolute;inset:0;border-radius:14px;background:repeating-conic-gradient(from 0deg at 30% 50%,rgba(255,255,255,.16) 0 8deg,transparent 8deg 22deg);pointer-events:none}
.coachAd .ad2 .flash{position:absolute;inset:0;pointer-events:none}
.coachAd .ad2 .bolt{position:absolute;width:26px;height:44px;filter:drop-shadow(0 2px 0 #3a2414)}
.coachAd .ad2 .bolt:first-child{left:86px;top:-14px;transform:rotate(-14deg);animation:adZap .9s steps(2) infinite}
.coachAd .ad2 .bolt:last-child{right:96px;bottom:-12px;transform:rotate(18deg);animation:adZap .9s steps(2) .45s infinite}
.coachAd .ad2 .ollie{position:absolute;left:-6px;bottom:-4px;width:112px;height:auto;max-height:150px;object-fit:contain;filter:drop-shadow(0 4px 0 rgba(58,36,20,.6));transform:rotate(-4deg)}
.coachAd .ad2 .txt{position:relative;display:flex;flex-direction:column;gap:1px;z-index:1}
.coachAd .ad2 .k{font:800 11px/1 "Baloo 2",sans-serif;letter-spacing:.14em;text-transform:uppercase;color:#fff;background:#d8141c;align-self:flex-start;padding:3px 8px;border-radius:4px;border:2px solid #3a2414;animation:adBlink .8s steps(2) infinite}
.coachAd .ad2 .h{font-family:"Bangers","Impact",sans-serif;font-size:clamp(26px,7.6vw,38px);line-height:.92;letter-spacing:.03em;color:#ffe14d;-webkit-text-stroke:2px #3a2414;paint-order:stroke fill;text-shadow:0 4px 0 #3a2414;margin-top:4px}
.coachAd .ad2 .h2{font-family:"Bangers","Impact",sans-serif;font-size:clamp(18px,5.2vw,24px);line-height:1;color:#fff;-webkit-text-stroke:1.4px #3a2414;paint-order:stroke fill;text-shadow:0 3px 0 #3a2414}
.coachAd .ad2 .s{font:800 12px/1.2 "Baloo 2",sans-serif;color:#3a2414;margin-top:3px}
.coachAd .ad2 .duel{position:absolute;right:10px;top:12px;width:100px;height:auto;transform:rotate(5deg);border-radius:8px;box-shadow:0 4px 0 #3a2414}
.coachAd .ad2 .p{position:absolute;right:-10px;bottom:-16px;width:84px;height:84px;display:grid;place-items:center;text-align:center;line-height:.85;background:#d8141c;color:#ffe14d;
  clip-path:polygon(50% 0,61% 18%,82% 10%,80% 31%,100% 38%,86% 54%,98% 74%,76% 76%,70% 98%,52% 85%,32% 100%,27% 78%,4% 76%,15% 56%,0 38%,20% 30%,18% 9%,39% 18%);animation:adPop 1s ease-in-out infinite;z-index:2}
.coachAd .ad2 .p b{display:block;font-family:"Bangers",sans-serif;font-size:32px;font-weight:400;-webkit-text-stroke:1px #3a2414;paint-order:stroke fill}
.coachAd .ad2 .p i{display:block;font:800 12px "Baloo 2",sans-serif;font-style:normal;color:#fff}
.coachAd .ad2 .tag{position:absolute;right:16px;top:-12px;font:800 11px/1 "Baloo 2",sans-serif;padding:4px 8px;border-radius:99px;background:#3a2414;color:#ffe14d;transform:rotate(4deg)}
@keyframes adGlow{0%,100%{box-shadow:0 5px 0 #3a2414,0 0 0 3px #ffe14d inset,0 0 0 0 rgba(255,90,31,0)}50%{box-shadow:0 5px 0 #3a2414,0 0 0 3px #fff inset,0 0 18px 6px rgba(255,90,31,.55)}}
@keyframes adZap{50%{opacity:.25}}
@media (max-width:370px){.coachAd .ad.ad2{padding-left:88px;padding-right:100px}.coachAd .ad2 .ollie{width:94px}.coachAd .ad2 .duel{width:86px}}
@media (prefers-reduced-motion:reduce){.coachAd .ad2,.coachAd .ad2 *{animation:none!important}}
</style>
'''
i=s.rfind('</body>'); s=s[:i]+css+s[i:]
open('v190.html','w',encoding='utf-8').write(s); print('ok')
