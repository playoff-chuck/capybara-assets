#!/usr/bin/env python3
"""V511: Nuts Südamerika (Skullgrog): «Skullgrog Rush» nicht mehr zuerst, sondern als letztes Lied – erst «Nuts Detour» (Martin 09.11. 16:23).
Aufruf: python3 tools/patch511.py site/index.html"""
import sys
p = sys.argv[1]; s = open(p, encoding="utf-8").read()
def rep(a, b, n=1):
    global s
    c = s.count(a); assert c == n, (c, a[:80]); s = s.replace(a, b)
rep('const GAME_VER = "V510";', 'const GAME_VER = "V511";')
rep('if (typeof S !== "undefined" && S && S.nuts) return [TRK_NZ[S.nuts.c] || TRK_NZ[0], TRK_NZ_ALL]; }',
    'if (typeof S !== "undefined" && S && S.nuts) return (S.nuts.c | 0) === 0 ? [TRK_NZ_ALL, TRK_NZ[0]] : [TRK_NZ[S.nuts.c] || TRK_NZ[0], TRK_NZ_ALL]; }   /* V511: Südamerika – Skullgrog Rush zuletzt */')
open(p, "w", encoding="utf-8").write(s); print("ok V511")
