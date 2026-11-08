#!/usr/bin/env python3
"""V479 – Test-Links für die Nuts-Höhlen der anderen Kontinente: ?test=nuts2 (Afrika, W61), nuts3 (Asien, W91), nuts4 (Nordamerika, W121);
?test=nuts bleibt Südamerika. Nutzung: python3 tools/patch479.py src dst"""
import sys, re
src, dst = sys.argv[1], sys.argv[2]
s = open(src, encoding="utf-8").read()

def rep(a, b, n=1):
    global s
    c = s.count(a)
    assert c == n, (c, a[:80])
    s = s.replace(a, b)

m = re.search(r'const GAME_VER = "V(\d+)";', s); v = int(m.group(1))
rep(m.group(0), f'const GAME_VER = "V{v + 1}";')
rep('peek: 3, nuts: 31, thief: 100,', 'peek: 3, nuts: 31, nuts2: 61, nuts3: 91, nuts4: 121, thief: 100,')
rep('if (q === "nuts") { setTimeout(() => { try { S.testRun = false; S.inWave = false; startDetour(0); } catch (e) {} }, 1500); }',
    'if (/^nuts\\d?$/.test(q)) { const nc = Math.max(0, (+q.slice(4) || 1) - 1); setTimeout(() => { try { S.testRun = false; S.inWave = false; startDetour(nc); } catch (e) {} }, 1500); }   /* V479: nuts2–4 = Afrika/Asien/Nordamerika */')
open(dst, "w", encoding="utf-8").write(s); print("ok", v + 1)
