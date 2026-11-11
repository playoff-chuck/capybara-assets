#!/usr/bin/env python3
# V639 (Martin 11.11. 21:07): Anrede im Russischen nach Welle – W1–30 «напарник», ab W31 «дружище», ab W61 «друг».
# Nur Anrede («…, напарник!»), nicht die 3. Person («Напарник шлёт…», «напарник приносит…»). Nur RU.
import sys, os
site = sys.argv[1]; p = os.path.join(site, "index.html"); s = open(p, encoding="utf-8").read()
def rep(a, b, n=1):
    global s
    c = s.count(a); assert c == n, (c, a[:90]); s = s.replace(a, b)
rep('const GAME_VER = "V638";', 'const GAME_VER = "V639";')
rep("function T(t) {",
    'function capyAddr(v) { try { if (I18N.lang !== "ru" || typeof v !== "string" || v.indexOf("напарник") < 0) return v; const TS = window.__TT && window.__TT.S, w = (TS && +TS.wave) || 0; if (w < 31) return v;   /* V639: Anrede nach Welle */\n'
    '  return v.replace(/, напарник(?=[\\s.,!?–—])/g, w >= 61 ? ", друг" : ", дружище"); } catch (e) { return v; } }\n'
    "function T(t) {")
rep("const lead = raw.match(/^\\s*/)[0], tail = raw.match(/\\s*$/)[0]; return lead + v + tail; }",
    "const lead = raw.match(/^\\s*/)[0], tail = raw.match(/\\s*$/)[0]; return lead + capyAddr(v) + tail; }")
rep('el.querySelector(".say").innerHTML = `${VOICE_TEXT[key]}<small>',
    'el.querySelector(".say").innerHTML = `${capyAddr(VOICE_TEXT[key])}<small>')
open(p, "w", encoding="utf-8").write(s)
print("ok V639")
