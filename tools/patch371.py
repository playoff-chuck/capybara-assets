"""V371 (Martin 07.11. 09:20): Dieb geht oben auf dem Ring und läuft nach dem Griff ohne Beschleunigen einfach weiter.
- Größe passend zur oberen Ring-Spur (ca. 1,75 Felder hoch statt 96 px), Füße in der Spur.
- Nach dem Griff: gleiche Geh-Animation, konstantes Gehtempo (wie beim Hereinkommen), kein Renn-Zyklus."""
import sys
src, dst = sys.argv[1], sys.argv[2]
s = open(src, encoding='utf-8').read()
def rep(a, b, cnt=1):
    global s
    n = s.count(a); assert n == cnt, (n, a[:70]); s = s.replace(a, b)
rep('const GAME_VER = "V370";', 'const GAME_VER = "V371";')
rep('else { fi = 15 + Math.floor(t * 9) % 4; tilt = 0.05; }   /* V362: Renn-Zyklus mit Geldsack */',
    'else { fi = 7 + Math.floor(t * 10) % 8; }   /* V371: geht einfach weiter, kein Rennen */')
rep('const gw = (window.__gdim && window.__gdim()[0]) || 12, cell = cr.width / gw, feet = cr.top + cell * 0.92, gx = r.left + r.width / 2;',
    'const gw = (window.__gdim && window.__gdim()[0]) || 12, cell = cr.width / gw, feet = cr.top + cell * 0.86, gx = r.left + r.width / 2;')
rep('const t = T.t, sc0 = Math.max(0.62, Math.min(1, (feet - 26) / (SZ - 5))),',
    'const t = T.t, sc0 = Math.min(1, cell * 1.75 / (SZ - 14)),')
rep('const sc = Math.max(0.62, Math.min(1, (feet - 26) / (SZ - 5))), ga =',
    'const sc = sc0, ga =   /* V371: so groß wie die Ring-Spur erlaubt */')
rep('      : reach + (end - reach) * Math.pow(Math.min(1, (t - 10.6) / 19.4), 1.35);                  /* rennt weg, wird schneller */',
    '      : Math.min(end, reach + Math.max((stop - x0) / 8, (end - reach) / 19) * (t - 10.6));        /* V371: geht im gleichen Tempo weiter */')
open(dst, 'w', encoding='utf-8').write(s)
print("ok")
