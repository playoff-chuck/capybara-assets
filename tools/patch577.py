#!/usr/bin/env python3
# V577 (Martin 11.11. 00:21–00:27):
# - Werbefenster (RU): Kauf-Knopf «ХОЧУ! · 350 🪙 ▶» bleibt eine Zeile (Münze inline, Schrift passt sich an),
#   «ТОЛЬКО ЭТА ВОЛНА!» überlappt den Titel nicht mehr, «−100%» wird nicht mehr abgeschnitten
# - Blu: in Welle 1–10 30 % weniger Sprüche (Kurs-Lob ausgenommen)
# - Tutorial: neuer Block startet ganz oben am Bildschirm und fliegt über Streifen und Karte ins Feld
import sys
src, dst = sys.argv[1], sys.argv[2]
s = open(src, encoding="utf-8").read()
def rep(a, b, n=1):
    global s
    c = s.count(a); assert c == n, (c, a[:90]); s = s.replace(a, b)
rep('const GAME_VER = "V576";', 'const GAME_VER = "V577";')

# Blu −30 % in W1–10
rep('  function rbSay(key, delay = 0, force = false) {\n',
    '  function rbSay(key, delay = 0, force = false) {\n    try { if (!force && S && (S.wave | 0) <= 10 && Math.random() < 0.3) return; } catch (e) {}   /* V577: W1–10 30 % weniger */\n')

# Einflug des Blocks von ganz oben (Tutorial)
rep('''    const card = coach.querySelector(".coachCard"), cr = card && card.getBoundingClientRect(); if (!cr || !cr.width) return;
    const r = cv.getBoundingClientRect(), sx = cv.width / r.width, sy = cv.height / r.height, p = S.piece;''',
    '''    const card = coach.querySelector(".coachCard"), cr = card && card.getBoundingClientRect(); if (!cr || !cr.width) return;
    const r = cv.getBoundingClientRect(), sx = cv.width / r.width, sy = cv.height / r.height, p = S.piece;
    const now = performance.now(); if (p !== EN.p) { EN.p = p; EN.t = now; let top = 1e9, cs = 20; for (const [x, y] of p.cells) { const [gx, gy] = v2g(p.x + x, p.y + y); const q = cvPt(gx, gy); top = Math.min(top, q.y); cs = q.cs || cs; } EN.d = Math.max(0, top + cs); let gi = 0.8; try { gi = gravityInterval(); } catch (e) {} EN.ms = Math.min(1400, Math.max(500, EN.d / cs * gi * 1000)); }   /* V577: Einflug von ganz oben */
    const k = Math.min(1, (now - EN.t) / EN.ms), off = -EN.d * (1 - k);''')
rep('''      if (x0 + w < cr.left || x0 > cr.right || y0 + h < cr.top || y0 > cr.bottom) continue;   // nur dort, wo die Karte drüberliegt
      ox.drawImage(cv, (x0 - r.left) * sx, (y0 - r.top) * sy, w * sx, h * sy, x0 * dpr, y0 * dpr, w * dpr, h * dpr); }''',
    '''      if (k >= 1 && (x0 + w < cr.left || x0 > cr.right || y0 + h < cr.top || y0 > cr.bottom)) continue;   // nach dem Einflug nur dort, wo die Karte drüberliegt
      ox.drawImage(cv, (x0 - r.left) * sx, (y0 - r.top) * sy, w * sx, h * sy, x0 * dpr, (y0 + off) * dpr, w * dpr, h * dpr); }''')
rep('const oc = document.createElement("canvas"); oc.id = "tutPieceCv";', 'const EN = { p: null, t: 0, d: 0, ms: 600 }; const oc = document.createElement("canvas"); oc.id = "tutPieceCv";')

CSS = '''<style id="v577">
#adBuy{display:flex!important;flex-direction:row!important;align-items:center;justify-content:center;gap:6px;flex-wrap:nowrap;line-height:1!important;padding:0 10px!important;font-size:min(19px,5.2vw)!important;overflow:hidden}
.adCard.sale #adBuy{font-size:min(21px,5.6vw)!important}
#adBuy *{display:inline-block!important;vertical-align:middle;margin:0!important;line-height:1!important;position:static!important;flex:0 0 auto}
#adBuy img,#adBuy .coin,#adBuy i,#adBuy svg{width:1.05em!important;height:1.05em!important}
.adCard.sale .saleHead{margin:-2px 0 8px!important}
.adCard.sale #adName{margin-top:2px!important}
.adCard.sale .salePrice{display:flex;flex-wrap:wrap;align-items:center;justify-content:center;gap:4px 8px;max-width:100%;padding:0 4px;box-sizing:border-box}
.adCard.sale .salePrice>*{flex:0 0 auto;max-width:100%}
.adCard .adBody{overflow:hidden}
</style>
'''
rep("</body>", CSS + "</body>")
open(dst, "w", encoding="utf-8").write(s)
print("ok")
