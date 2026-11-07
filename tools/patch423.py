#!/usr/bin/env python3
# V423 (Martin 07.11. 23:21): Lücken nach W100 füllen – zusätzliche Sonderwellen W103 Hailstorm, W111 Sidewinder, W125 Siberia, W133 Sonar
# (statt 105/127: W105 hat schon Magnet, W127 Boss-Hack). Feste Wellen-Tabelle SPEC_ABS hat Vorrang vor dem 100er-Zyklus.
# Dazu W124 «Unkraut-Feld»: 5 Samen gleichzeitig in 5 verschiedenen Spalten. Unkraut intern jetzt als Liste (D.weeds), D.weed = erstes (Getter/Setter).
import sys
src, dst = sys.argv[1], sys.argv[2]
s = open(src, encoding="utf-8").read()
def rep(a, b, n=1):
    global s
    assert s.count(a) == n, (s.count(a), a[:80])
    s = s.replace(a, b)
rep('const GAME_VER = "V422";', 'const GAME_VER = "V423";')
# --- Sonderwellen ---
rep("function specBase(w = S.wave) { if (!(w >= 1)) return 0; const e = SPEC_AT[((w - 1) % 100) + 1]; return e ? e[0] : 0; }",
    "const SPEC_ABS = { 103: [12, 1], 111: [16, 1], 125: [18, 1], 133: [4, 1] };   /* V423: Lücken nach W100 */\n"
    "function specE(w = S.wave) { w = w || 1; return SPEC_ABS[w] || SPEC_AT[((w - 1) % 100) + 1] || null; }\n"
    "function specBase(w = S.wave) { if (!(w >= 1)) return 0; const e = specE(w); return e ? e[0] : 0; }")
rep("function specK(w = S.wave) { const e = SPEC_AT[(((w || 1) - 1) % 100) + 1],", "function specK(w = S.wave) { const e = specE(w),")
rep("{ const e = SPEC_AT[((S.wave - 1) % 100) + 1]; if (e && e[0] === 16 && S.inWave && e[1] >= 2)", "{ const e = specE(S.wave); if (e && e[0] === 16 && S.inWave && e[1] >= 2)")
rep("const e = SPEC_AT[((S.wave - 1) % 100) + 1]; return !!(e && RADIO_BASES.includes(e[0])", "const e = specE(S.wave); return !!(e && RADIO_BASES.includes(e[0])")
# --- Unkraut als Liste ---
rep("  const D = { blk: null, mag: null, weed: null, thief: null, done: {} };",
    "  const D = { blk: null, mag: null, weeds: [], thief: null, done: {} };\n"
    "  Object.defineProperty(D, \"weed\", { get() { return D.weeds[0] || null; }, set(v) { D.weeds = v ? [v] : []; } });   /* V423: mehrere Unkräuter */\n"
    "  const WEED5 = 124;")
rep('if (k === "weed") return [86, 110, 130].includes(w) && ', 'if (k === "weed") return (w === WEED5 || [86, 110, 130].includes(w)) && ')
rep('if (k === "weed") { let x = 2 + Math.floor(Math.random() * (GW - 4)); D.weed = { x, root: null, h: 0, seedY: -1, growT: 0, waves: 0 }; }',
    'if (k === "weed") { const n = S.wave === WEED5 ? 5 : 1, pool = []; for (let x = 1; x <= GW - 2; x++) pool.push(x);\n'
    '      for (let i = pool.length - 1; i > 0; i--) { const j = Math.floor(Math.random() * (i + 1)); [pool[i], pool[j]] = [pool[j], pool[i]]; }\n'
    '      const xs = n > 1 ? pool.slice(0, n).sort((a, b) => a - b) : [2 + Math.floor(Math.random() * (GW - 4))];\n'
    '      D.weeds = xs.map(x => ({ x, root: null, h: 0, seedY: -1, growT: Math.random() * 1.5, waves: 0 })); }')
