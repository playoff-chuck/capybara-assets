#!/usr/bin/env python3
"""V456 – Sprachschicht (Martin 08.11. 15:25): alle sichtbaren Texte laufen über eine Sprachtabelle lang/<code>.json,
Canvas-Texte und Sprachclips eingeschlossen; Sprach-Auswahl mit Flaggen ganz am Anfang (vor dem Startbild-Tipp);
Test-Links ?lang=xx, ?i18n=audit (fehlende Einträge im Protokoll), ?test=nuts (Nuts-Abstecher direkt).
Schritt 1: nur Englisch (Identität) – zum Prüfen, dass alle Screens aus der Tabelle identisch laufen.
Nutzung: python3 tools/patch456.py src dst"""
import sys
src, dst = sys.argv[1], sys.argv[2]
s = open(src, encoding="utf-8").read()

def rep(a, b, n=1):
    global s
    c = s.count(a)
    assert c == n, (c, a[:80])
    s = s.replace(a, b)

rep('const GAME_VER = "V455";', 'const GAME_VER = "V456";')

JS = r'''
/* ===== V456: Sprachschicht ===== */
const LANGS = { en: { flag: "🇬🇧🇺🇸", name: "English" }, es: { flag: "🇪🇸", name: "Español" }, pt: { flag: "🇧🇷🇵🇹", name: "Português" }, de: { flag: "🇦🇹🇩🇪🇨🇭", name: "Deutsch" }, ru: { flag: "🇷🇺", name: "Русский" } };
const I18N = { lang: "en", dict: null, cache: new Map(), miss: new Set(), seen: new Set(), audit: false, names: [], ready: false };
(function () { try { const q = new URLSearchParams(location.search), l = q.get("lang"); if (l && LANGS[l]) { localStorage.setItem("capy-lang", l); } I18N.audit = q.get("i18n") === "audit"; } catch (e) {}
  try { const l = localStorage.getItem("capy-lang"); if (l && LANGS[l]) I18N.lang = l; } catch (e) {} })();
const I18N_NUM = /\d[\d.,:/]*\d|\d/g, I18N_WS = /\s+/g;
function i18nNorm(t) { return String(t).replace(I18N_WS, " ").trim(); }
function i18nLookup(key) {   /* exakt → Zahlen-Muster → Namens-Muster → Teile an « · » */
  const D = I18N.dict; if (!D) return null;
  if (D[key] != null) return D[key];
  const nums = key.match(I18N_NUM); if (nums) { const pat = key.replace(I18N_NUM, "#"); const v = D[pat]; if (v != null) { let i = 0; return v.replace(/#/g, () => nums[i++] ?? "#"); } }
  for (const nm of I18N.names) { if (nm && key.includes(nm)) { const pat = key.split(nm).join("@"), v = D[pat]; if (v != null) return v.split("@").join(D[nm] != null ? D[nm] : nm); } }
  if (key.includes(" · ")) { const parts = key.split(" · "); let hit = false; const out = parts.map(p => { const k = i18nNorm(p); const v = k ? i18nLookup(k) : null; if (v != null) hit = true; return v != null ? v : p; }); if (hit) return out.join(" · "); }
  return null; }
function T(t) {
  if (t == null) return t; const raw = String(t); const key = i18nNorm(raw); if (!key || !/[A-Za-zÀ-ÿ]{2}/.test(key)) return raw;
  if (I18N.audit) I18N.seen.add(key);
  if (!I18N.dict) return raw;
  let v = I18N.cache.get(key); if (v === undefined) { v = i18nLookup(key); if (v == null) { I18N.miss.add(key); v = null; } I18N.cache.set(key, v); }
  if (v == null) return raw;
  const lead = raw.match(/^\s*/)[0], tail = raw.match(/\s*$/)[0]; return lead + v + tail; }
const I18N_SKIP = new Set(["SCRIPT", "STYLE", "TEXTAREA", "INPUT", "CODE"]), I18N_ATTR = ["placeholder", "aria-label", "title"], i18nDone = new WeakMap();
function i18nText(n) { const d = n.data; if (!d || !d.trim()) return; const p = n.parentNode; if (!p || I18N_SKIP.has(p.nodeName)) return; const m = i18nDone.get(n); if (m && m.out === d) return; const out = T(d); i18nDone.set(n, { out }); if (out !== d) n.data = out; }
function i18nEl(el) { if (!el || el.nodeType !== 1 || I18N_SKIP.has(el.nodeName)) return; for (const a of I18N_ATTR) { if (el.hasAttribute(a)) { const v = el.getAttribute(a), k = "a:" + a, m = i18nDone.get(el) || {}; if (m[k] === v) continue; const o = T(v); m[k] = o; i18nDone.set(el, m); if (o !== v) el.setAttribute(a, o); } }
  const w = document.createTreeWalker(el, NodeFilter.SHOW_TEXT | NodeFilter.SHOW_ELEMENT, null); let n; while ((n = w.nextNode())) { if (n.nodeType === 3) i18nText(n); else if (n.nodeType === 1 && !I18N_SKIP.has(n.nodeName)) { for (const a of I18N_ATTR) if (n.hasAttribute(a)) { const v = n.getAttribute(a), k = "a:" + a, m = i18nDone.get(n) || {}; if (m[k] === v) continue; const o = T(v); m[k] = o; i18nDone.set(n, m); if (o !== v) n.setAttribute(a, o); } } } }
function i18nApplyAll() { try { i18nEl(document.body); } catch (e) {} }
(function () { const obs = new MutationObserver(ms => { for (const m of ms) { if (m.type === "characterData") { i18nText(m.target); continue; } if (m.type === "attributes") { i18nEl(m.target); continue; } m.addedNodes.forEach(n => { if (n.nodeType === 3) i18nText(n); else i18nEl(n); }); } });
  const start = () => obs.observe(document.body, { childList: true, subtree: true, characterData: true, attributes: true, attributeFilter: I18N_ATTR }); if (document.body) start(); else document.addEventListener("DOMContentLoaded", start); })();
(function () { try { const P = CanvasRenderingContext2D.prototype, ft = P.fillText, st = P.strokeText, mt = P.measureText;
  P.fillText = function (t) { arguments[0] = T(t); return ft.apply(this, arguments); }; P.strokeText = function (t) { arguments[0] = T(t); return st.apply(this, arguments); }; P.measureText = function (t) { return mt.call(this, T(t)); }; } catch (e) {} })();
function i18nLoad(lang, cb) {
  I18N.lang = lang; I18N.cache.clear(); I18N.miss.clear(); try { localStorage.setItem("capy-lang", lang); } catch (e) {} document.documentElement.lang = lang;
  fetch(`lang/${lang}.json?v=${GAME_VER}`).then(r => r.ok ? r.json() : {}).catch(() => ({})).then(d => { I18N.dict = d || {}; I18N.names = Object.keys(I18N.dict).filter(k => /^[A-Z][A-Za-z' -]{2,24}$/.test(k) && !k.includes("#")).sort((a, b) => b.length - a.length); I18N.ready = true; i18nApplyAll();
    if (lang !== "en") fetch(`lang/voice_${lang}.json?v=${GAME_VER}`).then(r => r.ok ? r.json() : null).catch(() => null).then(v => { if (!v) return; try { for (const k in (v.v || {})) VOICE[k] = v.v[k]; for (const k in (v.t || {})) VOICE_TEXT[k] = v.t[k]; } catch (e) {} });
    cb && cb(); }); }
window.__i18n = { get lang() { return I18N.lang; }, miss: () => [...I18N.miss].sort(), seen: () => [...I18N.seen].sort(), set: l => i18nLoad(l), apply: i18nApplyAll, T };
function i18nPicker(onDone) {   /* ganz am Anfang: nur Flagge wählen */
  const ov = document.createElement("div"); ov.id = "ovLang"; ov.innerHTML = `<div class="lgBox"><div class="lgTitle">CAPYBARA SQUAD</div><div class="lgSub">Choose your language · Elige idioma · Escolha o idioma · Sprache wählen · Выберите язык</div>${Object.entries(LANGS).map(([k, v]) => `<button data-lang="${k}"><span class="lgFlag">${v.flag}</span><span class="lgName">${v.name}</span></button>`).join("")}</div>`;
  document.body.appendChild(ov);
  ov.addEventListener("click", e => { const b = e.target.closest("[data-lang]"); if (!b) return; e.stopPropagation(); const l = b.dataset.lang; ov.classList.add("out"); i18nLoad(l, () => { setTimeout(() => ov.remove(), 400); onDone && onDone(); }); }); }
/* ===== Ende V456 ===== */
'''
rep('const GAME_VER = "V456";', 'const GAME_VER = "V456";' + JS)

