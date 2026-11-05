"""V283 (Martin 16:53):
- Kanone: neuer Abschuss «B · Holz-Tock» (tock 420 Hz + triangle 260→200 Hz), kein Bass mehr.
- Boss-Hack als große Werbeanzeige: wenn das Hack-Angebot startet, erst eine fast bildschirmfüllende Karte (#ovHackAd, Bild Blue vs. Boss,
  rosa Knopf «HACK THE BOSS ▶» → sofort ins Duell). «Later» erst nach 3 s; danach bleibt der rosa Knopf oben mit dem Countdown.
  Countdown steht, solange die Karte offen ist (S.intro).
- Boss-Hack-Ausnahme (2 Wellen nach Vormerkung) hält trotzdem 30 s Abstand zum letzten Fenster/Angebot.
- Neuer Kontinent: freies Spielfeld (Startsteine unten), Türme samt Waffen ziehen mit (je Spalte auf eigenem Stein).
- Major-Ledger-Sprechblase: nur so hoch wie nötig (min-height 2,5em entfernt)."""
import sys
src, dst = sys.argv[1], sys.argv[2]
s = open(src, encoding='utf-8').read()
def rep(a, b, cnt=1):
    global s
    n = s.count(a); assert n == cnt, (n, a[:70]); s = s.replace(a, b)
rep('const GAME_VER = "V282";', 'const GAME_VER = "V283";')
rep('kan: k => k.thump(65, 34, 0.26, 0.304, "triangle"),', 'kan: k => { k.tock(420, 0.05, 0.3); k.thump(260, 200, 0.05, 0.18, "triangle"); },')
rep('window.__offerOK = (force) => force || (',
    'window.__offerOK = (force) => force ? performance.now() - Math.max(window.__evtLast || -1e9, window.__offerLast || -1e9) >= 30000 : (')
rep('S.hackOfferUntil = performance.now() + HK_OFFER_S * 1000; snd("radio");',
    'S.hackOfferUntil = performance.now() + HK_OFFER_S * 1000; try { window.__hackAd && window.__hackAd(); } catch (e) {} snd("radio");')
rep('function uiWinOpen() { try { const v = id => { const e = document.getElementById(id); return e && !e.hidden && getComputedStyle(e).display !== "none"; };',
    'function uiWinOpen() { try { const v = id => { const e = document.getElementById(id); return e && !e.hidden && getComputedStyle(e).display !== "none"; }; if (v("ovHackAd")) return true;')
