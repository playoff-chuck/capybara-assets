#!/usr/bin/env python3
# V641 (Martin 11.11. 21:49): «JOIN THE SQUAD» blockiert nichts mehr (Boss-Hack/Angebote warteten auf das Rufzeichen-Fenster);
# Fenster kommt in der nächsten Wellenpause ohne 95-s-Takt. Beitritt/Name/Held bleiben beim Tutorial-Zurücksetzen (V609) erhalten.
import sys, os
site = sys.argv[1]; p = os.path.join(site, "index.html"); s = open(p, encoding="utf-8").read()
def rep(a, b, n=1):
    global s
    c = s.count(a); assert c == n, (c, a[:90]); s = s.replace(a, b)
rep('const GAME_VER = "V640";', 'const GAME_VER = "V641";')
rep('const join = !joined() && (S.wave || 0) >= 7; return lucky || join;',
    'return lucky;   /* V641: Rufzeichen-Fenster hält nichts mehr auf */')
rep('if (!window.__offerOK()) { clearTimeout(window.__joinT); window.__joinT = setTimeout(maybeJoin, 3000); return; }',
    'if (!(window.__playScreen && window.__playScreen())) { clearTimeout(window.__joinT); window.__joinT = setTimeout(maybeJoin, 1500); return; }   /* V641: nächste Wellenpause, ohne 95-s-Takt */')
rep('capy-tutbak|capy-tutDone|capy-tutBack)$/', 'capy-tutbak|capy-tutDone|capy-tutBack|tarnturm-join|tarnturm-nick|tarnturm-hero)$/', 2)
open(p, "w", encoding="utf-8").write(s)
print("ok V641")