# Startbild: zuerst Sprache wählen (wenn noch keine gespeichert), dann wie bisher TAP TO START
rep('''  const go = () => { if (done) return; done = true; try { LS.set("tarnturm-terms", "1"); renderModes(); SFX.init(); SFX.music.menu(); } catch (e) {} sp.classList.add("out"); setTimeout(() => sp.remove(), 650); };
  sp.addEventListener("click", go); setTimeout(go, 6000); })();''',
'''  const go = () => { if (done) return; done = true; try { LS.set("tarnturm-terms", "1"); renderModes(); SFX.init(); SFX.music.menu(); } catch (e) {} sp.classList.add("out"); setTimeout(() => sp.remove(), 650); };
  let hasLang = false; try { hasLang = !!localStorage.getItem("capy-lang"); } catch (e) {}
  if (!hasLang) { sp.classList.add("pick"); i18nPicker(() => { sp.classList.remove("pick"); sp.addEventListener("click", go); setTimeout(go, 6000); }); }   /* V456: erst Flagge wählen */
  else { try { i18nLoad(I18N.lang); } catch (e) {} sp.addEventListener("click", go); setTimeout(go, 6000); } })();''')

# Test-Link ?test=nuts
rep('if (q === "elite") { try { LS.del("capy-wow-elite"); } catch (e) {} S.testRun = false; S.gold += 200; }',
    'if (q === "elite") { try { LS.del("capy-wow-elite"); } catch (e) {} S.testRun = false; S.gold += 200; } if (q === "nuts") { setTimeout(() => { try { S.testRun = false; S.inWave = false; startDetour(0); } catch (e) {} }, 1500); }   /* V456: Nuts direkt */')
