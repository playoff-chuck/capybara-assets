#!/usr/bin/env python3
# V643 (Martin 11.11. 21:49 «nichts länger als 2 Wellen blockiert»): Air-Drop-Angebote (Specials) stauten sich im Test W3–W17
# (Kanone ab W3, dazu Frost/Sniper/Ten-ton) – der 30-s-Ruhe/95-s-Takt kam in kurzen Wellen nie zustande.
# Neu: wartet ein bezahlbares Angebot ≥ 2 Wellen, kommt es mit 15 s Abstand zum letzten Ereignis; nach 6 Wellen verfällt es.
import sys, os
site = sys.argv[1]; p = os.path.join(site, "index.html"); s = open(p, encoding="utf-8").read()
def rep(a, b, n=1):
    global s
    c = s.count(a); assert c == n, (c, a[:90]); s = s.replace(a, b)
rep('const GAME_VER = "V642";', 'const GAME_VER = "V643";')
rep('setInterval(() => { try { if (!S || !S.adDue || !calm() || !window.__offerOK()) return;',
    'setInterval(() => { try { if (!S || !S.adDue) return;\n'
    '      { const w = S.wave | 0; S.adDueW = S.adDueW || {}; for (const k in S.adDueW) if (!S.adDue[k]) delete S.adDueW[k];   /* V643: wie lange wartet jedes Angebot */\n'
    '        for (const k in S.adDue) { if (!S.adDue[k]) continue; if (S.adDueW[k] == null) S.adDueW[k] = w; if (w - S.adDueW[k] > 6) { delete S.adDue[k]; delete S.adDueW[k]; } } }\n'
    '      const od = Object.keys(S.adDue).some(k => S.adDue[k] && (S.wave | 0) - S.adDueW[k] >= 2 && !why(k)) && performance.now() - Math.max(window.__offerLast || -1e9, window.__evtLast || -1e9) >= 15000;\n'
    '      if (!calm() || !(window.__offerOK() || od)) return;')
open(p, "w", encoding="utf-8").write(s)
print("ok V643")
