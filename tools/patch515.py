#!/usr/bin/env python3
"""V515: Test-Link ?test=shock – Ten-ton fällt automatisch alle 5 s in Welle 9 (Druckwelle + Sound vorführen), Martin 09.11. 16:42.
Aufruf: python3 tools/patch515.py site/index.html"""
import sys
p = sys.argv[1]; s = open(p, encoding="utf-8").read()
def rep(a, b, n=1):
    global s
    c = s.count(a); assert c == n, (c, a[:80]); s = s.replace(a, b)
rep('const GAME_VER = "V514";', 'const GAME_VER = "V515";')
rep('const map = { ton: 9,', 'const map = { shock: 9, ton: 9,')
rep('if (q === "ton") { S.tons = (S.tons || 0) + 2; LS.set("capy-tut-ton", "1"); }   /* V508 */',
    '''if (q === "ton") { S.tons = (S.tons || 0) + 2; LS.set("capy-tut-ton", "1"); }   /* V508 */
        if (q === "shock") { LS.set("capy-tut-ton", "1"); S.lives = 99; toast("TEST · Ten-ton drops every 5 s", "HQ", 2600);   /* V515: Druckwelle vorführen */
          const iv = setInterval(() => { try { if (!S || S.over || !S.started) { clearInterval(iv); return; } if (S.ton || S.paused || frozen()) return; S.tons = Math.max(1, S.tons || 0); startTon(); } catch (e) {} }, 5000); }''')
open(p, "w", encoding="utf-8").write(s); print("ok V515")
