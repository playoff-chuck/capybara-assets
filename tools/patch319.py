"""V319 (Käufer-Testlauf 06.11.: Orden-Fenster «FROM ROSIE WITH LOVE» kam 0,25 s nach dem Boss-Duell):
Orden-Geschenk wartet jetzt wie alle Pflicht-Fenster, bis kein Fenster offen ist und seit dem letzten Fenster 5 s Ruhe war."""
import sys
src, dst = sys.argv[1], sys.argv[2]
s = open(src, encoding='utf-8').read()
def rep(a, b, cnt=1):
    global s
    n = s.count(a); assert n == cnt, (n, a[:70]); s = s.replace(a, b)
rep('const GAME_VER = "V318";', 'const GAME_VER = "V319";')
rep('  const ms = albTake(), m = ms[0], h = heroKey(), b = buddyKey(), bn = b === "rosie" ? "Rosie" : "Blue";',
    '  try { if (uiWinOpen() || (S && (S.mapShow || S.mapFly || S.ordersOpen || S.drop)) || performance.now() - (window.__evtLast || -1e9) < 5000) { clearTimeout(window.__albT); window.__albT = setTimeout(albTry, 1000); return; } } catch (e) {}   /* V319: 5 s Ruhe */\n'
    '  const ms = albTake(), m = ms[0], h = heroKey(), b = buddyKey(), bn = b === "rosie" ? "Rosie" : "Blue";')
rep('function albGrant(id, img, name, line, tint) {', 'window.__albGrant = (...a) => albGrant(...a);   /* V319: Test-Hook */\nfunction albGrant(id, img, name, line, tint) {')
open(dst, 'w', encoding='utf-8').write(s)
print("ok")