rep('weed5: 131, elite: 6, peek: 3,', 'weed5: 131, elite: 6, peek: 3, nuts: 31,')

CSS = r'''
/* V456: Sprachwahl */
#ovLang{position:fixed;inset:0;z-index:260;display:flex;align-items:center;justify-content:center;background:rgba(40,20,12,.55);backdrop-filter:blur(3px);transition:opacity .35s}#ovLang.out{opacity:0;pointer-events:none}
#ovLang .lgBox{width:min(360px,calc(100vw - 32px));background:#fff7e8;border:3px solid #3a2414;border-radius:20px;box-shadow:0 6px 0 #3a2414;padding:16px 14px 14px;display:grid;gap:8px}
#ovLang .lgTitle{font:400 30px/1 Bangers,system-ui;letter-spacing:1px;text-align:center;color:#ee7a2c;-webkit-text-stroke:1px #3a2414}
#ovLang .lgSub{font:700 11.5px/1.3 "Baloo 2",system-ui;color:#7a5a3c;text-align:center;margin-bottom:4px}
#ovLang button{display:grid;grid-template-columns:auto 1fr;align-items:center;gap:12px;min-height:52px;padding:6px 14px;background:#fff;border:3px solid #3a2414;border-radius:14px;box-shadow:0 3px 0 #3a2414;font:800 18px "Baloo 2",system-ui;color:#3a2414;text-align:left;cursor:pointer}
#ovLang button:active{transform:translateY(2px);box-shadow:0 1px 0 #3a2414}
#ovLang .lgFlag{font-size:24px;letter-spacing:2px;line-height:1}
#splash.pick .spGo,#splash.pick .spDots{visibility:hidden}
'''
rep('#ovDaily .dlNote{font-size:12px;color:#7a5a3c;margin-top:8px;text-align:center}\n</style>', '#ovDaily .dlNote{font-size:12px;color:#7a5a3c;margin-top:8px;text-align:center}\n' + CSS + '</style>')

open(dst, "w", encoding="utf-8").write(s)
print("ok", dst)

