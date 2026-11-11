#!/usr/bin/env python3
# V604 (Martin 11.11. 08:17): Beim allerersten Flug über die Karte (Spielstart, Welle ≤ 1, noch keine Sterne) keine Windrose
# (Sterne/Anomalie-Anzeige rechts unten) – nur Karte und Flugzeug. Dazu: Lektion 7/8 Stein ganz rechts in der Ring-Spalte.
import sys
src, dst = sys.argv[1], sys.argv[2]
s = open(src, encoding="utf-8").read()
def rep(a, b, n=1):
    global s
    c = s.count(a); assert c == n, (c, a[:90]); s = s.replace(a, b)
rep('const GAME_VER = "V603";', 'const GAME_VER = "V604";')
rep('ov.className = m === "browse" ? "browse" : "auto";',
    'ov.className = m === "browse" ? "browse" : "auto"; try { if (m !== "browse" && S && (S.wave | 0) <= 1 && Object.values(starsAll()).reduce((a, b) => a + (+b || 0), 0) === 0) ov.classList.add("firstFly"); } catch (e) {}   /* V604 */')
rep('.mapRose svg{width:60px;height:60px;', '#ovMap.firstFly .mapRose{display:none!important}\n.mapRose svg{width:60px;height:60px;')
# Martin 08:18 «Gaaanz rechts Blöcke kommen lassen»: Lektion 7/8 – Stein ganz an den rechten Rand, in die Ring-Spalte der Monster
rep('''if (!cells.every(([x]) => px + x >= 1 && px + x <= W - 2)) continue; if (px > bx) bx = px; }''',
    '''if (!cells.every(([x]) => px + x >= 1 && px + x <= W - 1)) continue; if (px > bx) bx = px; }   /* V604: bis in die Ring-Spalte */''')
open(dst, "w", encoding="utf-8").write(s)
print("ok", dst)
