#!/usr/bin/env python3
# V620: Testlink ?test=hack zeigt die Coach-Tipps (V619) jedes Mal, damit Martin sie prüfen kann.
import sys, os
site = sys.argv[1]; p = os.path.join(site, "index.html"); s = open(p, encoding="utf-8").read()
def rep(a, b, n=1):
    global s
    c = s.count(a); assert c == n, (c, a[:90]); s = s.replace(a, b)
rep('const GAME_VER = "V619";', 'const GAME_VER = "V620";')
rep('return LS.get("capy-hk-tips") !== "1" && S && S.started && !S.over && !S.nuts && !S.testRun && !S.replay;',
    'const th = !!(S && S.testRun && S.testKind === "hack"); return (LS.get("capy-hk-tips") !== "1" || th) && S && S.started && !S.over && !S.nuts && (!S.testRun || th) && !S.replay;')
rep('if (kind === "hack") { S.wave = w;', 'if (kind === "hack") { S.testKind = "hack"; S.wave = w;')
open(p, "w", encoding="utf-8").write(s)
print("ok V620")
