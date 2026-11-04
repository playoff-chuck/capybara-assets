"""V212: Kein Doppel-Drop mehr – nach dem Landen eines Steins sind die Fall-Tasten (blau ▼, grün ⤓)
für 300 ms gesperrt, damit ein versehentlicher zweiter Tipp nicht gleich den nächsten Stein mitreißt."""
import sys
src, dst = sys.argv[1], sys.argv[2]
s = open(src, encoding='utf-8').read()
def rep(a, b, cnt=1):
    global s
    n = s.count(a); assert n == cnt, (n, a[:70]); s = s.replace(a, b)
rep('const GAME_VER = "V211";', 'const GAME_VER = "V212";')
rep('function spawnPiece() {', 'function spawnPiece() { S.dropLockUntil = performance.now() + 300;')
rep('function softDrop() { const p = S.piece; if (!canAct()) return;', 'function softDrop() { const p = S.piece; if (!canAct()) return; if (performance.now() < (S.dropLockUntil || 0)) return;')
rep('function hardDrop() { if (S.duel) { if (HK.phase === "pick") hkPick(HK.prev); return; } const p = S.piece; if (!canAct()) return;',
    'function hardDrop() { if (S.duel) { if (HK.phase === "pick") hkPick(HK.prev); return; } const p = S.piece; if (!canAct()) return; if (performance.now() < (S.dropLockUntil || 0)) return;')
open(dst, 'w', encoding='utf-8').write(s); print('ok')
