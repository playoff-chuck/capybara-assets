"""V299 (Übergabe-Punkt 2): Gratis-Air-Drops als Werbeanzeigen (Free-Modus).
Ten-ton-Rettungsgeschenke W8/14/22 (wenn Ten-ton schon bekannt), Clean-Sweep-Drop, Medkit und ±90°-Paket
kommen nicht mehr als Kiste #crate bzw. General-Meldung, sondern als große FREE-Anzeige (img/ad_drop_free.webp,
img/ad_med_free.webp). Eingereiht über __whenCalm (5 s Ruhe), nur am Spielscreen; die Wirkung (Heilung,
Feld gerade, Gold) passiert sofort wie bisher."""
import sys
src, dst = sys.argv[1], sys.argv[2]
s = open(src, encoding='utf-8').read()
def rep(a, b, cnt=1):
    global s
    n = s.count(a); assert n == cnt, (n, a[:70]); s = s.replace(a, b)
rep('const GAME_VER = "V298";', 'const GAME_VER = "V299";')

# 1) airDrop: Medkit / ±90°-Paket / Clean Sweep als Gratis-Anzeige
rep('function airDrop(title, loot) {\n', 'function airDrop(title, loot) { const _t0 = title, _l0 = loot;\n')
rep('  if (!med && !rp) { genWaveMsg(title, loot); return; }',
    '  if ((med || rp || title === "CLEAN SWEEP") && window.__dropAd && !S.nuts) { if (med || rp) genWaveMsg(_t0, _l0); window.__dropAd(med ? "med" : rp ? "rot" : "sweep", { loot, rp: rpBack }); return; }   /* V299 */\n'
    '  if (!med && !rp) { genWaveMsg(title, loot); return; }')

# 2) Ten-ton-Rettungsgeschenk: ist Ten-ton schon bekannt, kommt die Gratis-Anzeige
rep('if (!S.seen["g:ton"]) S.introQ.push({ t: "gear", k: "ton" }); }',
    'if (!S.seen["g:ton"]) S.introQ.push({ t: "gear", k: "ton" }); else if (window.__dropAd) window.__dropAd("ton"); }')

# 3) Anzeige-Baustein: showDrop im Anzeigen-Modul
rep('''    function paint() { if (isFree) { $a("adAct").innerHTML = `<button class="btn-accent" id="adFree">${cur === "elite" ? "AWESOME! · LET'S GO ▶" : "AWESOME! · IT'S FREE ▶"}</button>`;''',
    '''    function paint() { if (isFree) { $a("adAct").innerHTML = `<button class="btn-accent" id="adFree">${cur === "drop" ? dropBtn : cur === "elite" ? "AWESOME! · LET'S GO ▶" : "AWESOME! · IT'S FREE ▶"}</button>`;''')
rep('''    function close(bought) { ov.classList.remove("on"); ov.hidden = true; const k = cur; cur = null;''',
    '''    function close(bought) { ov.classList.remove("on"); ov.hidden = true; const k = cur; cur = null; if (k === "drop") { bought = false; $a("adCard").classList.remove("drop"); $a("saleWas").hidden = false; }''')
