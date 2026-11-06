"""V318 (Martin 06.11. 12:57/12:58 + Testlauf-Kleinigkeiten, Martin «ok» 10:00):
1. Boss-Einsatz ohne Casino-Optik: statt Goldmünzen-Bild abwechselnd die 3 Essens-Bilder (Wassermelonen /
   Mais-Äpfel-Orangen / Gras-Salat-Zuckerrohr-Karotten) – «Alle 3 Bilder verwenden. Top».
2. Wild Cards nie am Kontinent-Ende, mindestens ~3 min vorher: Wellen 20, 40, 56, 80, 100, 116, 140
   (statt 60 und 120, die direkt auf Kontinentwechsel fielen). Dauer-Text zeigt die nächste Wild-Card-Welle.
3. Kein Ten-ton-Sale, wenn in den nächsten 3 Wellen ein Gratis-Ten-ton (Air-Drop W8/14/22) kommt.
4. Sprechblasen warten auch während Boss-Hack-Einsatz/Duell (uiWinOpen kennt jetzt #ovHack und S.duel/S.hackAdOpen).
5. Erstes-Mal-Hinweise warten, solange ein Fenster/Anzeige offen ist (nie zusammen mit einer Anzeige).
Aufruf: python3 tools/patch318.py src dst   (kopiert review/v313/food_*.webp als site/img/<hash>.webp)"""
import sys, hashlib, shutil, os
src, dst = sys.argv[1], sys.argv[2]
s = open(src, encoding='utf-8').read()
def rep(a, b, cnt=1):
    global s
    n = s.count(a); assert n == cnt, (n, a[:70]); s = s.replace(a, b)

root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
imgs = []
for k in 'ABC':
    b = open(os.path.join(root, f'review/v313/food_{k}.webp'), 'rb').read()
    name = 'img/' + hashlib.sha256(b).hexdigest()[:10] + '.webp'
    shutil.copyfile(os.path.join(root, f'review/v313/food_{k}.webp'), os.path.join(root, 'site', name))
    imgs.append(name)

rep('const GAME_VER = "V317";', 'const GAME_VER = "V318";')
# 1) Essens-Bilder
rep('background:url(img/hk_bet.webp) center/cover;', f'background:url({imgs[0]}) center/cover;')
JS = r'''
/* V318: Boss-Einsatz-Bild wechselt zwischen 3 Essens-Bildern (keine Goldmünzen) */
try { (() => { const IM = __IMGS__, ov = document.getElementById("ovHack"); if (!ov) return; let was = false;
  new MutationObserver(() => { const on = !ov.hidden; if (on && !was) { let i = 0; try { i = (+localStorage.getItem("capy-betpic") || 0) % IM.length; localStorage.setItem("capy-betpic", String(i + 1)); } catch (e) {}
      const p = ov.querySelector(".hkBetPic"); if (p) p.style.backgroundImage = `url(${IM[i]})`; } was = on; }).observe(ov, { attributes: true, attributeFilter: ["hidden"] }); })(); } catch (e) { console.error("v318 bet", e); }
'''.replace('__IMGS__', '[' + ', '.join(f'"{x}"' for x in imgs) + ']')
# 2) Wild-Card-Wellen
rep('if (S.wave % 20 === 0 && S.wave >= 20) { S.ordDue = S.wave;', 'if (ORD_W.includes(S.wave)) { S.ordDue = S.wave;')
rep('function joined() {', 'const ORD_W = [20, 40, 56, 80, 100, 116, 140];   /* V318: Wild Cards nie am Kontinent-Ende (≥ 3 min vorher) */\n'
    'window.__ordNext = w => { const n = ORD_W.find(x => x > w); return n || 150; };\nfunction joined() {')
rep('<b>it lasts 20 waves – until wave ${S.wave + 20}</b>', '<b>it lasts until wave ${window.__ordNext(S.wave)}</b>')
rep('`WILD CARD · UNTIL WAVE ${(S.wave || 0) + 20}`', '`WILD CARD · UNTIL WAVE ${window.__ordNext(S.wave || 0)}`')
# 3) kein Ten-ton-Sale vor Gratis-Ten-ton
rep('if (S.adDue[k] && !why(k)) {',
    'if (S.adDue[k] && !why(k) && !(k === "ton" && [8, 14, 22].some(w => w >= (S.wave || 0) && w <= (S.wave || 0) + 3 && !(S.tonGift || {})[w]))) {')
# 4) Sprechblasen warten auch bei Boss-Einsatz/Duell
rep('return v("ovIntro") || document.body.classList.contains("introWin") || v("ovAd")',
    'return v("ovIntro") || v("ovHack") || !!(S && (S.duel || S.hackAdOpen)) || document.body.classList.contains("introWin") || v("ovAd")')
# 5) Erstes-Mal-Hinweise nie zusammen mit Fenster/Anzeige
rep('if (TUT.on || LS.get("tarnturm-hint-" + key) === "1" || hintKey) return;',
    'if (TUT.on || LS.get("tarnturm-hint-" + key) === "1" || hintKey) return;\n'
    '  try { if (uiWinOpen() || (S && (S.ordersOpen || S.mapShow || S.drop || S.paused))) { setTimeout(() => hint(key, title, sub, at), 1500); return; } } catch (e) {}   /* V318 */')
anchor = '})();\n</script>'
p = s.rindex(anchor); s = s[:p] + JS + s[p:]
open(dst, 'w', encoding='utf-8').write(s)
print("ok", imgs)
