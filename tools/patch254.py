"""V254: Kanonen-Anzeige (Welle 3) im lauten Marketplace-Stil (Martin 05.11. 13:27): Nano-Banana-Pro-Bild mit Explosions-
hintergrund und Rabatt-Stickern; durchgestrichener «Listenpreis» 40–400 % über unserem Preis (zufällig je Anzeige), dazu Rabatt in %
(z. B. −80 %), der Preis nach Rabatt ist immer der reguläre Preis (70 Gold). Große Schrift «MEGA DEAL», blinkende Sticker,
großer Knopf «I WANT IT! · 70 GOLD», kleiner Knopf «No thanks». Andere Anzeigen (Ten-ton, Mischer) unverändert."""
import sys
src, dst = sys.argv[1], sys.argv[2]
s = open(src, encoding='utf-8').read()
def rep(a, b, cnt=1):
    global s
    n = s.count(a); assert n == cnt, (n, a[:70]); s = s.replace(a, b)
rep('const GAME_VER = "V253";', 'const GAME_VER = "V254";')
rep('<div class="adCard"><div class="adPic" id="adPic">',
    '<div class="adCard" id="adCard"><div class="adPic" id="adPic"><span class="saleSt s1" id="saleS1"></span><span class="saleSt s2">HOT!</span><span class="saleSt s3">DEAL</span>')
rep('function paint() { const k = cur, w = why(k), act = $a("adAct");',
    'function paint() { const k = cur, w = why(k), act = $a("adAct"), sale = $a("adCard").classList.contains("sale");')
rep('act.innerHTML = w ? `<div class="adNote">${w}</div>` : `<button class="btn-accent" id="adBuy">${k === "ton" ? "BUY ANOTHER" : "BUY NOW"} · ${price(k)} GOLD ▶</button>`;',
    'act.innerHTML = w ? `<div class="adNote">${w}</div>` : `<button class="btn-accent" id="adBuy">${sale ? "I WANT IT!" : k === "ton" ? "BUY ANOTHER" : "BUY NOW"} · ${price(k)} GOLD ▶</button>`;')
rep('$a("adLater").textContent = w || k === "ton" ? "Got it" : "Later"; }',
    '$a("adLater").textContent = sale ? "No thanks" : w || k === "ton" ? "Got it" : "Later"; }')
rep('function show(k) { cur = k; const a = AD[k], d = INTRO_GEAR[k];',
    '''function show(k) { cur = k; const a = AD[k], d = INTRO_GEAR[k];
      { const card = $a("adCard"), sale = k === "kan"; card.classList.toggle("sale", sale); const old = $a("saleOld");
        if (sale) { const p = price(k), up = 0.4 + Math.random() * 3.6, was = Math.ceil(p * (1 + up) / 10) * 10, pct = Math.round((1 - p / was) * 100);
          $a("saleWas").textContent = `${was} GOLD`; $a("salePct").textContent = `−${pct}%`; $a("saleS1").textContent = `−${pct}%`; $a("saleNow").textContent = `${p} GOLD`; } }''')
rep('<div class="adBody"><h2 id="adName"></h2>',
    '<div class="adBody"><div class="saleHead"><b class="saleMega">MEGA DEAL</b><span class="saleOnly">ONLY THIS WAVE!</span></div><h2 id="adName"></h2><div class="salePrice"><s id="saleWas"></s><b id="saleNow"></b><i id="salePct"></i></div>')
