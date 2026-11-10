#!/usr/bin/env python3
# V555: Russische Fassung aufgeräumt (Martin 10.11. 13:56: «Grafik furchtbar, teils Englisch, Texte über Knöpfen»)
# - Übersetzung findet jetzt auch GROSS geschriebene Texte (Code macht oft .toUpperCase()) → Lob, Ansagen, Joker-Effekte
# - ~200 neue RU-Texte (tools/lang_src/ru_v555.json)
# - RU-Layout: Ladenknöpfe zweizeilig, Turm-Chips kleiner, Stempel und Warnband passen ins Bild
# - Freemium-Streifen (Martin 14:10/14:11): ab W41 und W51 schwebt er oben, lässt sich nicht wegdrücken, blinkt immer stärker;
#   Antippen öffnet die Info-Karte. Ende W60: große Karte. Info-Karte: Absatz linksbündig, Titel kleiner. Schalter bleibt AUS.
import sys
src, dst = sys.argv[1], sys.argv[2]
s = open(src, encoding="utf-8").read()
def rep(a, b, n=1):
    global s
    c = s.count(a); assert c == n, (c, a[:80]); s = s.replace(a, b)

rep('const GAME_VER = "V554";', 'const GAME_VER = "V555";')

# --- Übersetzung: Groß-/Kleinschreibung egal ---
rep('''function i18nLookup(key) {   /* exakt → Zahlen-Muster → Namens-Muster → Teile an « · » */
  const D = I18N.dict; if (!D) return null;''', '''function i18nLookup(key, DD) {   /* exakt → Zahlen-Muster → Namens-Muster → Teile an « · » */
  const D = DD || I18N.dict; if (!D) return null;''')
rep('const k = i18nNorm(p); const v = k ? i18nLookup(k) : null;', 'const k = i18nNorm(p); const v = k ? i18nLookup(k, DD) : null;')
rep('const va = i18nLookup(a), vb = i18nLookup(b);', 'const va = i18nLookup(a, DD), vb = i18nLookup(b, DD);')
rep('''  let v = I18N.cache.get(key); if (v === undefined) { v = i18nLookup(key); if (v == null) {''',
    '''  let v = I18N.cache.get(key); if (v === undefined) { v = i18nLookup(key); if (v == null) v = i18nCI(key); if (v == null) {''')
rep('function i18nApplyAll() {', '''function i18nCI(key) {   /* V555: Text ohne Rücksicht auf Groß-/Kleinschreibung suchen (Code schreibt oft GROSS) */
  const D = I18N.dict; if (!D || !/[A-Za-z]{2}/.test(key)) return null;
  if (I18N.upD !== D) { const U = {}; for (const k in D) { const u = k.toUpperCase(); if (!(u in U)) U[u] = D[k]; } I18N.up = U; I18N.upD = D; }
  const v = i18nLookup(key.toUpperCase(), I18N.up); if (v == null) return null;
  return key === key.toUpperCase() ? String(v).toUpperCase() : v; }
function i18nApplyAll() {''')