rep('weed: ["WEEDS!", "Blocks get stuck on it · Tesla or Sniper cut it"]', 'weed: ["WEEDS!", "Blocks get stuck on it · Tesla or Sniper cut it"], weed5: ["WEED FIELD!", "Five seeds at once · Tesla or Sniper cut them"]')
rep('snd("siren"); announce(NAMES[k][0], NAMES[k][1], "ALERT", 2400);', 'snd("siren"); { const nm = k === "weed" && D.weeds.length > 1 ? NAMES.weed5 : NAMES[k]; announce(nm[0], nm[1], "ALERT", 2400); }')
rep("  function weedCells() { const w = D.weed; if (!w || w.root == null) return []; const a = []; for (let i = 0; i < w.h; i++) a.push([w.x, w.root - i]); return a; }",
    "  function weedCells(w) { w = w || D.weed; if (!w || w.root == null) return []; const a = []; for (let i = 0; i < w.h; i++) a.push([w.x, w.root - i]); return a; }")
rep("    if (D.weed && D.weed.root != null && !S.rotMode) { const w = D.weed; for (const [x, y] of cells) { const gx = px + x, gy = py + y; if (gx === w.x && gy <= w.root && gy > w.root - w.h) return true; } }",
    "    if (!S.rotMode) for (const w of D.weeds) { if (w.root == null) continue; for (const [x, y] of cells) { const gx = px + x, gy = py + y; if (gx === w.x && gy <= w.root && gy > w.root - w.h) return true; } }")
rep("  clearLines = function () { let below = 0;\n    if (D.weed && D.weed.root != null && !S.rotMode) for (let y = D.weed.root + 1; y < GH; y++) { let full = true; for (let x = 1; x < GW - 1; x++) if (!S.grid[y * GW + x]) { full = false; break; } if (full) below++; }\n    const r = _cl.apply(this, arguments); if (r && below && D.weed) D.weed.root += below; return r; };",
    "  clearLines = function () { const bl = D.weeds.map(w => { let below = 0; if (w.root != null && !S.rotMode) for (let y = w.root + 1; y < GH; y++) { let full = true; for (let x = 1; x < GW - 1; x++) if (!S.grid[y * GW + x]) { full = false; break; } if (full) below++; } return [w, below]; });\n    const r = _cl.apply(this, arguments); if (r) for (const [w, b] of bl) if (b && D.weeds.includes(w)) w.root += b; return r; };")
rep("    const W2 = D.weed; if (W2 && W2.root != null) { const cs = weedCells(); let low = null; cs.forEach(([x, y], i) => { if (x >= x0 && x < x0 + w && y >= y0 && y < y0 + h && low == null) low = i; });\n      if (low === 0) { D.weed = null; fxText(W2.x, W2.root, \"WEED PULLED!\", \"#9be36b\"); hit = true; } else if (low != null) { W2.h = low; fxText(W2.x, W2.root - low, \"WEED CUT\", \"#9be36b\"); hit = true; } }",
    "    for (const W2 of D.weeds.slice()) { if (W2.root == null) continue; const cs = weedCells(W2); let low = null; cs.forEach(([x, y], i) => { if (x >= x0 && x < x0 + w && y >= y0 && y < y0 + h && low == null) low = i; });\n      if (low === 0) { D.weeds = D.weeds.filter(q => q !== W2); fxText(W2.x, W2.root, \"WEED PULLED!\", \"#9be36b\"); hit = true; } else if (low != null) { W2.h = low; fxText(W2.x, W2.root - low, \"WEED CUT\", \"#9be36b\"); hit = true; } }")
rep("    if (D.weed) { const w = D.weed;\n      if (w.root == null)", "    for (const w of D.weeds) {\n      if (w.root == null)")
rep("      if (D.weed) drawWeed(D.weed, s);", "      for (const w of D.weeds) drawWeed(w, s);")
open(dst, "w", encoding="utf-8").write(s)
print("ok")
