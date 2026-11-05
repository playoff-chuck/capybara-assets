"""V274 (Martin 05.11. 15:57): Angebots-Tor – nur echte Fenster zählen (keine Funk-Sprechblasen, kein Air-Drop-Kistchen),
30 s Abstand nach Fenster, max. 1 Angebot je 2 min. Boss-Hack: spätestens 2 Wellen nach Vormerkung ohne Abstand;
vorgemerkter Hack wird nicht mehr überschrieben."""
import sys
src, dst = sys.argv[1], sys.argv[2]
s = open(src, encoding='utf-8').read()
def rep(a, b, cnt=1):
    global s
    n = s.count(a); assert n == cnt, (n, a[:70]); s = s.replace(a, b)
rep('const GAME_VER = "V273";', 'const GAME_VER = "V274";')
rep('>= 45000 && performance.now() - (window.__offerLast || -1e9) >= 150000);',
    '>= 30000 && performance.now() - (window.__offerLast || -1e9) >= 120000);')
rep('if (S.intro || S.alert || S.duel || S.drop || S.ordersOpen ||', 'if (S.intro || S.duel || S.ordersOpen ||')
rep('if (hkOfferWave(S.wave) && S.wave < 150) S.hackPending = S.wave;', 'if (hkOfferWave(S.wave) && S.wave < 150) S.hackPending = S.hackPending || S.wave;')
rep('&& inPlay() && !(S.hackOfferUntil > performance.now()) && window.__offerOK()) {',
    '&& inPlay() && !(S.hackOfferUntil > performance.now()) && window.__offerOK((S.wave || 0) >= S.hackPending + 2)) {')
open(dst, 'w', encoding='utf-8').write(s)
