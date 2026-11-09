// Grafik-Prüfung Weltkarte mit Spielfortschritt (Nuts-Bestwerte, Welle 60): kein Schild/Etikett darf gestreckt sein.
// Aufruf: node tools/check_map.js /abs/pfad/site/index.html   → «OK» oder Liste der gestreckten Elemente (Exit 1)
// Anlass V523: «☠ L27» war ein 82 px hoher Balken (top + bottom gleichzeitig gesetzt) – nur sichtbar mit Nuts-Fortschritt.
const { chromium } = require('playwright');
(async () => {
  const f = process.argv[2]; const b = await chromium.launch(); const pg = await b.newPage({ viewport: { width: 412, height: 915 } });
  await pg.addInitScript(() => { const L = { 'capy-reset': '276', 'tarnturm-tut': '1', 'tarnturm-terms': '1', 'capy-lang': 'en', 'tarnturm-cp-pro': '60' };
    for (let c = 0; c < 4; c++) L['tarnturm-nuts-best-' + c] = String([27, 3, 30, 1][c]); for (const k in L) localStorage.setItem(k, L[k]); });
  await pg.route(/\/api\//, r => r.fulfill({ status: 200, body: '{}' }));
  await pg.goto('file://' + f); await pg.waitForTimeout(2500);
  try { await pg.click('#splash', { timeout: 2000 }); } catch (e) {}
  await pg.waitForTimeout(1500); await pg.evaluate(() => document.getElementById('btnMap').click()); await pg.waitForTimeout(3500);
  const bad = await pg.evaluate(() => [...document.querySelectorAll('#ovMap em, #ovMap i, #ovMap b, .mNuts em, .mNuts i, .mPin em, .mPin b')]
    .filter(e => e.getClientRects().length).map(e => [e.className, e.getBoundingClientRect()]).filter(([c, r]) => r.height > 40 && r.height > 2.5 * r.width).map(([c, r]) => c + ' ' + Math.round(r.width) + '×' + Math.round(r.height)));
  console.log(bad.length ? 'GESTRECKT: ' + bad.join(', ') : 'OK'); await b.close(); process.exit(bad.length ? 1 : 0);
})();
