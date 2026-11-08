#!/usr/bin/env python3
"""V457 (Martin 08.11. 15:55/15:57):
- Nuts-Musik: 5 Suno-Stücke (music/nz_*.mp4, −19 LUFS): je Kontinent sein Stück + «Nuts Detour» als zweites; DJ-Anzeige mit Namen/BPM.
- Flaggen-Auswahl auch im Zahnrad-Menü (Sprache live wechseln; Texte werden aus dem englischen Original neu übersetzt).
Nutzung: python3 tools/patch457.py src dst"""
import sys
src, dst = sys.argv[1], sys.argv[2]
s = open(src, encoding="utf-8").read()

def rep(a, b, n=1):
    global s
    c = s.count(a)
    assert c == n, (c, a[:80])
    s = s.replace(a, b)

rep('const GAME_VER = "V456";', 'const GAME_VER = "V457";')

# --- Nuts-Musik ---
rep('const TRK_ORDER = ["andes", "jungle", "copacabana", "rumba", "samba", "loungedisco", "chilldisco", "airport"];',
    'const TRK_ORDER = ["andes", "jungle", "copacabana", "rumba", "samba", "loungedisco", "chilldisco", "airport"];\n'
    'const TRK_NZ = ["skullgrog", "gorkazar", "frostgnaw", "grumblefang"], TRK_NZ_ALL = "nutsanthem";   /* V457: Nuts-Musik je Kontinent + Anthem */')
rep('function trkPool(wave) { if (!wave) return ["airport"]; const p = Math.floor(((wave - 1) % 30) / 5);',
    'function trkPool(wave) { if (!wave) return ["airport"]; try { if (typeof S !== "undefined" && S && S.nuts) return [TRK_NZ[S.nuts.c] || TRK_NZ[0], TRK_NZ_ALL]; } catch (e) {}   /* V457 */ const p = Math.floor(((wave - 1) % 30) / 5);')
rep('const TRK_FILE = { airport: "airport_bossa",', 'const TRK_FILE = { skullgrog: "nz_skullgrog", gorkazar: "nz_gorkazar", frostgnaw: "nz_frostgnaw", grumblefang: "nz_grumblefang", nutsanthem: "nz_anthem", airport: "airport_bossa",')
rep('const TRK = { airport: ["Airport Bossa", 100],', 'const TRK = { skullgrog: ["Skullgrog Rush", 170], gorkazar: ["Gorkazar Groove", 132], frostgnaw: ["Frostgnaw Sprint", 150], grumblefang: ["Grumblefang Stampede", 160], nutsanthem: ["Nuts Detour", 145], airport: ["Airport Bossa", 100],')
# Beim Start des Abstechers und bei der Rückkehr Musik neu wählen (Pool hängt jetzt von S.nuts ab)
rep('  try { SFX.music.start(S.wave); } catch (e) {}\n  announce("NUTS DETOUR!"', '  try { TP.key = null; SFX.music.start(S.wave); } catch (e) {}   /* V457: Nuts-Musik */\n  announce("NUTS DETOUR!"')

# --- Sprachschicht: Original merken, damit ein Wechsel im laufenden Spiel neu übersetzt ---
rep('function i18nText(n) { const d = n.data; if (!d || !d.trim()) return; const p = n.parentNode; if (!p || I18N_SKIP.has(p.nodeName)) return; const m = i18nDone.get(n); if (m && m.out === d) return; const out = T(d); i18nDone.set(n, { out }); if (out !== d) n.data = out; }',
    'function i18nText(n) { const d = n.data; if (!d || !d.trim()) return; const p = n.parentNode; if (!p || I18N_SKIP.has(p.nodeName)) return; const m = i18nDone.get(n); if (m && m.out === d && m.lang === I18N.lang) return; const src = (m && m.out === d) ? m.src : d; const out = T(src); i18nDone.set(n, { src, out, lang: I18N.lang }); if (out !== d) n.data = out; }   /* V457: Original merken */')
rep('''function i18nEl(el) { if (!el || el.nodeType !== 1 || I18N_SKIP.has(el.nodeName)) return; for (const a of I18N_ATTR) { if (el.hasAttribute(a)) { const v = el.getAttribute(a), k = "a:" + a, m = i18nDone.get(el) || {}; if (m[k] === v) continue; const o = T(v); m[k] = o; i18nDone.set(el, m); if (o !== v) el.setAttribute(a, o); } }
  const w = document.createTreeWalker(el, NodeFilter.SHOW_TEXT | NodeFilter.SHOW_ELEMENT, null); let n; while ((n = w.nextNode())) { if (n.nodeType === 3) i18nText(n); else if (n.nodeType === 1 && !I18N_SKIP.has(n.nodeName)) { for (const a of I18N_ATTR) if (n.hasAttribute(a)) { const v = n.getAttribute(a), k = "a:" + a, m = i18nDone.get(n) || {}; if (m[k] === v) continue; const o = T(v); m[k] = o; i18nDone.set(n, m); if (o !== v) n.setAttribute(a, o); } } } }''',
'''function i18nAttr(el, a) { const v = el.getAttribute(a), k = "a:" + a, m = i18nDone.get(el) || {}; if (m[k] === v && m[k + ":l"] === I18N.lang) return; const src = m[k] === v ? m[k + ":s"] : v; const o = T(src); m[k] = o; m[k + ":s"] = src; m[k + ":l"] = I18N.lang; i18nDone.set(el, m); if (o !== v) el.setAttribute(a, o); }
function i18nEl(el) { if (!el || el.nodeType !== 1 || I18N_SKIP.has(el.nodeName)) return; for (const a of I18N_ATTR) if (el.hasAttribute(a)) i18nAttr(el, a);
  const w = document.createTreeWalker(el, NodeFilter.SHOW_TEXT | NodeFilter.SHOW_ELEMENT, null); let n; while ((n = w.nextNode())) { if (n.nodeType === 3) i18nText(n); else if (n.nodeType === 1 && !I18N_SKIP.has(n.nodeName)) { for (const a of I18N_ATTR) if (n.hasAttribute(a)) i18nAttr(n, a); } } }''')