css = r'''
<style id="v254sale">
.adCard .saleSt,.adCard .saleHead,.adCard .salePrice{display:none}
.adCard.sale .saleSt,.adCard.sale .saleHead{display:block}
.adCard.sale .salePrice{display:flex}
.adCard.sale{border-color:#3a2a1a;background:linear-gradient(180deg,#fff6e6,#ffe9c2)}
.adCard.sale .adPrice{display:none}
.adCard.sale .adTag{background:#e0262a;animation:saleBlink .5s steps(2) infinite}
@keyframes saleBlink{50%{background:#ffd23a;color:#3a2a1a}}
.saleSt{position:absolute;z-index:1;transform:translate(-50%,-50%) rotate(-12deg);font-family:Bangers,system-ui;letter-spacing:.5px;color:#fff;-webkit-text-stroke:1px #7a1010;text-shadow:0 2px 0 #7a1010;white-space:nowrap;animation:saleWob 1.1s ease-in-out infinite}
.saleSt.s1{left:79%;top:17%;font-size:26px}
.saleSt.s2{left:11%;top:36%;font-size:20px;color:#e0262a;-webkit-text-stroke:1px #7a4a10;text-shadow:0 2px 0 #fff6c8;transform:translate(-50%,-50%) rotate(10deg)}
.saleSt.s3{left:16.5%;top:71%;font-size:19px;transform:translate(-50%,-50%) rotate(-8deg)}
@keyframes saleWob{0%,100%{scale:1}50%{scale:1.14}}
.saleHead{margin:-4px 0 2px}
.saleMega{display:block;font-family:Bangers,system-ui;font-weight:400;font-size:20px;letter-spacing:2px;color:#e0262a;line-height:1}
.saleOnly{display:inline-block;margin-top:3px;background:#3a2a1a;color:#ffd23a;font:900 10.5px/1 system-ui;letter-spacing:1px;border-radius:6px;padding:4px 7px 3px}
.adCard.sale .adBody h2{font-size:38px;color:#ffd23a;-webkit-text-stroke:1.6px #3a2a1a;text-shadow:0 3px 0 #3a2a1a}
.salePrice{align-items:center;justify-content:center;gap:10px;margin:6px 0 2px}
.salePrice s{font:800 17px/1 system-ui;color:#8a7a66;text-decoration:none;position:relative;white-space:nowrap}
.salePrice s:after{content:"";position:absolute;left:-4px;right:-4px;top:50%;height:3px;background:#e0262a;transform:rotate(-8deg);border-radius:2px}
.salePrice b{font-family:Bangers,system-ui;font-weight:400;font-size:40px;line-height:1;letter-spacing:1px;color:#e0262a;-webkit-text-stroke:1.2px #3a2a1a;white-space:nowrap}
.salePrice i{font-style:normal;font:900 15px/1 system-ui;color:#fff;background:#e0262a;border:2.5px solid #3a2a1a;border-radius:10px;padding:6px 8px 5px;transform:rotate(6deg);animation:saleWob .9s ease-in-out infinite}
.adCard.sale .adBody p{margin:4px 0 8px;min-height:18px}
.adCard.sale .adMet{display:none}
.adCard.sale #adBuy{background:linear-gradient(180deg,#ffd23a,#ff8a1c 55%,#e0262a)!important;color:#3a2a1a!important;font-size:21px!important;border:3px solid #3a2a1a!important;box-shadow:0 5px 0 #3a2a1a!important;position:relative;overflow:hidden}
.adCard.sale #adBuy:after{content:"";position:absolute;top:0;bottom:0;width:40%;left:-60%;background:linear-gradient(100deg,transparent,rgba(255,255,255,.75),transparent);animation:saleShine 1.6s ease-in-out infinite}
@keyframes saleShine{0%{left:-60%}60%,100%{left:120%}}
@media (prefers-reduced-motion:reduce){.saleSt,.salePrice i,.adCard.sale .adTag,.adCard.sale #adBuy:after{animation:none}}
</style>
'''
s = s.replace('$a("adPic").style.backgroundImage = `url(${a.img})`;', '$a("adPic").style.backgroundImage = `url(${k === "kan" ? "img/ad_kan_sale.webp" : a.img})`;', 1)
rep('$a("adTag").textContent = a.tag;', '$a("adTag").textContent = k === "kan" ? "SALE" : a.tag;')
i = s.rfind('</body>'); s = s[:i] + css + s[i:]
open(dst, 'w', encoding='utf-8').write(s); print('ok')
