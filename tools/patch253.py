"""V253: Neue Waffen der ersten 10 Wellen als Werbeanzeige statt Hinweisfenster (Martin 05.11. 10:39):
Kanone (W3), Ten-ton drop (W5, erster gratis), Betonmischer (W9). Anzeige mit Nano-Banana-Pro-Bild (img/ad_kan|ton|mix.webp),
Titel, ein Satz, Kennzahlen, großer Knopf «BUY NOW · <Preis>» – nur wenn genug Gold da ist (und bei der Kanone ein Turm mit
freiem Platz) –, sonst an derselben Stelle ein kurzer Hinweis; kleiner Knopf «Later» bzw. «Got it». Kauf passiert sofort:
Kanone auf den ersten Turm mit freiem Platz, Mischer/Ten-ton in die Pocket. Feste Größen, nichts verschiebt sich."""
import sys
src, dst = sys.argv[1], sys.argv[2]
s = open(src, encoding='utf-8').read()
def rep(a, b, cnt=1):
    global s
    n = s.count(a); assert n == cnt, (n, a[:70]); s = s.replace(a, b)
rep('const GAME_VER = "V252";', 'const GAME_VER = "V253";')
css = r'''
<style id="v253ads">
#ovAd{position:fixed;inset:0;z-index:958;display:flex;align-items:center;justify-content:center;padding:16px;background:rgba(40,28,16,.66)}
#ovAd[hidden]{display:none}
.adCard{position:relative;width:min(360px,100%);background:#fff6e6;border:3px solid #3a2a1a;border-radius:22px;overflow:hidden;box-shadow:0 14px 36px rgba(0,0,0,.5);color:#3a2a1a;text-align:center;transform:translateY(24px) scale(.92);opacity:0;transition:transform .38s cubic-bezier(.2,1.4,.4,1),opacity .2s}
#ovAd.on .adCard{transform:none;opacity:1}
.adPic{position:relative;width:100%;aspect-ratio:720/537;background:#e9dcc2 center/cover no-repeat;border-bottom:3px solid #3a2a1a}
.adPic:after{content:"";position:absolute;inset:0;background:linear-gradient(180deg,rgba(0,0,0,0) 60%,rgba(58,42,26,.35))}
.adTag{position:absolute;left:10px;top:10px;z-index:1;background:#e86fa3;color:#fff;font:900 11px/1 system-ui;letter-spacing:1px;border-radius:8px;padding:6px 9px 5px;border:2px solid #3a2a1a}
.adWave{position:absolute;right:10px;top:10px;z-index:1;background:#fff6e6;color:#3a2a1a;font:900 11px/1 system-ui;letter-spacing:.6px;border-radius:8px;padding:6px 8px 5px;border:2px solid #3a2a1a}
.adPrice{position:absolute;right:12px;bottom:-16px;z-index:2;background:#f6c945;color:#3a2a1a;font:900 15px/1 system-ui;border-radius:999px;padding:8px 13px 7px;border:3px solid #3a2a1a;box-shadow:0 3px 0 #3a2a1a;transform:rotate(-4deg);white-space:nowrap}
.adBody{padding:20px 16px 14px}
.adBody h2{font-family:Bangers,system-ui;font-weight:400;font-size:34px;letter-spacing:1px;line-height:1;margin:0;color:#ee7a2c;-webkit-text-stroke:1.2px #3a2a1a}
.adBody p{margin:6px 0 10px;font-weight:800;font-size:14px;line-height:1.3;min-height:36px}
.adMet{display:flex;justify-content:center;gap:6px;margin-bottom:12px;min-height:24px}
.adMet span{background:#efe2c8;border-radius:999px;padding:4px 9px;font:800 11.5px/1.2 system-ui;white-space:nowrap}
.adAct{height:54px;display:flex;align-items:center;justify-content:center}
#adBuy{width:100%;height:54px!important;min-height:54px!important;margin:0!important;font-size:19px!important;white-space:nowrap;animation:adPulse 1.4s ease-in-out infinite}
@keyframes adPulse{0%,100%{transform:none}50%{transform:scale(1.03)}}
.adNote{font:800 13px/1.3 system-ui;color:#7a6650;background:#efe2c8;border-radius:12px;padding:9px 12px;width:100%;box-sizing:border-box}
#adLater{margin:8px auto 0!important;height:34px!important;min-height:34px!important;padding:0 18px!important;font-size:14px!important;background:transparent!important;border:2px solid #cdbb98!important;color:#7a6650!important;box-shadow:none!important}
@media (prefers-reduced-motion:reduce){#adBuy{animation:none}}
</style>
'''
js = r'''
  /* V253: Werbeanzeigen für die ersten Waffen */
  try { (() => {
    const AD = { kan: { img: "img/ad_kan.webp", tag: "NEW GEAR", line: "Big splash damage. Cracks the tough guys." },
                 ton: { img: "img/ad_ton.webp", tag: "FREE GIFT", line: "Your first one is free – it's already in your Pocket!" },
                 mix: { img: "img/ad_mix.webp", tag: "NEW GEAR", line: "Fills a hole to the top and buries monsters." } };
    const ov = document.createElement("div"); ov.id = "ovAd"; ov.hidden = true;
    ov.innerHTML = `<div class="adCard"><div class="adPic" id="adPic"><span class="adTag" id="adTag"></span><span class="adWave" id="adWave"></span><span class="adPrice" id="adPrice"></span></div>
      <div class="adBody"><h2 id="adName"></h2><p id="adLine"></p><div class="adMet" id="adMet"></div><div class="adAct" id="adAct"></div><button id="adLater"></button></div></div>`;
    document.body.appendChild(ov);
    const $a = id => document.getElementById(id); let cur = null;
    const price = k => k === "kan" ? WEAP.kan.cost : k === "mix" ? MIX_COST : TON_COST;
    function slotTower() { const L = limits(Math.max(1, S.wave)); for (const t of S.towers.values()) if (t.w.length < L.weapons) return t; return null; }
    function why(k) { const p = price(k); if (S.gold < p) return `Not enough gold yet · ${p} gold`; if (k === "kan" && !slotTower()) return S.towers.size ? "All towers are full · tap a tower later" : "Build a tower first, then mount it"; return ""; }
    function paint() { const k = cur, w = why(k), act = $a("adAct");
      act.innerHTML = w ? `<div class="adNote">${w}</div>` : `<button class="btn-accent" id="adBuy">${k === "ton" ? "BUY ANOTHER" : "BUY NOW"} · ${price(k)} GOLD ▶</button>`;
      $a("adLater").textContent = w || k === "ton" ? "Got it" : "Later"; }
    function show(k) { cur = k; const a = AD[k], d = INTRO_GEAR[k];
      $a("adPic").style.backgroundImage = `url(${a.img})`; $a("adTag").textContent = a.tag; $a("adWave").textContent = `WAVE ${S.wave}`;
      $a("adPrice").textContent = k === "ton" ? "1 FREE" : `${price(k)} GOLD`; $a("adName").textContent = d[0].toUpperCase(); $a("adLine").textContent = a.line;
      $a("adMet").innerHTML = d[2]().filter(x => !/gold|free/i.test(x)).slice(0, 3).map(x => `<span>${x}</span>`).join("");
      lastW = why(k); paint(); $("ovIntro").hidden = true; ov.hidden = false; requestAnimationFrame(() => ov.classList.add("on"));
      try { snd("radio"); } catch (e) {} }
    function close(bought) { ov.classList.remove("on"); ov.hidden = true; const k = cur; cur = null; try { closeIntro(); } catch (e) {}
      if (bought) try { toast(`${INTRO_GEAR[k][0].toUpperCase()} · ${k === "kan" ? "mounted on your tower" : "in your Pocket"}`, "ARMORY", 2000); } catch (e) {} }
    function buy() { const k = cur; if (!k || why(k)) { paint(); return; } const p = price(k);
      if (k === "kan") { const t = slotTower(); if (!t) { paint(); return; } t.w.push({ type: "kan", lvl: 1, cd: 0 }); }
      else if (k === "mix") S.mixers = (S.mixers || 0) + 1; else S.tons = (S.tons || 0) + 1;
      S.gold -= p; try { snd("shopBuy"); setTimeout(() => SFX.say("Nice!", 1.0, 1.0), 200); } catch (e) {} try { window.__vib && window.__vib([20], true); } catch (e) {} close(true); }
    ov.addEventListener("click", e => { e.stopPropagation(); if (e.target.closest("#adBuy")) buy(); else if (e.target.closest("#adLater")) { try { snd("uiTap"); } catch (er) {} close(false); } });
    let lastW = null; setInterval(() => { if (!ov.hidden && cur) { const w = why(cur); if (w !== lastW) { lastW = w; paint(); } } }, 400);
    const _si = showIntro;
    showIntro = function (q) { const r = _si.apply(this, arguments); try { if (q && q.t === "gear" && AD[q.k] && (S.wave || 0) <= 10 && !S.nuts) show(q.k); } catch (e) { console.error("ad", e); } return r; };
    window.__TT && (window.__TT.ad = { show, close });
  })(); } catch (e) { console.error("ads", e); }
'''
i = s.rfind('</body>'); s = s[:i] + css + s[i:]
i = s.rfind('})();\n</script>'); s = s[:i] + js + s[i:]
open(dst, 'w', encoding='utf-8').write(s); print('ok')
