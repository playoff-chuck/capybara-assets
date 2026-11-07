"""V381 (Martin 07.11. 14:12, Screenshot «SPLAT THEM WITH BLOCKS!»): Spiel hält an, solange eine Tipp-Karte (Glühbirne) offen ist."""
import sys
src, dst = sys.argv[1], sys.argv[2]
s = open(src, encoding='utf-8').read()
def rep(a, b, cnt=1):
    global s
    n = s.count(a); assert n == cnt, (n, a[:70]); s = s.replace(a, b)
rep('const GAME_VER = "V380";', 'const GAME_VER = "V381";')
rep('function frozen() { return !S.started || S.over || S.paused || S.coachHold || S.intro || S.duel || S.mode || S.sel || S.shop || S.drop || S.ordersOpen || S.mix || S.tiltCard; }',
    'function frozen() { return !S.started || S.over || S.paused || S.coachHold || S.intro || S.duel || S.mode || S.sel || S.shop || S.drop || S.ordersOpen || S.mix || S.tiltCard || !!(window.__tipBulb && window.__tipBulb.open); }   /* V381: Tipp-Karte hält das Spiel an */')
open(dst, 'w', encoding='utf-8').write(s)
print("ok")
