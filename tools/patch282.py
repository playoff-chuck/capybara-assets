"""V282 (Martin 16:46): Bildschirm-Ablauf konsolidiert – nie zwei Screens kurz hintereinander.
- `window.__whenCalm(fn, gap)`: führt fn erst aus, wenn kein Fenster/keine Karte offen ist und das letzte Fenster/der letzte Übergang
  mindestens `gap` ms zu ist (`__evtLast`). Pflicht-Fenster (Neuheiten Monster/Waffe, Orders beim Wiedereinstieg) laufen damit, gap 5 s.
- Einstieg (neues Spiel und Fortsetzen) zählt als Übergang: `__evtLast` = jetzt → Angebote frühestens 30 s danach.
- Angebote bleiben am gemeinsamen Tor (30 s nach Fenster, max. 1 je 2 min)."""
import sys
src, dst = sys.argv[1], sys.argv[2]
s = open(src, encoding='utf-8').read()
def rep(a, b, cnt=1):
    global s
    n = s.count(a); assert n == cnt, (n, a[:70]); s = s.replace(a, b)
rep('const GAME_VER = "V281";', 'const GAME_VER = "V282";')
rep('function uiWinOpen() {',
    '''window.__whenCalm = (fn, gap = 5000) => { const t0 = performance.now(); const tick = () => { try {
    const busy = uiWinOpen() || (S && (S.mapShow || S.mapFly || S.paused || S.ordersOpen || S.duel || S.drop)) || (typeof TUT !== "undefined" && TUT.on) || (typeof hkOfferOn === "function" && hkOfferOn());
    if (!S || !S.started || S.over) return;
    if (busy || performance.now() - (window.__evtLast || -1e9) < gap) { if (performance.now() - t0 < 600000) setTimeout(tick, 300); return; }
    fn(); } catch (e) { console.error("whenCalm", e); } }; setTimeout(tick, 300); };
function uiWinOpen() {''')
rep('if (q) showIntro(q);', 'if (q) window.__whenCalm(() => showIntro(q), 5000);')
rep('if (S.ordersOpen) { S.ordersOpen = false; setTimeout(() => showOrders(), 900); }',
    'window.__evtLast = performance.now(); if (S.ordersOpen) { S.ordersOpen = false; window.__whenCalm(() => showOrders(), 5000); }')
rep('function startGame(m, fromWave = 0) {', 'function startGame(m, fromWave = 0) { window.__evtLast = performance.now();')
rep('if (!S || !S.ordDue || !ordFree()) return; if (performance.now() - (S.ordDueT || 0) < 1200) return;',
    'if (!S || !S.ordDue || !ordFree()) return; if (performance.now() - (S.ordDueT || 0) < 1200 || performance.now() - (window.__evtLast || -1e9) < 5000) return;')
open(dst, 'w', encoding='utf-8').write(s)
