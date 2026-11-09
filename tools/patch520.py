#!/usr/bin/env python3
"""V520 (Martin 09.11. 17:16): Nuts-Regel «gleiche Ausrüstung für alle»:
- Gold nur noch Baumaterial für Türme/Waffen/Ausbau (Start 0, verdient durch Monster + Level).
- Laden für Specials, Coach und Wolf in Nuts zu; kein Boss-Hack (Einsatz) in Nuts.
- Specials nur aus Grundausstattung (2 je Sorte) + Airdrops. Restgold zählt nicht.
Aufruf: python3 tools/patch520.py site/index.html"""
import sys
p = sys.argv[1]; s = open(p, encoding="utf-8").read()
def rep(a, b, n=1):
    global s
    c = s.count(a); assert c == n, (c, a[:80]); s = s.replace(a, b)
rep('const GAME_VER = "V519";', 'const GAME_VER = "V520";')
NZB = '["snipe","tesla","wolf","mix","chomp","ton","coach","lock"]'
# Laden: Kauf-Knöpfe in Nuts gesperrt
rep('  rows.sort((p, q) => p[0] - q[0]);\n  CATS.forEach(',
    '  if (S.nuts) rows.forEach(r => { const m = r[1].match(/data-shop="(\\w+)"/), k = m && m[1]; if (k && ' + NZB + '.includes(k)) r[1] = r[1].replace(/<button data-shop="(\\w+)" class="([^"]*)"( disabled)?>[\\s\\S]*?<\\/button>/, `<button data-shop="$1" class="$2 off" disabled>NUTS<span class="lbl">no buying</span></button>`).replace(\'class="shopItem\', \'class="shopItem dis\'); });   /* V520 */\n  rows.sort((p, q) => p[0] - q[0]);\n  CATS.forEach(')
rep('  if (b.classList.contains("off")) { snd("nope"); return; }   /* V443: gesperrt / zu wenig Gold – nur Vorschau */',
    '  if (b.classList.contains("off")) { snd("nope"); return; }   /* V443: gesperrt / zu wenig Gold – nur Vorschau */\n  if (S.nuts && b.dataset.shop && ' + NZB + '.includes(b.dataset.shop)) { snd("nope"); toast("NUTS RULES · no shopping in the caves – starter kit + air drops only", "DENIED", 2200); return; }   /* V520 */')
# Specials-Kategorie: Untertitel in Nuts
rep('const CATS = [["TOWERS & WEAPONS", "Build a tower, add weapons", "cTow"], ["SPECIALS", "Buy, then USE – right here", "cSpe"],',
    'const CATS = [["TOWERS & WEAPONS", "Build a tower, add weapons", "cTow"], ["SPECIALS", S.nuts ? "Nuts: starter kit + air drops only · USE here" : "Buy, then USE – right here", "cSpe"],')
# kein Boss-Hack in Nuts
rep('function hkOfferOn() { return S && S.started && !S.over &&', 'function hkOfferOn() { return S && S.started && !S.over && !S.nuts &&')
rep('  if (S.hackPending && !S.drop &&', '  if (S.hackPending && !S.nuts && !S.drop &&')
# Hinweis am Nuts-Schild
rep('return `Left: a Nuts detour – empty field, ${NZ_KIT.gold} gold, ${NZ_KIT.lives} lives, ${NZ_MAX} levels, each harder. Your run waits here.`;',
    'return `Left: a Nuts detour – empty field, ${NZ_KIT.lives} lives, ${NZ_MAX} levels, each harder. Same kit for everyone: 2 of each special + air drops, no shopping. Gold only builds towers. Your run waits here.`;')
rep('const putAd = () => { const sh = document.getElementById("sheet"); if (!sh || sh.hidden) return;', 'const putAd = () => { const sh = document.getElementById("sheet"); if (!sh || sh.hidden || (typeof S !== "undefined" && S && S.nuts)) return;   /* V520: kein Coach-Angebot in Nuts */')
open(p, "w", encoding="utf-8").write(s); print("ok V520")
