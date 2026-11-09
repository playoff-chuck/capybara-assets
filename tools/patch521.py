#!/usr/bin/env python3
"""V521 (Martin 09.11. 17:17): Nuts-Laden – ist ein Special aufgebraucht, klebt ein «SOLD OUT»-Sticker drüber.
Aufruf: python3 tools/patch521.py site/index.html"""
import sys
p = sys.argv[1]; s = open(p, encoding="utf-8").read()
def rep(a, b, n=1):
    global s
    c = s.count(a); assert c == n, (c, a[:80]); s = s.replace(a, b)
rep('const GAME_VER = "V520";', 'const GAME_VER = "V521";')
rep(""".replace('class="shopItem', 'class="shopItem dis'); });   /* V520 */""",
    """.replace('class="shopItem', 'class="shopItem dis'); if (k && k in OWN && !(OWN[k] > 0)) r[1] = r[1].replace(/<\\/div>\\s*$/, '<i class="soldOut">SOLD OUT</i></div>'); });   /* V520/V521 */""")
rep('.modeBtn.nzCont{', '.shopItem{position:relative}.shopItem .soldOut{position:absolute;left:50%;top:50%;transform:translate(-50%,-50%) rotate(-12deg);z-index:3;pointer-events:none;padding:4px 12px;font:400 20px/1 Bangers,system-ui;letter-spacing:.06em;color:#fff;background:#d8322e;border:3px solid #fff;border-radius:6px;box-shadow:0 0 0 3px #7a1210,0 4px 0 rgba(0,0,0,.3);white-space:nowrap}\n.modeBtn.nzCont{')
rep('  rows.sort((p, q) => p[0] - q[0]);\n  CATS.forEach(', '  if (S.nuts) for (let i = rows.length - 1; i >= 0; i--) if (/data-shop="wolf"/.test(rows[i][1])) rows.splice(i, 1);   /* V521: kein Wolf in Nuts */\n  rows.sort((p, q) => p[0] - q[0]);\n  CATS.forEach(')
open(p, "w", encoding="utf-8").write(s); print("ok V521")
