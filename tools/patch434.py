#!/usr/bin/env python3
# V434 (/neu-Chat, Martins Kommentar zu To-do 90): Windrose auf der Weltkarte im Comic-Stil (dicke braune Kontur, Comic-Buchstaben,
# rosa/gelbe Spitzen, leicht schräg), Zahlen darunter in der Comic-Schrift; Fragezeichen auf den Totenkopf-Gebieten entfernt.
import sys
src, dst = sys.argv[1], sys.argv[2]
s = open(src, encoding="utf-8").read()
def rep(a, b, n=1):
    global s
    assert s.count(a) == n, (s.count(a), a[:80])
    s = s.replace(a, b)

rep('const GAME_VER = "V433";', 'const GAME_VER = "V434";')
rep('''${b ? "" : '<text x="41" y="34" text-anchor="middle" class="nzQ">?</text>'}''', '''''')
OLD = '''r.innerHTML = `<svg viewBox="0 0 60 60" aria-hidden="true"><circle cx="30" cy="30" r="27" fill="#f3ead6" stroke="#3a2414" stroke-width="2.5"/><path d="M30 5 L35 30 L30 55 L25 30Z" fill="#3a2414"/><path d="M30 5 L35 30 L25 30Z" fill="#e0412c"/><path d="M5 30 L30 25 L55 30 L30 35Z" fill="#7a6a52"/><circle cx="30" cy="30" r="3.5" fill="#ffc93c" stroke="#3a2414" stroke-width="1.5"/><text x="30" y="14" text-anchor="middle" font-size="8" font-weight="700" fill="#fff">N</text></svg>'''
NEW = '''r.innerHTML = `<svg viewBox="0 0 64 64" aria-hidden="true"><g transform="rotate(-6 32 32)"><circle cx="32" cy="32" r="28" fill="#3a2414"/><circle cx="31" cy="31" r="26" fill="#fff6e6" stroke="#3a2414" stroke-width="2"/><path d="M32 8 L36 28 L56 32 L36 36 L32 56 L28 36 L8 32 L28 28Z" fill="#ffc93c" stroke="#3a2414" stroke-width="2.4" stroke-linejoin="round"/><path d="M32 8 L36 28 L28 28Z" fill="#ff6fb5" stroke="#3a2414" stroke-width="2.4" stroke-linejoin="round"/><path d="M17 17 L30 29 L21 23Z M47 17 L34 29 L43 23Z M47 47 L34 35 L43 41Z M17 47 L30 35 L21 41Z" fill="#3a2414"/><circle cx="32" cy="32" r="4.5" fill="#fff6e6" stroke="#3a2414" stroke-width="2.2"/><text x="32" y="13" text-anchor="middle" font-family="Bangers,Impact,system-ui" font-size="11" fill="#fff6e6" stroke="#3a2414" stroke-width="2.2" paint-order="stroke" transform="rotate(6 32 32)">N</text></g></svg>'''
rep(OLD, NEW)
rep('.mapRose{position:absolute;right:max(10px,env(safe-area-inset-right,0px));bottom:calc(env(safe-area-inset-bottom,0px) + 70px);z-index:5;display:flex;flex-direction:column;align-items:center;gap:2px;pointer-events:none;font:700 11px/1.1 system-ui,sans-serif;color:#fff;text-shadow:0 1px 2px #000',
    '.mapRose{position:absolute;right:max(10px,env(safe-area-inset-right,0px));bottom:calc(env(safe-area-inset-bottom,0px) + 70px);z-index:5;display:flex;flex-direction:column;align-items:center;gap:2px;pointer-events:none;font:400 12px/1.1 Bangers,Impact,system-ui,sans-serif;letter-spacing:.5px;color:#fff6e6;-webkit-text-stroke:.6px #3a2414;text-shadow:1px 2px 0 #3a2414')
rep('.mapRose svg{width:54px;height:54px;filter:drop-shadow(0 2px 3px rgba(0,0,0,.5))}', '.mapRose svg{width:60px;height:60px;filter:drop-shadow(2px 3px 0 rgba(58,36,20,.55))}')
rep('.mapRose .rsTot{font-size:13px;color:#ffc93c}', '.mapRose .rsTot{font-size:16px;color:#ffc93c}')
rep('.mapRose .rsCnt{font-size:9px;opacity:.9;text-align:center;line-height:1.25}', '.mapRose .rsCnt{font-size:10px;opacity:.95;text-align:center;line-height:1.25;letter-spacing:.3px}')
rep('.mapRose .rsNuts{font-size:11px;color:#ff6fb5}', '.mapRose .rsNuts{font-size:12px;color:#ff6fb5}')
open(dst, "w", encoding="utf-8").write(s)
print("ok")
