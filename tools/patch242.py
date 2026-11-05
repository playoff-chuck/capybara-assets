"""V242: (1) Boss-Hack-Uhr steht, solange eine Szene oder ein Fenster offen ist (Karte/Flug, Neuheit, Air Drop, Wild Cards,
Pause, Menüs); danach bleiben mindestens 8 s. (2) Kontinentwechsel in fester Reihenfolge: Air Drop → Wild Cards (W20/40/…)
→ Wegweiser (W30/60/90/120) → Feier + Flug → höchstens ein Neuheiten-Fenster. Wild Cards hängen nicht mehr an einem
5,3-s-Timer (kamen mitten im Flug oder erst in der neuen Welle). Der Wegweiser kommt vor dem Boss-Signal (ging bei W30/W90
verloren, wenn man den Boss nicht sofort gespielt hat); das Boss-Signal erscheint dann nach der Ankunft."""
import sys
src, dst = sys.argv[1], sys.argv[2]
s = open(src, encoding='utf-8').read()
def rep(a, b, cnt=1):
    global s
    n = s.count(a); assert n == cnt, (n, a[:70]); s = s.replace(a, b)
rep('const GAME_VER = "V241";', 'const GAME_VER = "V242";')

# (1) Uhr anhalten + Start nur, wenn nichts offen ist und kein Wegweiser/Wild Cards anstehen
rep('''const HK_OFFER_S = 20;   // V178z6: 20 s
function hkOfferTick() {
  if (!S || !S.started || S.over) return;
  if (S.hackPending && !S.drop && !S.ordersOpen && !S.duel && !S.paused && inPlay() && !(S.hackOfferUntil > performance.now()))''',
'''const HK_OFFER_S = 20;   // V178z6: 20 s
let hkLastT = 0, hkHeldMs = 0;   // V242: Uhr steht während Szenen/Fenstern
function hkHold() { return !!(S.mapShow || S.intro || S.drop || S.ordersOpen || S.paused || !inPlay()); }
function hkSignFirst() { try { const c = NZ_BASES.indexOf(S.wave); return c >= 0 && !S.inWave && !S.nuts && !S.won && !(S.nutsAsk || {})[c]; } catch (e) { return false; } }
function hkOfferTick() {
  if (!S || !S.started || S.over) { hkLastT = 0; return; }
  { const now = performance.now(), dt = hkLastT ? now - hkLastT : 0; hkLastT = now;
    if (S.hackOfferUntil > 0 && !S.duel) { if (hkHold()) { S.hackOfferUntil += dt; hkHeldMs += dt; } else { if (hkHeldMs > 1500) S.hackOfferUntil = Math.max(S.hackOfferUntil, now + 8000); hkHeldMs = 0; } } else hkHeldMs = 0; }
  if (S.hackPending && !S.drop && !S.ordersOpen && !S.duel && !S.paused && !S.intro && !S.mapShow && !S.ordDue && !hkSignFirst() && !(!S.inWave && S.waveCD < 0.6) && inPlay() && !(S.hackOfferUntil > performance.now()))''')

# (2a) Wild Cards: vormerken statt Timer
rep('if (S.wave % 20 === 0 && S.wave >= 20) setTimeout(() => { if (S.started && !S.over) showOrders(); }, 5300);',
    'if (S.wave % 20 === 0 && S.wave >= 20) { S.ordDue = S.wave; S.ordDueT = performance.now(); }   /* V242: kommt nach dem Air Drop, vor Wegweiser und Flug */')
# (2b) Wegweiser: nach den Wild Cards, vor dem Boss-Signal
rep('if (S.toSpawn > 0 || S.monsters.length || S.hackPending || hkOfferOn() || !inPlay()) return;\n  showSign(c);',
    'if (S.toSpawn > 0 || S.monsters.length || S.ordDue || hkOfferOn() || !inPlay()) return;\n  showSign(c);')
# (2c) Spielstand
rep('const SAVE_KEYS = ["nutsAsk", ', 'const SAVE_KEYS = ["ordDue", "hackPending", "nutsAsk", ')

# (2d) Wild Cards zeigen, sobald nichts anderes offen ist; Wellenstart wartet auf Wild Cards und Wegweiser
js = '''
  /* V242: Reihenfolge am Wellenende – Air Drop → Wild Cards → Wegweiser → Feier/Flug */
  try {
    const ordFree = () => S && S.started && !S.over && !S.nuts && !S.drop && !S.intro && !S.duel && !S.paused && !S.mapShow && !S.ordersOpen && inPlay();
    setInterval(() => { try { if (!S || !S.ordDue || !ordFree()) return; if (performance.now() - (S.ordDueT || 0) < 1200) return; S.ordDue = 0; showOrders(); } catch (e) {} }, 300);
    const _swG = startWave; startWave = function () {
      try { if (S && S.started && !S.over && !S.nuts && !S.inWave) {
          if (S.ordDue) { if (ordFree()) { S.ordDue = 0; showOrders(); } return; }
          if (hkSignFirst()) { if (!S.drop && !S.intro && !S.duel && !S.paused && inPlay() && !hkOfferOn()) showSign(NZ_BASES.indexOf(S.wave)); if (!hkOfferOn()) return; }
        } } catch (e) {}
      return _swG.apply(this, arguments); };
  } catch (e) { console.error("v242", e); }
'''
tail = '})();\n</script>'
assert s.count(tail) >= 1
i = s.rfind(tail); s = s[:i] + js + s[i:]
open(dst, 'w', encoding='utf-8').write(s); print('ok')
