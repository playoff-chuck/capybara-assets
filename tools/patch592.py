#!/usr/bin/env python3
# V592 (Martin 11.11. 02:06, Tutorial-Video): Aufräumen
# - «Falsche Pixel»: der Einflug von oben kopierte manchmal leere Feldstücke (Block war noch nicht gezeichnet) →
#   der einfliegende Stein wird jetzt selbst gemalt (gleiches Muster wie im Feld, TNT inklusive), nie mehr leere Kacheln
# - Wenn das Tutorial das Spiel anhält (Lektionen mit Wartezeit), wird der stehende Stein nicht über die Karte gemalt – Text bleibt lesbar
# - Buchhalter: zählte die +1000 Urkunden-Punkte mitten im Hochzählen («505»). Seine Meldung zählt jetzt nur echte Spielpunkte
#   (Wellen × Linien × Splats) – so wie er es auch ansagt
# - Laden im Tutorial: öffnet immer oben (Turm-Knopf sichtbar, vorher blieb er nach dem Sniper unten stehen);
#   Major Ledger (Buchhalter-Kopf mit Sprechblase) im Laden bis zur Urkunde ausgeblendet
import sys
src, dst = sys.argv[1], sys.argv[2]
s = open(src, encoding="utf-8").read()
def rep(a, b, n=1):
    global s
    c = s.count(a); assert c == n, (c, a[:90]); s = s.replace(a, b)
rep('const GAME_VER = "V591";', 'const GAME_VER = "V592";')

# 1) Einflug: Zellen selbst malen
rep('''      for (const [x, y] of p.cells) { const [gx, gy] = v2g(p.x + x, p.y + y); if (gy < 0) continue;
        const a = cvPt(gx, gy), b = cvPt(gx + 1, gy + 1), x0 = Math.min(a.x, b.x), y0 = Math.min(a.y, b.y), w = Math.abs(b.x - a.x), h = Math.abs(b.y - a.y);
        const im = document.createElement("canvas"); im.width = Math.max(1, Math.round(w * sx)); im.height = Math.max(1, Math.round(h * sy)); im.getContext("2d").drawImage(cv, (x0 - r.left) * sx, (y0 - r.top) * sy, w * sx, h * sy, 0, 0, im.width, im.height);
        EN.c.push({ im, x0, y0, w, h }); bot = Math.max(bot, y0 + h); cs = Math.max(cs, h); }''',
'''      p.cells.forEach(([x, y], i) => { const [gx, gy] = v2g(p.x + x, p.y + y);
        const a = cvPt(gx, gy), b = cvPt(gx + 1, gy + 1), x0 = Math.min(a.x, b.x), y0 = Math.min(a.y, b.y), w = Math.abs(b.x - a.x), h = Math.abs(b.y - a.y);
        const im = document.createElement("canvas"), S2 = CELL; im.width = im.height = Math.max(1, Math.round(S2)); const g = im.getContext("2d");   /* V592: selbst malen statt kopieren */
        try { if (i === p.tnt) tntCell(0, 0, g, S2, 0, 0); else { g.fillStyle = patterns[p.col] || "#555"; g.fillRect(0, 0, S2, S2); const e = Math.max(1, S2 * 0.12);
          g.fillStyle = "rgba(255,248,220,.22)"; g.fillRect(0, 0, S2, e); g.fillRect(0, 0, e, S2); g.fillStyle = "rgba(0,0,0,.38)"; g.fillRect(0, S2 - e, S2, e); g.fillRect(S2 - e, 0, e, S2);
          g.strokeStyle = "rgba(10,14,8,.8)"; g.lineWidth = Math.max(1, S2 * 0.04); g.strokeRect(0.5, 0.5, S2 - 1, S2 - 1); } } catch (er) {}
        EN.c.push({ im, x0, y0, w, h }); bot = Math.max(bot, y0 + h); cs = Math.max(cs, h); });''')
# 2) bei angehaltenem Tutorial nicht über die Karte malen
rep('      if (!dimNow && !over(x0, y0, w, h, cr) && !over(x0, y0, w, h, br)) continue;',
    '      if (S.coachHold && over(x0, y0, w, h, cr)) continue;   /* V592: Karte lesbar, solange das Spiel steht */\n      if (!dimNow && !over(x0, y0, w, h, cr) && !over(x0, y0, w, h, br)) continue;')
# 3) Buchhalter nur echte Spielpunkte
rep('''  const sc = calcScore(); S.score = sc;
  for (const m of SCORE_MARKS) if (sc >= m && (S.scoreMark || 0) < m) { S.scoreMark = m; bookkeeper(sc, m); break; }''',
'''  const sc = calcScore(); S.score = sc; const base = Math.max(0, sc - (S.bonusPts | 0));   /* V592: Urkunden-Bonus zählt nicht für den Buchhalter */
  for (const m of SCORE_MARKS) if (base >= m && (S.scoreMark || 0) < m) { S.scoreMark = m; bookkeeper(base, m); break; }''')
# 4) Laden im Tutorial oben öffnen, Ledger aus
rep('function openShop() { S.lsay = ((S.lsay || 0) + 1 + Math.floor(Math.random() * 9)) % 10; S.sel = null; S.shop = true; renderShop(); $("sheet").hidden = false; }',
    'function openShop() { S.lsay = ((S.lsay || 0) + 1 + Math.floor(Math.random() * 9)) % 10; S.sel = null; S.shop = true; renderShop(); $("sheet").hidden = false; try { if (TUT.on && (TUT_STEPS[TUT.step] || {}).ar !== "spec") { const top0 = () => document.querySelectorAll("#sheet .shopTiles, #sheetIn").forEach(e => { e.scrollTop = 0; }); top0(); requestAnimationFrame(top0); } } catch (e) {} }   /* V592: im Tutorial oben öffnen */')

# Turm-Knopf im offenen Laden ins Bild holen (nach dem Sniper blieb der Laden unten stehen)
rep("""        const place = () => document.querySelector('#sheet button[data-shop="tower"]');""",
    """        const place = () => { const b = document.querySelector('#sheet button[data-shop="tower"]'); try { if (b) { const q = b.getBoundingClientRect(), sc = b.closest(".shopTiles"), z = sc ? sc.getBoundingClientRect() : { top: 70, bottom: innerHeight - 70 }; if (q.height && (q.top < z.top + 6 || q.bottom > z.bottom - 6)) b.scrollIntoView({ block: "center" }); } } catch (e) {} return b; };   /* V592 */""")
rep('/* V584: neue Aufgabe', 'setInterval(() => { try { document.body.classList.toggle("tutRun", !!(typeof TUT !== "undefined" && TUT.on)); } catch (e) {} }, 300);   /* V592: Markierung fürs CSS */\n/* V584: neue Aufgabe')
CSS = """<style id="v592">
body.tutRun .ledgerTop{display:none!important}
</style>
"""
rep('</body>', CSS + '</body>')
open(dst, "w", encoding="utf-8").write(s)
print("ok V592")
