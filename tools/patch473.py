#!/usr/bin/env python3
"""V473 – Echtes Höhlen-Hintergrundbild im Nuts-Abstecher (Frage C, Martin 08.11. «zeig erst ein Nano-Bild» → «bau ein»):
bg/nuts_<kontinent>.webp (vorerst nur Südamerika, Nano Banana Pro 0,14 $). Gibt es für den Kontinent ein Bild,
ersetzt es den Orts-Hintergrund; der rote Höhlen-Tint wird dann deutlich zurückgenommen, weil das Bild das Licht
schon mitbringt. Kontinente ohne Bild behalten den bisherigen Look (Orts-Bild + Tint).
Nutzung: python3 tools/patch473.py src dst"""
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

rep('function wherePos(w) {',
    'const NUTS_BG = ["bg/nuts_samerica.webp", null, null, null];   /* V473: echtes Höhlenbild je Nuts-Territorium (null = alter Look) */\n'
    'const NUTS_DI = Object.assign({}, NUTS_D, { f: "saturate(1.1) brightness(.96)", night: .06, tint: "linear-gradient(180deg,rgba(150,30,40,.12),rgba(30,8,12,.2))" });   /* V473: Tint zurückgenommen, wenn ein Bild da ist */\n'
    'function wherePos(w) {')
rep('  const P = wherePos(live ? S.wave || 1 : 1), D = live ? (S.nuts ? NUTS_D : DAY[P.d]) : DAY[1];\n'
    '  const key = P.cont[0] + "|" + P.p + "|" + (live ? (S.nuts ? "nuts" : P.d) : "menu");\n'
    '  if (key === skyKey) return; skyKey = key;\n'
    '  const im = SKY_BG[P.cont[0]], pl = (PLACE_BG[P.c === 4 ? "antarctica" : P.cont[0]] || [])[P.p];',
    '  const nb = live && S.nuts ? NUTS_BG[S.nuts.c | 0] : null;   /* V473 */\n'
    '  const P = wherePos(live ? S.wave || 1 : 1), D = live ? (S.nuts ? (nb ? NUTS_DI : NUTS_D) : DAY[P.d]) : DAY[1];\n'
    '  const key = P.cont[0] + "|" + P.p + "|" + (live ? (S.nuts ? "nuts" + (nb ? "i" : "") : P.d) : "menu");\n'
    '  if (key === skyKey) return; skyKey = key;\n'
    '  const im = SKY_BG[P.cont[0]], pl = nb || (PLACE_BG[P.c === 4 ? "antarctica" : P.cont[0]] || [])[P.p];')
rep('  if (key === skyKey) return; skyKey = key;\n  const im = SKY_BG[P.cont[0]], pl = nb ||',
    '  if (key === skyKey) return; skyKey = key; document.body.classList.toggle("nzImg", !!nb);   /* V473 */\n  const im = SKY_BG[P.cont[0]], pl = nb ||')
rep('body.inNuts #sky{filter:brightness(.28) saturate(.6) sepia(.45) hue-rotate(-22deg) contrast(1.15)!important}',
    'body.inNuts #sky{filter:brightness(.28) saturate(.6) sepia(.45) hue-rotate(-22deg) contrast(1.15)!important}\n'
    'body.inNuts.nzImg #sky{filter:brightness(.72) saturate(1.05) contrast(1.08)!important}   /* V473: echtes Höhlenbild bleibt sichtbar */')
open(dst, "w", encoding="utf-8").write(s); print("ok", v + 1)
