"""V256: Werbeanzeigen (Martin 05.11. 13:32):
- Alle drei Anzeigen der ersten 10 Wellen im Marketplace-Stil (Kanone, Ten-ton, Betonmischer; neue Nano-Banana-Pro-Bilder
  img/ad_ton_sale.webp, img/ad_mix_sale.webp), Rabatt-Sticker je Bild passend gesetzt.
- «SALE» als professionelles Eckband (rot mit goldenen Kanten, schräg) statt Blink-Etikett.
- Kanone und Mischer kommen erst, wenn man sie wirklich nutzen kann: Kanone sobald ein Turm mit freiem Platz da ist und 70 Gold,
  Mischer sobald 350 Gold da sind – an einer ruhigen Stelle (kein anderes Fenster, kein Tutorial, keine Karte). Bis dahin
  erscheint zur Freischaltwelle nichts. Ten-ton: das Geschenk (erster gratis) kommt wie bisher in Welle 5; die Sale-Anzeige
  «BUY ANOTHER» erst, wenn 600 Gold da sind (einmal). Vorgemerkte Anzeigen stehen im Spielstand (adDue)."""
import sys
src, dst = sys.argv[1], sys.argv[2]
s = open(src, encoding='utf-8').read()
def rep(a, b, cnt=1):
    global s
    n = s.count(a); assert n == cnt, (n, a[:70]); s = s.replace(a, b)
rep('const GAME_VER = "V255";', 'const GAME_VER = "V256";')
rep('''    const AD = { kan: { img: "img/ad_kan.webp", tag: "NEW GEAR", line: "Big splash damage. Cracks the tough guys." },
                 ton: { img: "img/ad_ton.webp", tag: "FREE GIFT", line: "Your first one is free – it's already in your Pocket!" },
                 mix: { img: "img/ad_mix.webp", tag: "NEW GEAR", line: "Fills a hole to the top and buries monsters." } };''',
'''    const AD = { kan: { img: "img/ad_kan.webp", sale: "img/ad_kan_sale.webp", st: [[79, 17], [11, 36], [16.5, 71]], tag: "NEW GEAR", line: "Big splash damage. Cracks the tough guys." },
                 ton: { img: "img/ad_ton.webp", sale: "img/ad_ton_sale.webp", st: [[73, 16], [10, 78], [11, 51]], tag: "FREE GIFT", line: "Your first one is free – it's already in your Pocket!", sline: "Crush them all again – grab a second one!" },
                 mix: { img: "img/ad_mix.webp", sale: "img/ad_mix_sale.webp", st: [[8.6, 43], [90, 39], [8.6, 78]], tag: "NEW GEAR", line: "Fills a hole to the top and buries monsters." } };
    let saleMode = false;''')
rep('function show(k) { cur = k; const a = AD[k], d = INTRO_GEAR[k];', 'function show(k, sale) { cur = k; saleMode = !!sale; const a = AD[k], d = INTRO_GEAR[k];')
rep('{ const card = $a("adCard"), sale = k === "kan"; card.classList.toggle("sale", sale); const old = $a("saleOld");',
    '{ const card = $a("adCard"); card.classList.toggle("sale", sale); [1, 2, 3].forEach(n => { const el = card.querySelector(".saleSt.s" + n); if (el && a.st) { el.style.left = a.st[n - 1][0] + "%"; el.style.top = a.st[n - 1][1] + "%"; } });')
rep('$a("adPic").style.backgroundImage = `url(${k === "kan" ? "img/ad_kan_sale.webp" : a.img})`; $a("adTag").textContent = k === "kan" ? "SALE" : a.tag;',
    '$a("adPic").style.backgroundImage = `url(${sale ? a.sale : a.img})`; $a("adTag").textContent = sale ? "SALE" : a.tag;')
rep('$a("adName").textContent = d[0].toUpperCase(); $a("adLine").textContent = a.line;', '$a("adName").textContent = d[0].toUpperCase(); $a("adLine").textContent = sale && a.sline ? a.sline : a.line;')
rep('function close(bought) { ov.classList.remove("on"); ov.hidden = true; const k = cur; cur = null; try { closeIntro(); } catch (e) {}',
    'function close(bought) { ov.classList.remove("on"); ov.hidden = true; const k = cur; cur = null; if (late) { late = false; S.intro = false; S.adOpen = false; } else try { closeIntro(); } catch (e) {}')
rep('''    showIntro = function (q) { const r = _si.apply(this, arguments); try { if (q && q.t === "gear" && AD[q.k] && (S.wave || 0) <= 10 && !S.nuts) show(q.k); } catch (e) { console.error("ad", e); } return r; };''',
'''    let late = false;
    try { if (typeof SAVE_KEYS !== "undefined" && !SAVE_KEYS.includes("adDue")) SAVE_KEYS.push("adDue"); } catch (e) {}
    showIntro = function (q) { const r = _si.apply(this, arguments);
      try { if (q && q.t === "gear" && AD[q.k] && (S.wave || 0) <= 10 && !S.nuts) {
          S.adDue = S.adDue || {};
          if (q.k === "ton") { show("ton", false); S.adDue.ton = 1; }                       // Geschenk sofort, Sale später (600 Gold)
          else if (!why(q.k)) show(q.k, true);                                              // sofort nutzbar → gleich als Sale
          else { S.adDue[q.k] = 1; $("ovIntro").hidden = true; try { closeIntro(); } catch (e) {} }   // sonst später, wenn nutzbar
        } } catch (e) { console.error("ad", e); } return r; };
    const calm = () => S && S.started && !S.over && !S.nuts && !S.testRun0 && !S.intro && !S.drop && !S.alert && !S.ordersOpen && !S.duel && !S.mapShow && !S.mapFly && !S.signOpen && !S.joinOpen
      && !S.mode && !S.sel && !S.shop && !S.paused && !S.mix && !S.banditOpen && !(typeof TUT !== "undefined" && TUT.on) && !(typeof hkOfferOn === "function" && hkOfferOn()) && (typeof inPlay !== "function" || inPlay()) && !document.hidden && ov.hidden;
    setInterval(() => { try { if (!S || !S.adDue || !calm()) return; for (const k of ["kan", "mix", "ton"]) if (S.adDue[k] && !why(k)) { delete S.adDue[k]; late = true; S.intro = true; S.adOpen = true; show(k, true); break; } } catch (e) {} }, 700);''')
css = r'''
<style id="v256sale">
.adCard.sale .adPic{overflow:hidden}
.adCard.sale .adTag{left:-38px!important;top:18px!important;width:150px;box-sizing:border-box;text-align:center;transform:rotate(-38deg);background:linear-gradient(180deg,#ff5a44,#c8161b)!important;color:#fff!important;border:0!important;border-top:2.5px solid #ffd23a!important;border-bottom:2.5px solid #ffd23a!important;border-radius:0!important;font:400 19px/1 Bangers,system-ui!important;letter-spacing:3px!important;padding:5px 0 4px!important;box-shadow:0 4px 8px rgba(0,0,0,.35);text-shadow:0 2px 0 #7a1010;animation:none!important;z-index:3}
.adCard.sale .adWave{background:#3a2a1a;color:#ffd23a;border-color:#ffd23a}
</style>
'''
i = s.rfind('</body>'); s = s[:i] + css + s[i:]
open(dst, 'w', encoding='utf-8').write(s); print('ok')
