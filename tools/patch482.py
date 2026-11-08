#!/usr/bin/env python3
"""V482 – Linearer Anstieg über alle 150 Wellen (Martin 08.11. 23:08/23:12): alle Korrekturstufen (×0,55 ab W21, HP-Faktoren 0,7/0,6/0,55/0,7/0,4,
Stufen ×1,15/×1,25, Kontinent-Rabatte, Tempo-Bremsen) sind im Hauptspiel ersetzt durch Geraden vom Startwert W1 zum Endwert W150:
  Anzahl 11 → 65 · Leben (Grunt) 15,6 → 1 320,8 · Tempo (Grunt) 1,28 → 1,67 · Anführer ab W6 jedes 6., ab W57 jedes 5. Monster (bis W150).
Nuts-Abstecher unverändert (eigene Formeln). Nutzung: python3 tools/patch482.py src dst"""
import sys, re
src, dst = sys.argv[1], sys.argv[2]
s = open(src, encoding="utf-8").read()
def rep(a, b, n=1):
    global s
    c = s.count(a); assert c == n, (c, a[:80]); s = s.replace(a, b)
m = re.search(r'const GAME_VER = "V(\d+)";', s); v = int(m.group(1))
rep(m.group(0), f'const GAME_VER = "V{v + 1}";\n'
    'const LIN = { n: [11, 65], hp: [15.6, 1320.8], sp: [1.28, 1.67] };   /* V482: Start W1 → Ende W150, linear (Martin 08.11.) */\n'
    'function lin(k, w) { const a = LIN[k]; return a[0] + (a[1] - a[0]) * (Math.max(1, Math.min(150, w)) - 1) / 149; }')
# Leben
rep('''  const hp = ordv("monHpMul") * (w >= 50 ? 1.25 : w >= 20 ? 1.15 : 1) * (S.nuts ? 1 : w >= 91 && w <= 100 ? 0.75 : w >= 101 && w <= 110 ? 0.75 : w >= 111 && w <= 120 ? 0.85 : w >= 121 && w <= 150 ? 0.90 : 1) * (!S.nuts && w >= 21 && w <= 150 ? (w <= 30 ? 0.7 : w <= 60 ? 0.6 : w <= 90 ? 0.55 : w <= 120 ? 0.7 : 0.4) : 1) * baseHp * ({''',
    '''  const hp = ordv("monHpMul") * (S.nuts ? (w >= 50 ? 1.25 : w >= 20 ? 1.15 : 1) * baseHp : lin("hp", w)) * ({''')
# Tempo
rep('''  const sp = ordv("monSpdMul") * (!S.nuts && w >= 21 && w <= 150 ? (w <= 30 ? 0.85 : w <= 60 ? 0.8 : 0.65) : 1) * Math.min(G.spMax, G.spBase + G.spGrow * w) * ({''',
    '''  const sp = ordv("monSpdMul") * (S.nuts ? Math.min(G.spMax, G.spBase + G.spGrow * w) : lin("sp", w)) * ({''')
# Anzahl
rep('''  S.toSpawn = Math.max(1, Math.round(Math.min(L.monsters, G.waveBase + G.wavePer * S.wave) * (!S.nuts && S.wave >= 21 && S.wave <= 150 ? 0.55 : 1)) + (!S.nuts && S.wave >= 10 ? 1 : 0));   /* V457: ab W10 +1 Monster */''',
    '''  S.toSpawn = S.nuts ? Math.max(1, Math.round(Math.min(L.monsters, G.waveBase + G.wavePer * S.wave))) : Math.round(lin("n", S.wave));   /* V482: linear 11 → 65 (Nuts: eigene Zahl unten) */''')
# Anführer
rep('''    if (!S.nuts && S.wave >= 6 && S.wave <= 40) for (let i = n0; i < S.monsters.length; i++) { const m = S.monsters[i]; S.ldN = (S.ldN || 0) + 1;   /* V463: Anführer */
      if (S.ldN % 6 === 0 && !m.boss) {''',
    '''    if (!S.nuts && S.wave >= 6) for (let i = n0; i < S.monsters.length; i++) { const m = S.monsters[i]; S.ldN = (S.ldN || 0) + 1;   /* V463: Anführer · V482: ab W6 jedes 6., ab W57 jedes 5. */
      if (S.ldN % (S.wave >= 57 ? 5 : 6) === 0 && !m.boss) {''')
# Erwartungswert für Statistik (expK)
rep('''const expK = w => { try { return Math.min(limits(w).monsters, G.waveBase + G.wavePer * w) * (w >= 21 ? 0.55 : 1) * 0.95; } catch (e) { return 10; } };''',
    '''const expK = w => { try { return lin("n", w) * 0.95; } catch (e) { return 10; } };   /* V482 */''')
# Unkraut: W126 und W136 wachsen 30 % schneller (Martin 08.11. 23:14)
rep('''  const WEEDN = { 106: 3, 126: 4, 136: 5 };   /* V426: am Ortsanfang */''',
    '''  const WEEDN = { 106: 3, 126: 4, 136: 5 };   /* V426: am Ortsanfang */
  const WEEDSPD = { 126: 1.3, 136: 1.3 };   /* V482: Wachstum +30 % (Martin 08.11.) */''')
rep('''D.weeds = xs.map(x => ({ x, root: null, h: 0, seedY: -1, growT: Math.random() * 1.5, waves: 0, delay: dl + Math.random() * 0.4 }));''',
    '''D.weeds = xs.map(x => ({ x, root: null, h: 0, seedY: -1, growT: Math.random() * 1.5, waves: 0, delay: dl + Math.random() * 0.4, gi: 6.8 / (WEEDSPD[S.wave] || 1) }));''')
rep('''if (w.growT >= 6.8) {''', '''if (w.growT >= (w.gi || 6.8)) {''')
rep('''else w.growT = 6.8; }''', '''else w.growT = (w.gi || 6.8); }''')
s = s.replace('"""V482 – Linearer Anstieg', '"""V482 – Linearer Anstieg (+ Unkraut W126/W136 wächst 30 % schneller)', 1)
open(dst, "w", encoding="utf-8").write(s); print("ok", v + 1)
