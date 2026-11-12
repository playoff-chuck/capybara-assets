# V691 (Martin 12.11. 21:42/21:43): Boss-Hack-Ergebniskarte professioneller – kein weisser Hintergrund mehr.
# Gemalte Saftbar (Nano Banana Pro, img/hk_bar.webp), Blue und Rosie stehen HINTER der Theke (Unterkoerper verdeckt),
# vor jedem ein Glas frisch gepresster Karottensaft (img/hk_juice.webp). Karte in dunklem Holz statt Creme.
# Coach Ollie bekommt dieselbe Bar. Niederlage: vorerst dunkle Karte mit Monster (eigenes Bild folgt).
import sys
src, dst = sys.argv[1], sys.argv[2]
s = open(src, encoding="utf8").read()
def rep(a, b, n=1):
    global s; c = s.count(a); assert c == n, (a[:70], c); s = s.replace(a, b)

CSS = r'''<style id="v691">
/* V691: Boss-Hack-Ergebnis – Saftbar, dunkle Holzkarte */
#ovHack #hackRes.hkNew{background:linear-gradient(180deg,#4a2c17 0%,#2e1b0e 55%,#22140a 100%)!important;border:3px solid #17150c!important;border-radius:20px!important;box-shadow:0 6px 0 #17150c,0 16px 34px rgba(0,0,0,.45),inset 0 1px 0 rgba(255,220,160,.18)!important;color:#fff3dc!important;padding:0 0 14px!important;gap:4px!important;width:min(360px,calc(100vw - 24px))!important;overflow-x:hidden!important}
#ovHack #hackRes.hkNew.lose{background:linear-gradient(180deg,#3d2236 0%,#28152a 55%,#1c0f1d 100%)!important}
#ovHack #hackRes.hkNew #hkArt.scn{width:100%!important;max-width:none!important;height:auto!important;min-height:0!important;max-height:none!important;aspect-ratio:1116/833;margin:0!important;position:relative;flex:none!important;border-bottom:3px solid #17150c;border-radius:17px 17px 0 0;overflow:hidden}
#hkArt .hkScn{position:absolute;inset:0;overflow:hidden}
#hkArt .hkScn img.bg,#hkArt .hkScn img.fg{position:absolute;inset:0;width:100%!important;height:100%!important;max-width:none!important;object-fit:cover;animation:none!important}
#hkArt .hkScn img.fg{clip-path:inset(66.8% 0 0 0);z-index:3}
#hkArt .hkScn .fig{position:absolute;bottom:11%;width:46%;transform:translateX(-50%);z-index:2}
#hkArt .hkScn .fig img{display:block;width:100%!important;height:auto!important;max-width:none!important;aspect-ratio:1;object-fit:contain;filter:drop-shadow(0 4px 6px rgba(40,20,5,.45));animation:hkSway 2.4s ease-in-out infinite!important;transform-origin:50% 90%}
#hkArt .hkScn .fig.r img{animation-delay:-1.2s!important}
#hkArt .hkScn .fig.flip img{transform:scaleX(-1);animation-name:hkSwayF!important}
#hkArt .hkScn .jc{position:absolute;bottom:29.5%;width:8.5%!important;height:auto!important;max-width:none!important;transform:translateX(-50%);z-index:4;filter:drop-shadow(0 3px 2px rgba(40,20,5,.5));animation:none!important}
#hkArt .hkScn .bub{position:absolute;top:3.5%;transform:translateX(-50%);z-index:5;background:#fff7e8;color:#3a2414;border:2.5px solid #3a2414;border-radius:12px;padding:3px 9px 4px;font:800 12.5px/1.15 var(--f-ui,"Baloo 2",sans-serif);max-width:47%;white-space:normal;text-wrap:balance;text-align:center;box-sizing:border-box;box-shadow:0 3px 0 #3a2414;opacity:0;animation:hkBub .45s cubic-bezier(.2,1.6,.4,1) .35s forwards}
#hkArt .hkScn .bub.r{animation-delay:1s}
#hkArt .hkScn .bub b{display:block;font:400 13px/1 var(--f-display,"Bangers",sans-serif);letter-spacing:.04em;color:#3f7fd6}
#hkArt .hkScn .bub b.rosie{color:#d94f93}
#hkArt .hkScn .bub::after{content:"";position:absolute;left:50%;bottom:-9px;width:12px;height:12px;background:#fff7e8;border-right:2.5px solid #3a2414;border-bottom:2.5px solid #3a2414;transform:translateX(-50%) rotate(45deg)}
#hkArt .hkScn .glow{position:absolute;left:50%;top:-30%;width:120%;height:90%;transform:translateX(-50%);background:radial-gradient(closest-side,rgba(255,214,120,.35),transparent);z-index:1;pointer-events:none}
@keyframes hkSway{0%,100%{transform:translateY(0) rotate(-1.5deg)}50%{transform:translateY(-5px) rotate(1.5deg)}}
@keyframes hkSwayF{0%,100%{transform:scaleX(-1) translateY(0) rotate(-1.5deg)}50%{transform:scaleX(-1) translateY(-5px) rotate(1.5deg)}}
@keyframes hkBub{from{opacity:0;transform:translateX(-50%) scale(.5)}to{opacity:1;transform:translateX(-50%) scale(1)}}
#ovHack #hackRes.hkNew h2{position:relative;z-index:6;margin:-58px 0 8px!important;font:400 clamp(34px,10.5vw,46px)/1 var(--f-display,"Bangers",sans-serif)!important;letter-spacing:.03em;color:#ffd84d!important;-webkit-text-stroke:2.5px #2a170a;paint-order:stroke fill;text-shadow:0 4px 0 #2a170a,0 0 22px rgba(255,190,60,.55)!important;white-space:nowrap!important}
#ovHack #hackRes.hkNew.lose h2{color:#ff9ad0!important;text-shadow:0 4px 0 #2a170a,0 0 22px rgba(255,90,170,.45)!important}
#ovHack #hackRes.hkNew #hkArt:not(.scn){margin-top:16px!important}
#ovHack #hackRes.hkNew #hkArt:not(.scn)+h2{margin-top:4px!important}
#ovHack #hackRes.hkNew .hkDevT{color:rgba(255,236,210,.55)!important}
#ovHack #hackRes.hkNew .hkScore{margin-top:2px}
#ovHack #hackRes.hkNew .hkScore span{font-size:46px;text-shadow:0 3px 0 #17150c}
#ovHack #hackRes.hkNew .hkScore .me{color:#7cc0ff!important}#ovHack #hackRes.hkNew .hkScore .me.rosie{color:#ff8fc8!important}
#ovHack #hackRes.hkNew .hkScore .bo{color:#9cdf5f!important}
#ovHack #hackRes.hkNew .hkScore i{color:#f6e3c0!important}
#ovHack #hackRes.hkNew .hkScoreL{color:#d9c29b!important;font-weight:700}
#ovHack #hackRes.hkNew .hkGold{background:rgba(0,0,0,.32)!important;border:2px solid rgba(255,209,102,.5)!important;border-radius:14px!important;box-shadow:inset 0 0 18px rgba(255,190,60,.12);margin:6px 14px 8px!important;padding:8px 18px!important}
#ovHack #hackRes.hkNew .hkGold b{color:#ffd166!important;text-shadow:0 3px 0 #17150c}
#ovHack #hackRes.hkNew.lose .hkGold{border-color:rgba(255,138,106,.45)!important}#ovHack #hackRes.hkNew.lose .hkGold b{color:#ff8a6a!important}
#ovHack #hackRes.hkNew .hkGold small{color:#f4e2c4!important}
#ovHack #hackRes.hkNew .hkRow{padding:0 14px;box-sizing:border-box}
#ovHack #hackRes.hkNew .hkConf{z-index:7}
body:has(#ovHack:not([hidden]) #hackRes:not([hidden])) #buddy,body:has(#ovHack:not([hidden]) #hackRes:not([hidden])) #buddy *{visibility:hidden!important}   /* keine Funk-Blase über der Karte */
@media (prefers-reduced-motion:reduce){#hkArt .hkScn .fig img{animation:none!important}#hkArt .hkScn .bub{animation:none;opacity:1}}
</style>
<style id="v592">'''
rep('<style id="v592">', CSS)

