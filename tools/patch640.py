#!/usr/bin/env python3
# V640 (Martin 11.11. 21:15): RU-Sprachclips mit passender Anrede – ab W31 Clip <k>__dr («дружище»), ab W61 <k>__dg («друг»).
# Clips in site/lang/voice_ru.json (tools/voice_addr_ru.py, HeyGen «Martin 4min», 12 Clips, 31 s, 0,01 $).
import sys, os
site = sys.argv[1]; p = os.path.join(site, "index.html"); s = open(p, encoding="utf-8").read()
def rep(a, b, n=1):
    global s
    c = s.count(a); assert c == n, (c, a[:90]); s = s.replace(a, b)
rep('const GAME_VER = "V639";', 'const GAME_VER = "V640";')
rep("/* V325: keine «soldier»-Sprüche */",
    "/* V640: RU-Anrede in der Stimme (ab W31 «дружище», ab W61 «друг») */\n"
    "try { (() => { const key = k => { try { if (I18N.lang !== \"ru\" || typeof k !== \"string\") return k; const TS = window.__TT && window.__TT.S, w = (TS && +TS.wave) || 0, k2 = w >= 61 ? k + \"__dg\" : w >= 31 ? k + \"__dr\" : null; return k2 && (window.__VOICE || {})[k2] ? k2 : k; } catch (e) { return k; } };\n"
    "  window.__sayKey = key; const sy = SFX.say; SFX.say = function (k) { const k2 = key(k); if (k2 === k) return sy.apply(SFX, arguments); const a = [...arguments]; a[0] = k2; return sy.apply(SFX, a); }; })(); } catch (e) { console.error(\"v640\", e); }\n"
    "/* V325: keine «soldier»-Sprüche */")
open(p, "w", encoding="utf-8").write(s)
print("ok V640")