# --- Nachtrag (Martin 15:28): Daily-Mission leichter für Anfänger, Schwierigkeit nach Spielstand (4 Stufen) ---
s = open(dst, encoding="utf-8").read()
rep('const DAILY_MSN = [["k", "Splat {n} monsters", [40, 60, 90]], ["l", "Clear {n} rows", [12, 18, 25]], ["w", "Finish {n} waves", [6, 10, 15]], ["t", "Build {n} towers", [6, 9, 12]], ["c3", "Clear 3 rows at once {n} times", [1, 2, 3]], ["sp", "Squish {n} monsters with blocks", [3, 5, 8]]];',
    'const DAILY_MSN = [["k", "Splat {n} monsters", [25, 40, 60, 90]], ["l", "Clear {n} rows", [8, 12, 18, 25]], ["w", "Finish {n} waves", [4, 6, 10, 15]], ["t", "Build {n} towers", [4, 6, 9, 12]], ["c3", "Clear 3 rows at once {n} times", [1, 1, 2, 3]], ["sp", "Squish {n} monsters with blocks", [2, 3, 5, 8]]];   /* V456: Stufe nach Spielstand – Anfänger (bis W30) · W30+ · W60+ · W100+ */')
rep('tier = bw >= 60 ? 2 : bw >= 35 ? 1 : 0;', 'tier = bw >= 100 ? 3 : bw >= 60 ? 2 : bw >= 30 ? 1 : 0;')
open(dst, "w", encoding="utf-8").write(s)
print("ok daily tiers")

# --- Nachtrag (Martin 15:33, Simulation-Vorschläge alle ok): Balancing ---
s = open(dst, encoding="utf-8").read()
# 1 Unkraut im Ring: −3 Leben + Unkraut verdorrt (Game over nur, wenn die Leben ausgehen)
rep('if (ny <= 0 && !S.over) { w.growT = 0; try { fxText(w.x, 1, "WEEDS TOOK THE RING", "#ff6fb5"); } catch (e) {} gameOver("Weeds reached the ring."); }',
    'if (ny <= 0 && !S.over) { w.growT = 0; D.weeds = D.weeds.filter(q => q !== w); S.lives = Math.max(0, (S.lives || 0) - 3); try { fxText(w.x, 1, "WEED HIT THE RING · −3 ♥", "#ff6fb5"); snd("leak"); announce("WEED HIT THE RING", "−3 lives · the weed withers", "ALERT", 2600); hud(); } catch (e) {} if (S.lives <= 0) gameOver("Weeds reached the ring."); }   /* V456: −3 Leben statt Game over (Martin 08.11. 15:33) */')
# 2 Unkraut-Wellen entzerren: W131 → W136
rep('if (k === "weed") return [81, 106, 126, 131].includes(w)', 'if (k === "weed") return [81, 106, 126, 136].includes(w)')
rep('const WEEDN = { 106: 3, 126: 4, 131: 5 };', 'const WEEDN = { 106: 3, 126: 4, 136: 5 };')
rep('weed5: 131, elite: 6, peek: 3, nuts: 31,', 'weed5: 136, elite: 6, peek: 3, nuts: 31,')
# 3 Monster ab W61 stufenweise stärker: HP ×0,4 → Asien ×0,55, Nordamerika ×0,7 (Antarktis bleibt ×0,4)
rep('(!S.nuts && w >= 21 && w <= 150 ? 0.4 : 1) * baseHp', '(!S.nuts && w >= 21 && w <= 150 ? (w >= 91 && w <= 120 ? 0.7 : w >= 61 && w <= 90 ? 0.55 : 0.4) : 1) * baseHp')
# 4 W1–4: Steine 10 % langsamer
rep('const g = Math.max(G.gravMin, G.gravBase - le * G.gravLine - we * G.gravWave) * ordv("gravMul") * (!S.nuts && S.wave >= 21 && S.wave <= 150 ? 1.8 : 1)',
    'const g = Math.max(G.gravMin, G.gravBase - le * G.gravLine - we * G.gravWave) * ordv("gravMul") * (!S.nuts && S.wave >= 21 && S.wave <= 150 ? 1.8 : 1) * (!S.nuts && S.wave <= 4 ? 1.1 : 1)')
open(dst, "w", encoding="utf-8").write(s)
print("ok balancing")
