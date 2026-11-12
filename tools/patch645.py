#!/usr/bin/env python3
# V645 (Martin 12.11. 08:15–08:33, Variante 3 «Rosenstein»): Anzeige nächster Stein im Spiel-Kopf –
# nur der nächste Stein (zweiter ausgeblendet), immer rosa, doppelte Steingröße +15 %, ohne weißes Feld,
# waagerecht mittig unter der Wellennummer (in Nuts ohne Wellennummer: Mitte des alten Feldes).
# Gilt überall (Web, RU-Spiegel → RuStore, TWA → Google Play).
# Dazu: Monster im Spielfeld 28 % größer, Bilder unverändert (Martin 08:35).
import sys, os
site = sys.argv[1]; p = os.path.join(site, "index.html"); s = open(p, encoding="utf-8").read()
def rep(a, b, n=1):
    global s
    c = s.count(a); assert c == n, (c, a[:90]); s = s.replace(a, b)
rep('const GAME_VER = "V644";', 'const GAME_VER = "V645";')
# Zeichnen: Leinwand darf breiter als hoch sein; Steine füllen sie; nächster Stein immer rosa (L-Farbe)
rep('const c = $(cvId), g = c.getContext("2d"), W = c.width; g.clearRect(0, 0, W, W);',
    'const c = $(cvId), g = c.getContext("2d"), W = c.width, H = c.height; g.clearRect(0, 0, W, H);   /* V645 */')
rep('cs = Math.floor(W / 4.4);', 'cs = Math.floor(Math.min(W / (w + 0.4), H / (h + 0.2), W / 4.4 * 2));')
rep('oy = (W - h * cs) / 2', 'oy = (H - h * cs) / 2')
rep('const set = CAMO[pc.col];', 'const set = cvId === "nextCv" ? CAMO[KEYS.indexOf("L")] : CAMO[pc.col];   /* V645: nächster Stein immer rosa */')
rep('<canvas id="nextCv" width="96" height="96"></canvas>', '<canvas id="nextCv" width="192" height="96"></canvas>')
# Darstellung im Spiel-Kopf
rep('body:has(.bar:not(.off)) .nextRow{gap:3px!important}',
    'body:has(.bar:not(.off)) .nextRow{gap:3px!important}\n'
    'html body:has(.bar:not(.off)) .bar .cell:has(.nextRow){background:none!important;border-color:transparent!important;box-shadow:none!important}'
    'html body:has(.bar:not(.off)) .bar #next2Cv{display:none!important}'
    'html body:has(.bar:not(.off)) .bar #nextCv{width:48px!important;height:24px!important;position:fixed;z-index:30;filter:drop-shadow(0 2px 0 rgba(58,36,20,.55))}   /* V645 */')
# Lage: mittig unter der Wellennummer, senkrecht in der Mitte des alten Feldes
rep('function drawNext() {',
    '(() => { const pos = () => { try { const c = document.getElementById("nextCv"), cell = c && c.closest(".cell"); if (!cell || document.querySelector(".bar.off")) return;\n'
    '  const g = cell.getBoundingClientRect(), wn = document.getElementById("waveNum"); let x = g.left + g.width / 2;\n'
    '  if (wn && getComputedStyle(wn).visibility !== "hidden" && wn.offsetWidth) { const r = wn.getBoundingClientRect(); x = r.left + r.width / 2; }\n'
    '  const L = Math.round(x - 24) + "px", T = Math.round(g.top + g.height / 2 - 12) + "px"; if (c.style.left !== L) c.style.left = L; if (c.style.top !== T) c.style.top = T; } catch (e) {} };\n'
    '  setInterval(pos, 250); addEventListener("resize", pos); })();   /* V645 */\n'
    'function drawNext() {')
# Monster im Spielfeld 28 % größer (Martin 08:35: gleiche Bilder, gleicher 3D-Look, nur größer; Treffer/Wege unverändert)
rep('const MON_R = {', 'const MON_FS = 1.28;   /* V645: Monster im Feld größer */\nconst MON_R = {')
rep('    drawMonster(ctx, m, cx, cy, s, now);\n    const r = s * MON_R[k];',
    '    drawMonster(ctx, m, cx, cy, s * MON_FS, now);\n    const r = s * MON_FS * MON_R[k];')
open(p, "w", encoding="utf-8").write(s)
print("ok V645")
