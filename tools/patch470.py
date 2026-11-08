#!/usr/bin/env python3
"""V470 – t136 Rest: Wow-Banner («SQUAD INCOMING!» u. a.) passt auf schmale Screens in allen Sprachen
(PT «ESQUADRÃO CHEGANDO!» lief bei 360 px 10 px über den Rand) – Schrift schrumpft, bis der Titel passt;
Untertitel «Rosie/Blue sends a free Ten-ton drop» übersetzt (fehlte in ES/PT/DE/RU).
Nutzung: python3 tools/patch470.py src dst  (Übersetzungen: tools/lang_src/<lang>_v470.json + i18n_merge.py)"""
import sys
src, dst = sys.argv[1], sys.argv[2]
s = open(src, encoding="utf-8").read()

def rep(a, b, n=1):
    global s
    c = s.count(a)
    assert c == n, (c, a[:80])
    s = s.replace(a, b)

rep('const GAME_VER = "V469";', 'const GAME_VER = "V470";')
rep('function wowBanner(t, sub) { const d = document.createElement("div"); d.className = "wowBan"; d.innerHTML = `<b>${t}</b>${sub ? `<small>${sub}</small>` : ""}`; document.body.appendChild(d); setTimeout(() => d.remove(), 2000); }',
    'function wowBanner(t, sub) { const d = document.createElement("div"); d.className = "wowBan"; d.innerHTML = `<b>${t}</b>${sub ? `<small>${sub}</small>` : ""}`; document.body.appendChild(d); wowBanFit(d); setTimeout(() => wowBanFit(d), 60); setTimeout(() => d.remove(), 2000); }\n'
    '/* V470 (t136): übersetzte Titel (PT «ESQUADRÃO CHEGANDO!») nie breiter als der Screen – Schrift schrumpft */\n'
    'function wowBanFit(d) { try { const b = d.querySelector("b"); if (!b) return; b.style.fontSize = ""; const max = window.innerWidth - 24, w = b.offsetWidth; if (w > max) b.style.fontSize = Math.floor(44 * max / w) + "px"; } catch (e) {} }')
rep('.wowBan small{display:inline-block;margin-top:8px;',
    '.wowBan small{display:inline-block;max-width:calc(100vw - 32px);margin-top:8px;')
open(dst, "w", encoding="utf-8").write(s)
print("ok V470")
