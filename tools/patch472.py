#!/usr/bin/env python3
"""V472 – Sprachclips der gewählten Sprache werden wirklich abgespielt: nach dem Laden von lang/voice_<lang>.json
werden die Clips neu dekodiert (BUF), beim Zurückwechseln auf Englisch kommen die englischen Clips/Texte zurück.
Nutzung: python3 tools/patch472.py src dst"""
import sys
src, dst = sys.argv[1], sys.argv[2]
s = open(src, encoding="utf-8").read()

def rep(a, b, n=1):
    global s
    c = s.count(a)
    assert c == n, (c, a[:80])
    s = s.replace(a, b)

import re
m = re.search(r'const GAME_VER = "V(\d+)";', s); v = int(m.group(1))
rep(m.group(0), f'const GAME_VER = "V{v + 1}";')
rep('\nconst SAMPLES = {};\n/* V385:', '\nwindow.__VOICE = VOICE; window.__VOICE_TEXT = VOICE_TEXT;   /* V472: für die Sprachschicht erreichbar */\nconst SAMPLES = {};\n/* V385:')
rep('    if (lang !== "en") fetch(`lang/voice_${lang}.json?v=${GAME_VER}`).then(r => r.ok ? r.json() : null).catch(() => null).then(v => { if (!v) return; try { for (const k in (v.v || {})) VOICE[k] = v.v[k]; for (const k in (v.t || {})) VOICE_TEXT[k] = v.t[k]; } catch (e) {} });',
    '    { const VOICE = window.__VOICE || {}, VOICE_TEXT = window.__VOICE_TEXT || {}, VE = window.__voiceEN || (window.__voiceEN = { v: {}, t: {} });   /* V472: Original merken, wiederherstellen, neu dekodieren */\n'
    '      try { for (const k in VE.v) VOICE[k] = VE.v[k]; for (const k in VE.t) VOICE_TEXT[k] = VE.t[k]; } catch (e) {}\n'
    '      const dec = () => { try { window.__decAudio && window.__decAudio(); } catch (e) {} };\n'
    '      if (lang === "en") dec(); else fetch(`lang/voice_${lang}.json?v=${GAME_VER}`).then(r => r.ok ? r.json() : null).catch(() => null).then(v => { if (!v || I18N.lang !== lang) return; try {\n'
    '        for (const k in (v.v || {})) { if (!(k in VE.v) && k in VOICE) VE.v[k] = VOICE[k]; VOICE[k] = v.v[k]; }\n'
    '        for (const k in (v.t || {})) { if (!(k in VE.t) && k in VOICE_TEXT) VE.t[k] = VOICE_TEXT[k]; VOICE_TEXT[k] = v.t[k]; } } catch (e) {} dec(); }); }')
rep('  window.__decAudio = () => { if (ac) decodeAll(); };   /* V385 */', '  window.__decAudio = () => { if (ac) decodeAll(); };   /* V385 */\n  window.__vsrc = k => { const b = BUF["v_" + k]; return b ? (b.__src || "").slice(2000, 2030) + "|" + b.length : null; };   /* V472 Test-Hook */')
open(dst, "w", encoding="utf-8").write(s); print("ok", v + 1)
