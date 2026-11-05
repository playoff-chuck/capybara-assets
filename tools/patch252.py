"""V252: Einarmiger Bandit neu gestaltet (Martin 05.11. 10:39): Automat als Nano-Banana-Pro-Bild (img/bandit_cab.webp,
Capybara mit Barett obenauf, Camo-Bänder, Goldrand mit Lämpchen, rosa Hebel). Die drei Walzen laufen genau in den drei weißen
Fenstern des Bildes; Tipp auf den Hebel oder SPIN startet. Beim Ziehen ruckt der Automat, beim Jackpot leuchten die Fenster gold.
Feste Größen (Seitenverhältnis des Bildes), nichts verschiebt sich."""
import sys
src, dst = sys.argv[1], sys.argv[2]
s = open(src, encoding='utf-8').read()
def rep(a, b, cnt=1):
    global s
    n = s.count(a); assert n == cnt, (n, a[:70]); s = s.replace(a, b)
rep('const GAME_VER = "V251";', 'const GAME_VER = "V252";')
# Fenster im Bild (800×1066, gemessen): links/oben/Breite/Höhe in %
WIN = [(12.25, 37.7, 13.4, 22.5), (31.75, 38.1, 13.6, 22.9), (51.8, 38.5, 14.0, 23.1)]
reels = "".join(f'<div class="bdReel" id="bdR{i}" style="left:{l}%;top:{t}%;width:{w}%;height:{h}%"><div class="bdStrip" id="bdS{i}"></div></div>' for i, (l, t, w, h) in enumerate(WIN))
rep('''<div class="bdMach"><div class="bdWin">${[0, 1, 2].map(i => `<div class="bdReel" id="bdR${i}"><div class="bdStrip" id="bdS${i}"></div></div>`).join("")}</div><div class="bdLights">${"<i></i>".repeat(12)}</div>
        <div class="bdLever" id="bdLever" aria-label="Pull"><u></u><b></b><i></i></div></div>''',
    f'''<div class="bdCab" id="bdCab"><img class="bdCabImg" src="img/bandit_cab.webp" alt="" draggable="false">{reels}<div class="bdFlash"></div><button class="bdLever" id="bdLever" aria-label="Pull the lever"></button></div>''')
rep('const $b = id => document.getElementById(id), H = 96, LEN = 30;', 'const $b = id => document.getElementById(id), LEN = 30; const rh = i => Math.max(40, $b("bdR" + i).clientHeight || 96);')
rep('s.style.transition = `transform ${stops[i]}ms cubic-bezier(.12,.62,.18,1)`; s.style.transform = `translateY(${-(LEN - 1) * H}px)`;',
    's.style.setProperty("--rh", rh(i) + "px"); s.style.transition = `transform ${stops[i]}ms cubic-bezier(.12,.62,.18,1)`; s.style.transform = `translateY(${-(LEN - 1) * rh(i)}px)`;')
rep('const lv = $b("bdLever"); lv.classList.add("pull"); setTimeout(() => lv.classList.remove("pull"), 420);',
    'const cab = $b("bdCab"); cab.classList.remove("kick"); void cab.offsetWidth; cab.classList.add("kick");')
rep('ov.hidden = false; requestAnimationFrame(() => ov.classList.add("on"));',
    'ov.hidden = false; [0, 1, 2].forEach(i => $b("bdS" + i).style.setProperty("--rh", rh(i) + "px")); requestAnimationFrame(() => ov.classList.add("on"));')
css = r'''
<style id="v252bandit">
#ovBandit .bdBox{width:min(360px,100%);padding:12px 12px 14px}
#ovBandit .bdBox h2{margin:4px 0 0}
#ovBandit .bdSub{margin-bottom:4px}
.bdCab{position:relative;width:min(100%,calc((100vh - 270px) * .751));aspect-ratio:600/799;margin:0 auto;user-select:none;-webkit-user-select:none}
.bdCabImg{position:absolute;inset:0;width:100%;height:100%;pointer-events:none;filter:drop-shadow(0 8px 10px rgba(58,42,26,.28))}
.bdCab.kick{animation:bdKick .42s cubic-bezier(.3,1.6,.5,1)}
@keyframes bdKick{0%{transform:none}25%{transform:translateY(6px) rotate(-1.2deg)}55%{transform:translateY(-3px) rotate(.8deg)}100%{transform:none}}
#ovBandit .bdCab .bdReel{position:absolute;border:0;border-radius:9px/12px;background:#fff;overflow:hidden;box-shadow:inset 0 0 0 1px rgba(58,42,26,.08)}
#ovBandit .bdCab .bdReel:after{border-radius:inherit;background:linear-gradient(180deg,rgba(58,42,26,.32),rgba(58,42,26,0) 30%,rgba(58,42,26,0) 70%,rgba(58,42,26,.32))}
#ovBandit .bdCab .bdStrip div{height:var(--rh,96px)}
#ovBandit .bdCab .bdStrip img{width:88%;height:auto;max-height:80%;aspect-ratio:1}
#ovBandit .bdCab .bdReel.hit{box-shadow:0 0 0 3px #f6c945,0 0 16px 4px #ffe79a,inset 0 0 0 1px rgba(58,42,26,.08)}
.bdFlash{position:absolute;inset:3% 4%;border-radius:22px;pointer-events:none;opacity:0;background:radial-gradient(60% 40% at 45% 48%,rgba(255,231,154,.75),rgba(255,231,154,0) 70%)}
#ovBandit.spin .bdFlash{animation:bdFl .5s ease-in-out infinite alternate}
#ovBandit.win .bdFlash{animation:bdFl .16s steps(2) infinite}
@keyframes bdFl{from{opacity:0}to{opacity:.85}}
.bdCab .bdLever{position:absolute;left:79%;top:30%;width:21%;height:42%;border:0!important;background:transparent!important;box-shadow:none!important;padding:0!important;min-height:0!important;cursor:pointer;border-radius:30px!important}
.bdCab .bdLever:focus-visible{outline:3px solid #4f86c9}
#ovBandit .bdRes{margin:6px 0 8px}
@media (prefers-reduced-motion:reduce){.bdCab.kick,#ovBandit.spin .bdFlash,#ovBandit.win .bdFlash{animation:none}}
</style>
'''
i = s.rfind('</body>'); s = s[:i] + css + s[i:]
open(dst, 'w', encoding='utf-8').write(s); print('ok')
