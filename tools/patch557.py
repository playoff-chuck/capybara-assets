#!/usr/bin/env python3
# V557: Goldmünze statt Wort «золота» (Martin 10.11. 15:10/15:16). RU-Texte tragen das Zeichen U+E000 (tools/lang_src/ru_v557.json),
# i18nText ersetzt es durch <img class="coinI" src="img/coin64.webp"> (Münze groß gezeichnet: tools/coin557.svg, verkleinert auf 64 px).
# Auf Canvas (Hack-Duell u. a.) wird das Zeichen zu «🪙».
import sys
src, dst = sys.argv[1], sys.argv[2]
s = open(src, encoding="utf-8").read()
def rep(a, b, n=1):
    global s
    c = s.count(a); assert c == n, (c, a[:80]); s = s.replace(a, b)
rep('const GAME_VER = "V556";', 'const GAME_VER = "V557";')
rep('''const out = T(src); i18nDone.set(n, { src, out, lang: I18N.lang }); if (out !== d) n.data = out; }''',
    '''const out = T(src); i18nDone.set(n, { src, out, lang: I18N.lang }); if (out !== d) n.data = out; if (out.indexOf("\\uE000") >= 0) queueMicrotask(() => { if (n.parentNode && n.data === out) i18nCoin(n, out); }); }   /* erst nach dem Durchlauf tauschen, sonst bricht der TreeWalker ab */
function i18nCoin(n, out) {   /* V557: Münz-Zeichen → Bild */
  const p = n.parentNode; if (!p) return; const f = document.createDocumentFragment(); const parts = out.split("\\uE000");
  parts.forEach((t, i) => { if (t) { const tn = document.createTextNode(t); i18nDone.set(tn, { src: t, out: t, lang: I18N.lang }); f.appendChild(tn); }
    if (i < parts.length - 1) { const im = document.createElement("img"); im.className = "coinI"; im.src = "img/coin64.webp"; im.alt = "🪙"; im.draggable = false; f.appendChild(im); } });
  p.replaceChild(f, n); }''')
rep('''P.fillText = function (t) { arguments[0] = T(t); return ft.apply(this, arguments); }; P.strokeText = function (t) { arguments[0] = T(t); return st.apply(this, arguments); }; P.measureText = function (t) { return mt.call(this, T(t)); };''',
    '''const TC = t => { const v = T(t); return typeof v === "string" && v.indexOf("\\uE000") >= 0 ? v.replace(/\\uE000/g, "🪙") : v; };   /* V557 */
  P.fillText = function (t) { arguments[0] = TC(t); return ft.apply(this, arguments); }; P.strokeText = function (t) { arguments[0] = TC(t); return st.apply(this, arguments); }; P.measureText = function (t) { return mt.call(this, TC(t)); };''')
rep('#ovMap{position:fixed;inset:0;z-index:990;', '''img.coinI{display:inline-block!important;width:1.15em!important;height:1.15em!important;max-width:none!important;vertical-align:-.22em!important;margin:0 .04em 0 .08em!important;padding:0!important;border:0!important;background:none!important;filter:drop-shadow(0 1px 0 rgba(58,36,20,.35));pointer-events:none}
html[lang=ru] #sheet #sheetIn .shopTiles .shopItem button .lbl{font-size:13px!important;letter-spacing:.02em!important}
html[lang=ru] #sheet #sheetIn .shopTiles .shopItem button{min-height:42px!important}
#sheetIn .slotRow button small img.coinI{width:1.25em!important;height:1.25em!important}
#ovMap{position:fixed;inset:0;z-index:990;''')
open(dst, "w", encoding="utf-8").write(s)
print("ok")