# --- Freemium-Streifen ---
rep('''  b.classList.add("on"); clearTimeout(b.__t); b.__t = setTimeout(() => b.classList.remove("on"), 9000); };''',
    '''  b.classList.add("on"); clearTimeout(b.__t); b.__t = setTimeout(() => b.classList.remove("on"), 9000); };
/* V555: Streifen ab W41 und W51 – schwebt oben, nicht wegdrückbar, blinkt immer stärker; Antippen = Info-Karte. Ende W60 = große Karte. */
const FM_BAND_W = [41, 51];
function fmBandEl() { let b = document.getElementById("fmBand"); if (!b) { b = document.createElement("div"); b.id = "fmBand"; b.setAttribute("role", "button"); document.body.appendChild(b);
    b.addEventListener("click", e => { e.stopPropagation(); try { S.fmTap = +b.dataset.t || 0; saveGame(); } catch (er) {} b.classList.remove("on", "blink"); fmInfo(FM.next() >= 0 ? FM.next() : 2); }); } return b; }
setInterval(() => { try {
  const b = document.getElementById("fmBand");
  if (!FM.on || typeof S === "undefined" || !S || !S.started || S.over || S.nuts || S.replay || S.testRun || FM.next() < 0) { if (b) b.classList.remove("on", "blink"); return; }
  const w = S.wave || 0, t = w >= FM_BAND_W[1] ? FM_BAND_W[1] : w >= FM_BAND_W[0] ? FM_BAND_W[0] : 0;
  if (w >= 60 && !S.inWave && !S.fmEnd60) { S.fmEnd60 = 1; if (b) b.classList.remove("on", "blink"); window.__fmBanner("A", 60); return; }
  const busy = document.body.classList.contains("mapUp") || !!document.querySelector("#ovFm:not([hidden])");
  if (!t || S.fmTap === t || busy) { if (b) b.classList.remove("on", "blink"); return; }
  const el = fmBandEl(); if (!el.classList.contains("on") || el.dataset.t !== String(t)) { el.dataset.t = t; el.__t0 = performance.now();
    el.innerHTML = `<i>🔒</i><span><b>${60 - Math.min(59, w) === 1 ? "LAST FREE WAVE" : `${60 - w} WAVES TO ASIA`}</b><small>From ${FM.one} or 2 friends</small></span><em>▶</em>`; el.classList.add("on"); }
  else { const bb = el.querySelector("b"), txt = 60 - w <= 1 ? "LAST FREE WAVE" : `${60 - w} WAVES TO ASIA`; if (bb && bb.dataset.src !== txt) { bb.dataset.src = txt; bb.textContent = txt; } }
  /* Blinkstärke 0–5: Wellen seit Start + Minuten ignoriert, ab W51 eine Stufe mehr */
  const lvl = Math.min(5, (t === FM_BAND_W[1] ? 1 : 0) + Math.floor((w - t) / 2) + Math.floor((performance.now() - (el.__t0 || 0)) / 90000));
  el.style.setProperty("--fmBl", [2.6, 2.0, 1.5, 1.1, 0.8, 0.55][lvl] + "s"); el.style.setProperty("--fmGl", (0.35 + lvl * 0.13).toFixed(2)); el.classList.add("blink");
} catch (e) {} }, 1000);
try { if (typeof SAVE_KEYS !== "undefined") ["fmTap", "fmEnd60"].forEach(k => { if (!SAVE_KEYS.includes(k)) SAVE_KEYS.push(k); }); } catch (e) {}''')
rep('''#fmBand.on{transform:translate(-50%,0);opacity:1;pointer-events:auto}''',
    '''#fmBand.on{transform:translate(-50%,0);opacity:1;pointer-events:auto}
#fmBand.blink{animation:fmBlink var(--fmBl,2.6s) ease-in-out infinite}
@keyframes fmBlink{0%,100%{box-shadow:0 4px 0 rgba(0,0,0,.35),0 0 0 0 rgba(255,201,60,0);border-color:#ffc93c}50%{box-shadow:0 4px 0 rgba(0,0,0,.35),0 0 22px 6px rgba(255,201,60,var(--fmGl,.35));border-color:#fff3b0}}''')
rep('#ovFm p{margin:0 0 10px;', '#ovFm p{margin:0 0 10px;text-align:left;')
rep('#ovFm h2{margin:0 0 4px;font:400 30px/1 Bangers', '#ovFm h2{margin:0 0 6px;font:400 26px/1.05 Bangers')

# --- RU-Layout ---
rep('#ovMap{position:fixed;inset:0;z-index:990;', '''html[lang=ru] #sheet #sheetIn .shopTiles .shopItem button{flex-direction:column!important;white-space:normal!important;line-height:1.05!important;gap:0!important;padding:3px 4px!important;font-size:11.5px!important;letter-spacing:.02em!important;min-height:38px!important}
html[lang=ru] #sheet #sheetIn .shopTiles .shopItem button *{white-space:nowrap!important;font-size:10px!important;letter-spacing:0!important}
html[lang=ru] #sheet #sheetIn .shopTiles .shopItem .useBtn{font-size:11px!important;flex-direction:row!important;min-height:28px!important}
html[lang=ru] #sheet #sheetIn .shopTiles .shopItem:has(.useBtn){grid-template-columns:34px 1fr!important}
html[lang=ru] #sheet #sheetIn .shopTiles .shopItem:has(.useBtn) button:not(.useBtn){grid-column:1 / -1!important;grid-row:2!important}
html[lang=ru] #sheet #sheetIn .shopTiles .shopItem:has(.useBtn) .useBtn{grid-column:1 / -1!important;grid-row:3!important}
html[lang=ru] #sheet .ledgerBubble span{font-size:12.5px!important;line-height:1.2!important}
html[lang=ru] #sheetIn .slotRow button span{font-size:13px!important;letter-spacing:0!important}
html[lang=ru] #sheetIn .slotRow button small{font-size:9.5px!important}
html[lang=ru] .stamp{max-width:calc(100vw - 28px)!important;white-space:normal!important;text-align:center;font-size:clamp(20px,6.6vw,32px)!important;line-height:1.05!important}
html[lang=ru] .stamp.t4{font-size:clamp(22px,7.4vw,36px)!important}
html[lang=ru] .mayday span{font-size:12px;letter-spacing:.03em;white-space:nowrap}
html[lang=ru] .mayday i{font-size:10px;letter-spacing:.04em;white-space:nowrap}
#ovMap{position:fixed;inset:0;z-index:990;''')

open(dst, "w", encoding="utf-8").write(s)
print("ok")
