#!/usr/bin/env python3
"""V441: Reichweite durchs Turm-Menü sehen – Waffe gedrückt halten: Menü wird fast durchsichtig,
Kreis in Waffenfarbe (gestrichelt) zeigt die Reichweite auf dem Feld; kurzer Tipp = kaufen wie bisher,
langes Halten kauft nicht. Testlink ?test=peek (Welle 3). (Martin 08.11. 11:48)
Nutzung: python3 tools/patch441.py src dst"""
import sys
src, dst = sys.argv[1], sys.argv[2]
s = open(src, encoding="utf-8").read()

def rep(a, b, n=1):
    global s
    c = s.count(a)
    assert c == n, (c, a[:80])
    s = s.replace(a, b)

rep('GAME_VER = "V440"', 'GAME_VER = "V441"')

# CSS
rep('.sheetIn{max-width:568px;margin:0 auto;display:flex;flex-direction:column;gap:10px}',
    '.sheetIn{max-width:568px;margin:0 auto;display:flex;flex-direction:column;gap:10px}\n'
    '.sheet{transition:opacity .18s}.sheet.peek{opacity:.14}\n'
    '.peekTip{font-size:12px;color:var(--muted);margin:-4px 0 0;text-align:center;letter-spacing:.02em}')

# Tipp im Menü (nur wenn Waffen zu kaufen/aufzurüsten sind)
rep('  $("sheetIn").innerHTML = h;\n}\n$("sheet").addEventListener("click", e => {',
    '  if (/data-buy=|data-up=/.test(h)) h = h.replace(\'</div>\', \'</div><div class="peekTip">👁 Hold a weapon to see its range</div>\');   /* V441 */\n'
    '  $("sheetIn").innerHTML = h;\n}\n$("sheet").addEventListener("click", e => {')

# Zeichnen: Vorschau-Kreis in Waffenfarbe
rep('''  if (S.sel) {
    const r = Math.max(0, ...S.sel.w.map(w => wstat(w).range), 0) + (S.sel.w.length ? heightBonus(S.sel) : 0);
    if (r) { ctx.fillStyle = "rgba(238,122,44,.1)"; ctx.strokeStyle = "rgba(238,122,44,.7)"; ctx.lineWidth = 1.5 * DPR; ctx.beginPath(); ctx.arc(C(S.sel.x), C(S.sel.y), r * s, 0, 7); ctx.fill(); ctx.stroke(); }
  }''',
'''  if (S.sel) {
    const pk = S.peek;   /* V441: gehaltene Waffe im Menü → ihre Reichweite */
    const r = pk ? wstat({ type: pk.type, lvl: pk.lvl }).range + heightBonus(S.sel) : Math.max(0, ...S.sel.w.map(w => wstat(w).range), 0) + (S.sel.w.length ? heightBonus(S.sel) : 0);
    if (r) { const hx = pk ? WEAP[pk.type].col : "#ee7a2c", rgb = `${parseInt(hx.slice(1, 3), 16)},${parseInt(hx.slice(3, 5), 16)},${parseInt(hx.slice(5, 7), 16)}`;
      ctx.fillStyle = `rgba(${rgb},${pk ? .18 : .1})`; ctx.strokeStyle = `rgba(${rgb},${pk ? .95 : .7})`; ctx.lineWidth = (pk ? 3 : 1.5) * DPR; if (pk) ctx.setLineDash([9 * DPR, 7 * DPR]);
      ctx.beginPath(); ctx.arc(C(S.sel.x), C(S.sel.y), r * s, 0, 7); ctx.fill(); ctx.stroke(); ctx.setLineDash([]);
      if (pk) { ctx.font = `${Math.round(14 * DPR)}px Bangers, Impact, sans-serif`; ctx.textAlign = "center"; ctx.lineWidth = 4 * DPR; ctx.strokeStyle = "rgba(0,0,0,.55)"; ctx.fillStyle = hx; const tx = `${WEAP[pk.type].name.toUpperCase()} L${pk.lvl} · RANGE ${r.toFixed(1)}`, ty = C(S.sel.y) - r * s - 8 * DPR; ctx.strokeText(tx, C(S.sel.x), ty); ctx.fillText(tx, C(S.sel.x), ty); } }
  }''')

# Halten = schauen, Tippen = kaufen
rep('const SNIPE_COST = 200, MIX_COST = 350, TESLA_COST = 500, WOLF_COST = 500, WOLF_W = 100;',
'''/* V441: Reichweite durchs Menü sehen – Waffe/Upgrade gedrückt halten */
try { (() => { const sh = $("sheet"); let held = false, tm = 0;
  const end = () => { sh.classList.remove("peek"); if (S) S.peek = null; };
  sh.addEventListener("pointerdown", e => { const b = e.target.closest("button[data-buy],button[data-up],.wline"); if (!b || !S || !S.sel) return;
    let type, lvl; if (b.dataset.buy) { type = b.dataset.buy; lvl = 1; }
    else { const slot = b.closest(".slot"), i = b.dataset.up != null ? +b.dataset.up : [...sh.querySelectorAll(".slot")].indexOf(slot); const w = S.sel.w[i]; if (!w) return; type = w.type; lvl = b.dataset.up != null ? Math.min(maxLvl(), w.lvl + 1) : w.lvl; }
    S.peek = { type, lvl }; held = false; sh.classList.add("peek"); clearTimeout(tm); tm = setTimeout(() => { held = true; }, 320); }, { passive: true });
  ["pointerup", "pointercancel"].forEach(ev => sh.addEventListener(ev, () => { clearTimeout(tm); if (held) window.__peekSwallow = performance.now() + 500; held = false; end(); }));
  sh.addEventListener("click", e => { if (window.__peekSwallow && performance.now() < window.__peekSwallow && e.target.closest("button[data-buy],button[data-up]")) { window.__peekSwallow = 0; e.stopImmediatePropagation(); e.preventDefault(); } }, true);
  const _cs = closeSheet; closeSheet = function () { end(); return _cs.apply(this, arguments); };
})(); } catch (e) { console.error("v441", e); }
const SNIPE_COST = 200, MIX_COST = 350, TESLA_COST = 500, WOLF_COST = 500, WOLF_W = 100;''')

# Testlink
rep('weed5: 131, elite: 6, thief: 100', 'weed5: 131, elite: 6, peek: 3, thief: 100')

open(dst, "w", encoding="utf-8").write(s)
print("ok", dst)
