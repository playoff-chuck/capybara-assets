"""V193: Suno-Musik Afrika (W31–60) und Asien (W61–90), Meldungs-Schlange hängt nach Air Drop nicht mehr
(General-Sprechblasen gingen verloren), Knopf «verpasste Boss-Hacks» rechts neben der Wellen-Nummer."""
import sys
src, dst = sys.argv[1], sys.argv[2]
s = open(src, encoding='utf-8').read()
def rep(a, b, cnt=1):
    global s
    n = s.count(a); assert n == cnt, (n, a[:70]); s = s.replace(a, b)

rep('const GAME_VER = "V192";', 'const GAME_VER = "V193";')

# Musik
rep('loungedisco: ["Lounge Disco", 110] };', 'loungedisco: ["Lounge Disco", 110], oasis: ["Oasis Blues", 98], savanna: ["Savanna Groove", 104], dune: ["Dune Dub", 96], dune2: ["Dune Dub II", 96], pyramid: ["Pyramid Disco", 116], taiga: ["Taiga Lounge", 100], frozen: ["Frozen Lake", 96], steppe: ["Steppe Ride", 108], iceport: ["Ice Port Disco", 110], icepalace: ["Ice Palace", 120] };')
rep('loungedisco: "lounge_disco" };', 'loungedisco: "lounge_disco", oasis: "af_oasis", savanna: "af_savanna", dune: "af_dune", dune2: "af_dune2", pyramid: "af_pyramid", taiga: "as_taiga", frozen: "as_frozen", steppe: "as_steppe", iceport: "as_iceport", icepalace: "as_icepalace" };')
rep('function trkPool(wave) { if (!wave) return ["airport"]; const p = Math.floor(((wave - 1) % 30) / 5); return TRK_ORDER.slice(p, p + 3); }',
    'const TRK_AF = ["oasis", "savanna", "dune", "dune2", "pyramid"], TRK_AS = ["taiga", "frozen", "steppe", "iceport", "icepalace"];\n'
    'function trkPool(wave) { if (!wave) return ["airport"]; const p = Math.floor(((wave - 1) % 30) / 5);\n'
    '  if (wave >= 31 && wave <= 60) return [0, 1, 2].map(i => TRK_AF[(p + i) % 5]); if (wave >= 61 && wave <= 90) return [0, 1, 2].map(i => TRK_AS[(p + i) % 5]);\n'
    '  return TRK_ORDER.slice(p, p + 3); }')
rep('const useTrk = w => w === 0 || (w >= 1 && w <= 30);', 'const useTrk = w => w === 0 || (w >= 1 && w <= 90);')

# Meldungs-Schlange: während Air Drop warten statt liegen bleiben; hängender Drop nach 9 s freigeben
rep('  if (S && S.drop) return;                                               // Air Drop hat Vorrang, danach weiter',
    '  if (S && S.drop) { const now = performance.now(); if (!S._dropAt) S._dropAt = now; if (now - S._dropAt < 9000) { setTimeout(msgTick, 400); return; } S.drop = false; }   // V193: Air Drop hat Vorrang, dann weiter (nicht liegen bleiben)\n  if (S) S._dropAt = 0;')

# Verpasste Boss-Hacks: rechts neben der Wellen-Nummer statt darunter
rep('b.style.left = Math.round(r.left + r.width / 2 - b.offsetWidth / 2) + "px"; b.style.top = Math.round(r.bottom + 3) + "px"; }, 250); })();',
    'b.style.left = Math.round(Math.min(window.innerWidth - b.offsetWidth - 4, r.right + 4)) + "px"; b.style.top = Math.round(r.top + r.height / 2 - b.offsetHeight / 2) + "px"; }, 250); })();')

open(dst, 'w', encoding='utf-8').write(s); print('ok', dst)
