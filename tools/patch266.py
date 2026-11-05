"""V266 (Martin 05.11. 15:12): Ein gemeinsames Tor für alle Angebote (Sale-Anzeigen, Lucky Supply, Boss-Hack-Angebot,
Rufzeichen-Abfrage): mindestens 45 s nach jedem anderen Fenster/Ereignis und höchstens ein Angebot je 2,5 min.
Ausnahme: das Boss-Hack-Angebot wird spätestens zwei Wellen nach seiner Welle gezeigt (dann ohne Abstandsregel)."""
import sys
src, dst = sys.argv[1], sys.argv[2]
s = open(src, encoding='utf-8').read()
def rep(a, b, cnt=1):
    global s
    n = s.count(a); assert n == cnt, (n, a[:70]); s = s.replace(a, b)
rep('const GAME_VER = "V265";', 'const GAME_VER = "V266";')
gate = 'window.__offerOK = (force) => force || (performance.now() - (window.__evtLast || -1e9) >= 45000 && performance.now() - (window.__offerLast || -1e9) >= 150000);\n'
rep('const HK_OFFER_S = 20;', gate + 'const HK_OFFER_S = 20;')
rep('&& inPlay() && !(S.hackOfferUntil > performance.now())) { S.hackOfferWave = S.hackPending;',
    '&& inPlay() && !(S.hackOfferUntil > performance.now()) && window.__offerOK(S.wave >= S.hackPending + 2)) { window.__offerLast = performance.now(); S.hackOfferWave = S.hackPending;')
rep('  if (S.drop || S.ordersOpen || S.duel) { setTimeout(maybeJoin, 1500); return; }\n  S.intro = true; S.joinOpen = true;',
    '  if (S.drop || S.ordersOpen || S.duel) { setTimeout(maybeJoin, 1500); return; }\n  if (!window.__offerOK()) { clearTimeout(window.__joinT); window.__joinT = setTimeout(maybeJoin, 3000); return; }\n  window.__offerLast = performance.now(); S.intro = true; S.joinOpen = true;')
rep('lastW = why(k); paint(); window.__adLast = performance.now();', 'lastW = why(k); paint(); window.__adLast = window.__offerLast = performance.now();')
rep('if (!S || !S.adDue || !calm() || performance.now() - Math.max(window.__adLast || -1e9, window.__evtLast || -1e9) < 45000) return;',
    'if (!S || !S.adDue || !calm() || !window.__offerOK()) return;')
rep('&& performance.now() - Math.max(window.__evtLast || -1e9, window.__adLast || -1e9) >= 45000 && !S.inWave', '&& window.__offerOK() && !S.inWave')
rep('if (S) { S.banditDone = true; S.banditNext =', 'if (S) { window.__offerLast = performance.now(); S.banditDone = true; S.banditNext =')
open(dst, 'w', encoding='utf-8').write(s); print('ok')
