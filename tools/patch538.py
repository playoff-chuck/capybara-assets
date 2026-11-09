#!/usr/bin/env python3
"""V538 (Martin 09.11. 21:41): Versionsnummer oben rechts wieder auf Martins Handy (neue Spieler-Nr. nach Reset:
5478-BQ27 / BEEM-MGDC) und Sichtbarkeit laufend nachziehen (z. B. sofort nach Erhalt des Admin-Schlüssels).
Aufruf: python3 tools/patch538.py site/index.html"""
import sys
p = sys.argv[1]; s = open(p, encoding="utf-8").read()
def rep(a, b, n=1):
    global s
    c = s.count(a); assert c == n, (c, a[:80]); s = s.replace(a, b)
rep('const GAME_VER = "V537";', 'const GAME_VER = "V538";')
rep('capyUid() === "M2HL-KCQH" || !!localStorage.getItem("capy-adm");',
    '["M2HL-KCQH", "5478-BQ27", "BEEM-MGDC"].includes(capyUid()) || !!localStorage.getItem("capy-adm");')
rep('t.hidden = !capyMe(); o.appendChild(t); } }); } catch (e) {}',
    't.hidden = !capyMe(); o.appendChild(t); } }); } catch (e) {}\n  setInterval(() => { try { const me = capyMe(); document.querySelectorAll(".verTag").forEach(t => { if (t.hidden === me) t.hidden = !me; }); } catch (e) {} }, 1000);   /* V538 */')
open(p, "w", encoding="utf-8").write(s); print("ok V538")
