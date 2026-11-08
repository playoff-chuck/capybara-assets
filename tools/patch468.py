#!/usr/bin/env python3
"""V468 – Russisch live (lang/ru.json). Übersetzung von «A: B»-Texten (z. B. «ON THE RADAR: GRUNTS») aus beiden Teilen.
Nutzung: python3 tools/patch468.py src dst"""
import sys
src, dst = sys.argv[1], sys.argv[2]
s = open(src, encoding="utf-8").read()

def rep(a, b, n=1):
    global s
    c = s.count(a)
    assert c == n, (c, a[:80])
    s = s.replace(a, b)

rep('const GAME_VER = "V467";', 'const GAME_VER = "V468";')
rep('if (hit) return out.join(" · "); }\n  return null; }',
    'if (hit) return out.join(" · "); }\n'
    '  if (key.includes(": ")) { const i = key.indexOf(": "), a = key.slice(0, i), b = key.slice(i + 2); const va = i18nLookup(a), vb = i18nLookup(b); if (va != null && vb != null) return va + ": " + vb; }   /* V468 */\n'
    '  return null; }')

CYR = "U+0301,U+0400-045F,U+0490-0491,U+04B0-04B1,U+2116"
ff = (f"@font-face{{font-family:'Bangers';font-style:normal;font-weight:400;font-display:swap;src:url(fonts/oswald-700-cyrillic.woff2) format('woff2');unicode-range:{CYR}}}"
      f"@font-face{{font-family:'Barlow Condensed';font-style:normal;font-weight:500 600;font-display:swap;src:url(fonts/oswald-600-cyrillic.woff2) format('woff2');unicode-range:{CYR}}}"
      f"@font-face{{font-family:'Barlow Condensed';font-style:normal;font-weight:700 900;font-display:swap;src:url(fonts/oswald-700-cyrillic.woff2) format('woff2');unicode-range:{CYR}}}"
      f"@font-face{{font-family:'Baloo 2';font-style:normal;font-weight:400 900;font-display:swap;src:url(fonts/nunito-var-cyrillic.woff2) format('woff2');unicode-range:{CYR}}}\n")
i = s.index("@font-face{font-family:'Baloo 2'"); s = s[:i] + ff + s[i:]   # V468: Kyrillisch (Oswald für Bangers/Barlow, Nunito für Baloo)
open(dst, "w", encoding="utf-8").write(s); print("ok V468")