rep('''    window.__TT && (window.__TT.ad = { show, close });''',
    '''    /* V299: Gratis-Air-Drops als Anzeige */
    let dropBtn = "AWESOME! · IT'S FREE ▶";
    function showDrop(kind, o) { o = o || {}; const tc = typeof TON_COST !== "undefined" ? TON_COST : 300;
      const gold = ((o.loot || []).find(x => x[0] === "gold") || [])[2] || "";
      const D = { ton: { img: "img/ad_drop_free.webp", name: "TEN-TON DROP", mega: "RESCUE DROP", only: "ON THE HOUSE!", was: `${tc} GOLD`, now: "FREE", pct: "−100%", st: ["−100%", "GIFT!", "FREE"], price: "1 FREE",
                       line: "HQ sends you a Ten-ton drop – it's already in your Pocket!", met: ["Crushes monsters", "Stack ÷ 2", "In your Pocket"], btn: "AWESOME! · IT'S FREE ▶" },
                 sweep: { img: "img/ad_drop_free.webp", name: "CLEAN SWEEP", mega: "AIR DROP", only: "FIELD WIPED CLEAN!", was: "", now: `${gold} GOLD`, pct: "+1 MEDAL", st: ["WOW!", "GIFT!", "FREE"], price: `${gold} GOLD`,
                       line: "You cleared the whole field! HQ drops gold and a medal.", met: [`${gold} gold`, "+1 medal"], btn: "AWESOME! · COLLECT ▶" },
                 med: { img: "img/ad_med_free.webp", name: "MEDKIT", mega: "FIELD MEDIC", only: "VISION RESTORED!", was: "BLURRY", now: "SHARP", pct: "FREE", st: ["FREE", "HEAL!", "♥"], price: "FREE",
                       line: "Doc Hazel patched you up – you can see clearly again!", met: ["Vision sharp", "Wounds healed"], btn: "THANKS, DOC! ▶" },
                 rot: { img: "img/ad_drop_free.webp", name: `${o.rp || "+90°"} PACKAGE`, mega: "AIR DROP", only: "WORLD RESTORED!", was: "TILTED", now: "UPRIGHT", pct: "FREE", st: ["FREE", "GIFT!", "90°"], price: "FREE",
                       line: "The field is upright again – normal gravity is back!", met: ["Field upright", "Blocks fall down"], btn: "AWESOME! · LET'S GO ▶" } }[kind];
      if (!D) return; cur = "drop"; saleMode = true; isFree = true; dropBtn = D.btn; late = true; S.intro = true; S.adOpen = true;
      const card = $a("adCard"); card.classList.add("sale", "free", "drop"); const PS = [[14, 40], [14, 76], [52, 86]];
      [1, 2, 3].forEach(n => { const el = card.querySelector(".saleSt.s" + n); if (el) { el.style.left = PS[n - 1][0] + "%"; el.style.top = PS[n - 1][1] + "%"; el.textContent = D.st[n - 1]; } });
      $a("adPic").style.backgroundImage = `url(${D.img})`; $a("adPic").style.backgroundPosition = ""; $a("adTag").textContent = "FREE"; $a("adWave").textContent = `WAVE ${S.wave}`; $a("adPrice").textContent = D.price;
      $a("adName").textContent = D.name; $a("adLine").textContent = D.line; $a("adMet").innerHTML = D.met.map(x => `<span>${x}</span>`).join("");
      $a("saleWas").textContent = D.was; $a("saleWas").hidden = !D.was; $a("saleNow").textContent = D.now; $a("salePct").textContent = D.pct;
      card.querySelector(".saleMega").textContent = D.mega; card.querySelector(".saleOnly").textContent = D.only;
      paint(); window.__adLast = performance.now(); $("ovIntro").hidden = true; ov.hidden = false; requestAnimationFrame(() => ov.classList.add("on"));
      try { snd("crate"); if (kind === "sweep" || kind === "ton") [0.5, 0.8].forEach(d => setTimeout(() => snd("coin"), d * 1000)); } catch (e) {} try { window.__vib && window.__vib([20, 40, 20], true); } catch (e) {} }
    const dropQ = []; let dropWait = false;
    function pumpDrop() { if (dropWait || !dropQ.length) return; dropWait = true;
      window.__whenCalm(() => { if (!ov.hidden || (window.__playScreen && !window.__playScreen()) || S.nuts) { dropWait = false; setTimeout(pumpDrop, 1000); return; }
        const [k, o] = dropQ.shift(); dropWait = false; showDrop(k, o); const iv = setInterval(() => { if (ov.hidden) { clearInterval(iv); setTimeout(pumpDrop, 300); } }, 300); }, 5000); }
    window.__dropAd = (k, o) => { dropQ.push([k, o]); pumpDrop(); };
    window.__TT && (window.__TT.ad = { show, close, showDrop });''')
rep('</body>', '''<style id="v299drop">
.adCard.drop #saleWas[hidden]{display:none}
.adCard.drop .salePrice #salePct{white-space:nowrap}
</style>
</body>''')
open(dst, 'w', encoding='utf-8').write(s)
print("ok")
