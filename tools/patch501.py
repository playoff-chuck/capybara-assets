#!/usr/bin/env python3
"""V501: Air-Drop-Tutorial nutzt den großen gelben Comic-Pfeil wie die anderen Tutorials (statt grünem Dreieck) – Martin 09.11. 14:44.
Aufruf: python3 tools/patch501.py site/index.html"""
import sys
p = sys.argv[1]; s = open(p, encoding="utf-8").read()
def rep(a, b, n=1):
    global s
    c = s.count(a); assert c == n, (c, a[:80]); s = s.replace(a, b)
rep('const GAME_VER = "V500";', 'const GAME_VER = "V501";')
rep('html body #coach.tt2,html body #coach.tt2 .coachCard,html body #coach.tt2 .coachArrow{visibility:visible!important}',
    'html body #coach.tt2,html body #coach.tt2 .coachCard{visibility:visible!important}')
rep('''        return null;
      }
      const a = null;''',
    '''        return null;
      }
      if (typeof TONTUT !== "undefined" && TONTUT.st && hintKey === "tontut") {   /* V501: Air-Drop-Tutorial */
        if (TONTUT.st === 2) return vis(document.querySelector('#sheetIn [data-pocket="ton"]'));
        return vis(document.getElementById("bBuild")); }
      const a = null;''')
open(p, "w", encoding="utf-8").write(s); print("ok V501")
