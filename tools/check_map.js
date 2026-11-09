// Grafik-Prüfung Weltkarte mit Spielfortschritt (Nuts-Bestwerte): kein Schild gestreckt, keine zwei Schilder überlappen.
// Aufruf: node tools/check_map.js /abs/pfad/site/index.html [Welle=60] [screenshot.png]  → «OK» oder Fehlerliste (Exit 1)
// Vor jeder Karten-Änderung für mehrere Wellen laufen lassen (z. B. 5, 30, 60, 90).
// Anlass V523/V524: «☠ L27» als 82 px hoher Balken; «☠ L27» überdeckte «MANGROVE».
const { chromium } = require('playwright');
(async () => {
  const f = process.argv[2], CP = process.argv[3] || '60'; const b = await chromium.launch(); const pg = await b.newPage({ viewport: { width: 412, height: 915 } });
  await pg.addInitScript((CP) => { const L = { 'capy-reset': '276', 'tarnturm-tut': '1', 'tarnturm-terms': '1', 'capy-lang': 'en' };
    for (let c = 0; c < 4; c++) L['tarnturm-nuts-best-' + c] = String([27, 3, 30, 1][c]); L['tarnturm-cp-pro'] = CP; for (const k in L) localStorage.setItem(k, L[k]); }, CP);
  await pg.route(/\/api\//, r => r.fulfill({ status: 200, body: '{}' }));
  await pg.goto('file://' + f); await pg.waitForTimeout(2500);
  try { await pg.click('#splash', { timeout: 2000 }); } catch (e) {}
  await pg.waitForTimeout(1500); await pg.evaluate(() => document.getElementById('btnMap').click()); await pg.waitForTimeout(3500);
  const bad = await pg.evaluate(() => [...document.querySelectorAll('#ovMap em, #ovMap i, #ovMap b, .mNuts em, .mNuts i, .mPin em, .mPin b')]
    .filter(e => e.getClientRects().length).map(e => [e.className, e.getBoundingClientRect()]).filter(([c, r]) => r.height > 40 && r.height > 2.5 * r.width).map(([c, r]) => 'GESTRECKT ' + c + ' ' + Math.round(r.width) + '×' + Math.round(r.height)));
  const ov = await pg.evaluate(() => { const els = [...document.querySelectorAll('.mPin em, .nzTag, .nzL')].filter(e => e.getClientRects().length && getComputedStyle(e).visibility !== 'hidden'), r = els.map(e => e.getBoundingClientRect()), out = [];
    for (let a = 0; a < r.length; a++) for (let b = a + 1; b < r.length; b++) if (r[a].left < r[b].right && r[a].right > r[b].left && r[a].top < r[b].bottom && r[a].bottom > r[b].top) out.push(els[a].textContent.trim() + ' ↔ ' + els[b].textContent.trim()); return out; });
  if (ov.length) bad.push('ÜBERLAPPT: ' + ov.join(' | '));
  if (process.argv[4]) await pg.screenshot({ path: process.argv[4] });
  console.log(bad.length ? bad.join(', ') : 'OK'); await b.close(); process.exit(bad.length ? 1 : 0);
})();
