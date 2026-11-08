#!/usr/bin/env python3
"""V482 – Deutsch vorerst abgeschaltet (Martin 08.11. 23:17 «die deutsche Version gefällt mir nicht … entferne die Optionen»):
«de» aus LANGS entfernt → keine Flagge beim ersten Start und im Zahnrad-Menü; ein gespeichertes «de» fällt auf Englisch zurück.
Dateien site/lang/de.json und voice_de.json bleiben im Repo (Wiedereinschalten = eine Zeile). Nutzung: python3 tools/patch482.py src dst"""
import sys, re
src, dst = sys.argv[1], sys.argv[2]
s = open(src, encoding="utf-8").read()
def rep(a, b, n=1):
    global s
    c = s.count(a); assert c == n, (c, a[:80]); s = s.replace(a, b)
m = re.search(r'const GAME_VER = "V(\d+)";', s); v = int(m.group(1))
rep(m.group(0), f'const GAME_VER = "V{v + 1}";')
rep('''pt: { flag: "🇧🇷🇵🇹", name: "Português" }, de: { flag: "🇦🇹🇩🇪🇨🇭", name: "Deutsch" }, ru: { flag: "🇷🇺", name: "Русский" } };''',
    '''pt: { flag: "🇧🇷🇵🇹", name: "Português" }, ru: { flag: "🇷🇺", name: "Русский" } };   /* V482: de vorerst abgeschaltet (Martin 08.11.) – zum Einschalten wieder einfügen: de: { flag: "🇦🇹🇩🇪🇨🇭", name: "Deutsch" } */''')
rep('''  try { const l = localStorage.getItem("capy-lang"); if (l && LANGS[l]) I18N.lang = l; } catch (e) {} })();''',
    '''  try { const l = localStorage.getItem("capy-lang"); if (l && LANGS[l]) I18N.lang = l; else if (l) localStorage.setItem("capy-lang", "en"); } catch (e) {} })();   /* V482: abgeschaltete Sprache → Englisch */''')
open(dst, "w", encoding="utf-8").write(s); print("ok", v + 1)