rep('function hkHold() { return !!(S.mapShow || S.intro ||', 'function hkHold() { return !!(S.mapShow || S.intro || S.hackAdOpen ||')
rep('if (!S || !S.intro || S.joinOpen || S.signOpen || S.banditOpen || S.over) { stuck = 0; return; }', 'if (!S || !S.intro || S.joinOpen || S.signOpen || S.banditOpen || S.hackAdOpen || S.over) { stuck = 0; return; }')
js = r'''
  /* V283: Boss-Hack als große Werbeanzeige */
  try { (() => {
    const ov = document.createElement("div"); ov.id = "ovHackAd"; ov.hidden = true;
    ov.innerHTML = `<div class="hkCard"><div class="hkPic"><span class="hkTag">BOSS HACK</span><span class="hkWave" id="hkAdWave"></span><span class="hkBurst">LOOT!</span></div>
      <div class="hkBody"><small class="hkKick">BOSS SIGNAL DETECTED</small><h2>BEAT THE BOSS!</h2><p>Hack the boss in a quick duel and grab the big loot.</p>
      <button class="hkGo" id="hkAdGo">HACK THE BOSS ▶</button><button class="hkLater" id="hkAdLater">Later</button></div></div>`;
    document.body.appendChild(ov); let lockT = null;
    const close = () => { ov.classList.remove("on"); ov.hidden = true; if (S) { S.intro = false; S.hackAdOpen = false; } };
    window.__hackAd = () => { if (!S) return; S.intro = true; S.hackAdOpen = true; document.getElementById("hkAdWave").textContent = `WAVE ${S.wave}`;
      const later = document.getElementById("hkAdLater"); later.classList.add("wait"); clearTimeout(lockT); lockT = setTimeout(() => later.classList.remove("wait"), 3000);
      ov.hidden = false; requestAnimationFrame(() => ov.classList.add("on")); try { window.__vib && window.__vib([35, 50, 35], true); } catch (e) {} };
    ov.addEventListener("click", e => { e.stopPropagation();
      if (e.target.closest("#hkAdGo")) { try { snd("uiTap"); } catch (er) {} close(); try { openHack(); } catch (er) { console.error("hackAd", er); } }
      else if (e.target.closest("#hkAdLater") && !e.target.closest(".wait")) { try { snd("uiTap"); } catch (er) {} close(); } });
  })(); } catch (e) { console.error("hackAd", e); }
'''
i = s.rindex('})();\n</script>'); s = s[:i] + js + s[i:]
css = r'''
<style id="v283hack">
#ovHackAd{position:fixed;inset:0;z-index:960;display:flex;align-items:center;justify-content:center;padding:calc(10px + env(safe-area-inset-top,0px)) max(10px,env(safe-area-inset-right,0px)) calc(10px + env(safe-area-inset-bottom,0px)) max(10px,env(safe-area-inset-left,0px));background:rgba(40,8,32,.62);opacity:0;transition:opacity .25s}
#ovHackAd.on{opacity:1}
#ovHackAd .hkCard{width:min(100%,460px);max-height:100%;overflow:auto;border:3px solid #17150c;border-radius:20px;background:#fff7ee;box-shadow:0 14px 0 rgba(0,0,0,.35);transform:scale(.86);transition:transform .35s cubic-bezier(.3,1.5,.5,1)}
#ovHackAd.on .hkCard{transform:scale(1)}
#ovHackAd .hkPic{position:relative;aspect-ratio:1050/445;max-width:100%;background:url(img/2a5aeb2df0.webp) center/cover;border-bottom:3px solid #17150c;border-radius:17px 17px 0 0}
#ovHackAd .hkTag{position:absolute;left:10px;top:10px;font-family:Bangers,system-ui;font-size:22px;letter-spacing:1px;color:#fff;background:linear-gradient(180deg,#d6409f,#7a1f60);border:2.5px solid #17150c;border-radius:10px;padding:4px 10px 2px}
#ovHackAd .hkWave{position:absolute;right:10px;top:10px;font:900 13px/1 system-ui;background:#fff7ee;color:#17150c;border:2.5px solid #17150c;border-radius:9px;padding:6px 9px}
#ovHackAd .hkBurst{position:absolute;left:50%;bottom:10px;transform:translateX(-50%) rotate(-6deg);font-family:Bangers,system-ui;font-size:24px;color:#fff;-webkit-text-stroke:1px #7a1f60;background:#d6409f;border:2.5px solid #17150c;border-radius:12px;padding:3px 12px 1px;animation:hkWob 1s ease-in-out infinite}
@keyframes hkWob{50%{transform:translateX(-50%) rotate(4deg) scale(1.08)}}
#ovHackAd .hkBody{display:flex;flex-direction:column;align-items:center;gap:8px;padding:14px 16px 16px;text-align:center}
#ovHackAd .hkKick{font:900 12px/1 system-ui;letter-spacing:.14em;color:#b0328c}
#ovHackAd h2{margin:0;font-family:Bangers,system-ui;font-weight:400;font-size:40px;line-height:1;letter-spacing:1px;color:#d6409f;-webkit-text-stroke:1.4px #17150c}
#ovHackAd p{margin:0;font:700 15px/1.4 system-ui;color:#3a2a1a;max-width:32ch}
#ovHackAd .hkGo{width:100%;margin-top:6px;font-family:Bangers,system-ui;font-size:28px;letter-spacing:1px;color:#fff!important;background:linear-gradient(180deg,#e04aa8,#8a2470)!important;border:3px solid #17150c!important;text-shadow:0 2px 0 #4d1240;border-radius:14px;padding:14px 10px 10px;box-shadow:0 5px 0 #4d1240;cursor:pointer;animation:hpPulse 1.1s ease-in-out infinite}
#ovHackAd .hkGo:active{transform:translateY(3px);box-shadow:0 2px 0 #4d1240}
#ovHackAd .hkLater{font:800 14px/1 system-ui;color:#7a6a55!important;background:transparent!important;border:2px solid #e2d3bc!important;box-shadow:none!important;border-radius:12px;padding:10px 22px;cursor:pointer;transition:opacity .3s}
#ovHackAd .hkLater.wait{opacity:.35;pointer-events:none}
@media (prefers-reduced-motion:reduce){#ovHackAd .hkBurst,#ovHackAd .hkGo{animation:none}}
</style>
'''
i = s.rindex('</body>'); s = s[:i] + css + s[i:]

# Martin 16:59: neuer Kontinent = freies Spielfeld (nur unten ein paar zufällige Steine wie beim Spielstart); Türme ziehen mit,
# jeder Turm steht danach in seiner Spalte auf einem eigenen Stein auf dem neuen Boden, Waffen bleiben.
rep('if (P.p === 0 && P.d === 0 && S.wave > 1) { const vk',
    'if (P.p === 0 && P.d === 0 && S.wave > 1 && !S.nuts) { try { window.__contFresh && window.__contFresh(); } catch (e) { console.error("contFresh", e); } }\n    if (P.p === 0 && P.d === 0 && S.wave > 1) { const vk')
js2 = r'''
  /* V283: neuer Kontinent – freies Spielfeld, Türme ziehen mit */
  window.__gdim = () => [GW, GH];
  window.__contFresh = () => { if (!S) return; const keep = [...S.towers.values()].sort((a, b) => a.x - b.x);
    S.grid = new Uint8Array(NN); S.towers = new Map(); seedGarbage();
    const used = new Set();
    for (const t of keep) { let x = Math.max(1, Math.min(GW - 2, t.x)); for (let k = 0; k < GW && used.has(x); k++) x = x >= GW - 2 ? 1 : x + 1; used.add(x);
      let y = GH - 1; while (y > 0 && S.grid[y * GW + x]) y--; S.grid[y * GW + x] = 1 + (t.id % 7); t.x = x; t.y = y; S.towers.set(y * GW + x, t); }
    S.monsters = []; S.shots = []; try { gridChanged(); } catch (e) { S.dirty = true; } };
'''
i = s.rindex('})();\n</script>'); s = s[:i] + js2 + s[i:]
css2 = r'''
<style id="v283bubble">
#sheet .ledgerTop .ledgerBubble{min-height:0!important;height:auto!important;align-content:start!important}
#sheet .ledgerTop .ledgerBubble span{min-height:0!important}
</style>
'''
i = s.rindex('</body>'); s = s[:i] + css2 + s[i:]
open(dst, 'w', encoding='utf-8').write(s)