# --- Flaggen im Zahnrad-Menü ---
rep('<div class="setRow"><button id="setCloud" class="btn-small" type="button">☁ Cloud save</button><button id="setGuide" class="btn-small" type="button">Guide</button></div>',
    '<div class="setRow"><button id="setCloud" class="btn-small" type="button">☁ Cloud save</button><button id="setGuide" class="btn-small" type="button">Guide</button></div><div class="setLang" id="setLang" aria-label="Language"></div>')
rep('window.__i18n = { get lang() { return I18N.lang; },',
    '''function i18nSetRow() { const box = document.getElementById("setLang"); if (!box) return; box.innerHTML = Object.entries(LANGS).map(([k, v]) => `<button type="button" data-lang="${k}" class="${k === I18N.lang ? "on" : ""}" title="${v.name}"><span>${v.flag}</span></button>`).join("");
  if (!box.__wired) { box.__wired = true; box.addEventListener("click", e => { const b = e.target.closest("[data-lang]"); if (!b) return; e.stopPropagation(); try { SFX.init(); snd("uiTap"); } catch (er) {} i18nLoad(b.dataset.lang, () => { i18nSetRow(); try { renderModes(); } catch (er) {} }); i18nSetRow(); }); }
  try { new MutationObserver(() => { const ov = document.getElementById("ovSettings"); if (ov && !ov.hidden) i18nSetRow(); }).observe(document.getElementById("ovSettings"), { attributes: true, attributeFilter: ["hidden"] }); } catch (e) {} }
try { i18nSetRow(); } catch (e) {}   /* V457: Flaggen im Zahnrad-Menü */
window.__i18n = { get lang() { return I18N.lang; },''')
rep('#splash.pick .spGo,#splash.pick .spDots{visibility:hidden}',
    '#splash.pick .spGo,#splash.pick .spDots{visibility:hidden}\n'
    '#ovSettings .setLang{display:flex;gap:6px;justify-content:center;flex-wrap:wrap;margin-top:8px}#ovSettings .setLang button{min-height:0;height:40px;padding:0 8px;border:3px solid #3a2414;border-radius:12px;background:#fff!important;background-image:none!important;box-shadow:0 2px 0 #3a2414;font-size:20px;line-height:1;letter-spacing:1px;opacity:.55}#ovSettings .setLang button.on{opacity:1;background:#ffe6a8!important;transform:translateY(1px);box-shadow:0 1px 0 #3a2414}')

open(dst, "w", encoding="utf-8").write(s)
print("ok", dst)

# --- Nachtrag (Martin 15:58): Monster-Rabatt ab W21 zurücknehmen, früher Druck ---
s = open(dst, encoding="utf-8").read()
# HP: Südamerika W21–30 ×0,7 · Afrika ×0,6 · Asien ×0,55 · Nordamerika ×0,7 · Antarktis ×0,4 (unverändert)
rep('(!S.nuts && w >= 21 && w <= 150 ? (w >= 91 && w <= 120 ? 0.7 : w >= 61 && w <= 90 ? 0.55 : 0.4) : 1) * baseHp',
    '(!S.nuts && w >= 21 && w <= 150 ? (w <= 30 ? 0.7 : w <= 60 ? 0.6 : w <= 90 ? 0.55 : w <= 120 ? 0.7 : 0.4) : 1) * baseHp')
# Tempo: Südamerika W21–30 ×0,85 · Afrika ×0,8 · danach ×0,65 wie bisher
rep('const sp = ordv("monSpdMul") * (!S.nuts && w >= 21 && w <= 150 ? 0.65 : 1)',
    'const sp = ordv("monSpdMul") * (!S.nuts && w >= 21 && w <= 150 ? (w <= 30 ? 0.85 : w <= 60 ? 0.8 : 0.65) : 1)')
# Anzahl: ab W10 ein Monster mehr je Welle
rep('S.toSpawn = Math.max(1, Math.round(Math.min(L.monsters, G.waveBase + G.wavePer * S.wave) * (!S.nuts && S.wave >= 21 && S.wave <= 150 ? 0.55 : 1)));',
    'S.toSpawn = Math.max(1, Math.round(Math.min(L.monsters, G.waveBase + G.wavePer * S.wave) * (!S.nuts && S.wave >= 21 && S.wave <= 150 ? 0.55 : 1)) + (!S.nuts && S.wave >= 10 ? 1 : 0));   /* V457: ab W10 +1 Monster */')
open(dst, "w", encoding="utf-8").write(s)
print("ok pressure")
