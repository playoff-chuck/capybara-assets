"""V198: Hauptmusik klingt beim Boss-Hack in 3 s aus statt schlagartig zu stoppen."""
import sys
src, dst = sys.argv[1], sys.argv[2]
s = open(src, encoding='utf-8').read()
def rep(a, b, cnt=1):
    global s
    n = s.count(a); assert n == cnt, (n, a[:70]); s = s.replace(a, b)
rep('const GAME_VER = "V197";', 'const GAME_VER = "V198";')
rep('let hackHeld = false, wasHack = false;', 'let hackHeld = false, wasHack = false, hackFadeT = null, hackNow = false;')
rep('try { if (hackUp && TP.el && !TP.el.paused) { TP.el.pause(); hackHeld = true; }',
    'hackNow = hackUp; try { if (hackUp && TP.el && !TP.el.paused && !hackFadeT) { tpFade(0.0001, 3); hackFadeT = setTimeout(() => { hackFadeT = null; if (hackNow && TP.el && !TP.el.paused) { TP.el.pause(); hackHeld = true; } }, 3000); }\n      else if (!hackUp && hackFadeT) { clearTimeout(hackFadeT); hackFadeT = null; tpFade(0.5, 0.8); }')
open(dst, 'w', encoding='utf-8').write(s); print('ok')