# Szene bauen (eine Hilfsfunktion fuer Sieg und Coach)
rep('function hkFinish() {', r'''function hkScene(figs) {   /* V691: Figuren hinter der Saftbar, je ein Glas Karottensaft davor */
  const f = figs.map((o, i) => `<div class="fig${o.flip ? " flip" : ""}${i ? " r" : ""}" style="left:${o.x}%"><img src="${o.src}" alt=""></div>`).join("");
  const j = figs.map(o => `<img class="jc" src="img/hk_juice.webp" alt="" style="left:${o.jx}%">`).join("");
  const b = figs.map((o, i) => o.say ? `<span class="bub${i ? " r" : ""}" style="left:${o.x}%"><b class="${o.k || ""}">${o.name}</b>${o.say}</span>` : "").join("");
  return `<div class="hkScn"><img class="bg" src="img/hk_bar.webp" alt=""><div class="glow"></div>${f}<img class="fg" src="img/hk_bar.webp" alt="">${j}${b}</div>`; }
function hkFinish() {''')
rep('''    $("hkArt").innerHTML = `<img src="${COACH_IMG()}" alt="" style="width:110px;height:110px;object-fit:contain">`;''',
    '''    res.classList.add("hkNew"); $("hkArt").classList.remove("proud"); $("hkArt").classList.add("scn"); $("hkArt").innerHTML = hkScene([{ x: 50, jx: 63, src: COACH_IMG(), name: "Ollie", k: "", say: "" }]);   /* V691 */''')
rep('''  $("hkArt").classList.toggle("proud", win);''', '''  $("hkArt").classList.remove("proud"); $("hkArt").classList.toggle("scn", win); res.classList.add("hkNew");   /* V691: Saftbar statt weisser Karte */
  try { $("hkScMe").classList.toggle("rosie", heroKey() === "rosie"); } catch (e) {}''')
rep('''    $("hkArt").innerHTML = `<div class="hkProud"><div class="hpCol"><span class="hp"><b class="nm ${h}">${hn}</b>${hl}</span><span class="hpImg"><img class="h" src="${HERO_IMG[h]}" alt="" style="width:100px!important;height:100px!important;max-width:100px!important;object-fit:contain;display:block"></span></div><div class="hpCol r"><span class="hp"><b class="nm ${b}">${bn}</b>${bl}</span><span class="hpImg flip"><img class="b" src="${HERO_IMG[b]}" alt="" style="width:100px!important;height:100px!important;max-width:100px!important;object-fit:contain;display:block"></span></div></div>`;''',
    '''    $("hkArt").innerHTML = hkScene([{ x: 26, jx: 39, src: HERO_IMG[h], name: hn, k: h, say: hl }, { x: 74, jx: 61, src: HERO_IMG[b], name: bn, k: b, say: bl, flip: true }]);''')
rep('const GAME_VER = "V690"', 'const GAME_VER = "V691"')
open(dst, "w", encoding="utf8").write(s); print("ok", len(s))
