#!/usr/bin/env python3
"""V421 (Martin 07.11. 23:03 «alle vertonen»): 17 neue Blue-Sprechblasen (voice/lines11.json, HeyGen «Martin 4min», 44,6 s, 0,015 $).
Regeln wie V331 (rbSay): max. 1 je 20 s, jeder Spruch max. alle 4 min, nie bei offenem Fenster (Hack-Ergebnis mit force).
Auslöser: 1. Turm · MAXED OUT · 3 leere Türme · 2. Durchbruch · Gold ≥ 600 ohne Kauf 2 Wellen · Sniper ≥ 3 · Tesla · Lockdown · Chomper frisst ·
Wolf vertreibt Dieb · Dieb entkommt · Hack gewonnen/verloren · Stapel ≥ 14 mit Ten-ton · Checkpoint · Nacht beginnt · neuer Kontinent."""
import sys, json, base64, os
src, dst = sys.argv[1], sys.argv[2]
s = open(src, encoding='utf-8').read()
def rep(a, b, cnt=1):
    global s
    n = s.count(a); assert n == cnt, (n, a[:70]); s = s.replace(a, b)
rep('const GAME_VER = "V420";', 'const GAME_VER = "V421";')
VD = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'voice')
L = json.load(open(os.path.join(VD, 'lines11.json'), encoding='utf-8'))
vt = ''.join(f'{json.dumps(k)}: {json.dumps(t)}, ' for k, t in L.items())
vb = ''.join(f'"{k}":"' + base64.b64encode(open(os.path.join(VD, k + '.mp3'), 'rb').read()).decode() + '",' for k in L)
rep('const VOICE_TEXT = {', 'const VOICE_TEXT = {' + vt)
rep('const VOICE = {', 'const VOICE = {' + vb)
# Haken mitten im Code
rep('S.towers.set(c, t); S.mode = null; snd("build"); openSheet(t); S.towersBuilt++;',
    'S.towers.set(c, t); S.mode = null; snd("build"); openSheet(t); S.towersBuilt++; S.lastBuyW = S.wave; if (S.towersBuilt === 1 && window.__rbSay) setTimeout(() => window.__rbSay("rb_tower1"), 1500);   /* V421 */')
rep('m.dead = true; S.lives--; S.waveLeaks++; snd("leak"); loseMedal();',
    'm.dead = true; S.lives--; S.waveLeaks++; snd("leak"); loseMedal(); if (S.waveLeaks === 2 && window.__rbSay) window.__rbSay("rb_gap");   /* V421 */')
JS = r'''
  /* V421: 17 weitere Sprüche */
  const _pr2 = praise; praise = function (text) { const r = _pr2.apply(this, arguments); try { if (text === "MAXED OUT") rbSay("rb_maxed", 1200); } catch (e) {} return r; };
  const _to2 = toast; toast = function (msg) { const r = _to2.apply(this, arguments); try { const m = String(msg || "");
    if (/WOLF SCARED HIM OFF/.test(m)) rbSay("rb_wolfgone", 1600); else if (/THIEF GOT AWAY/.test(m)) rbSay("rb_stolen", 1200); else if (/^CHECKPOINT/.test(m)) rbSay("rb_checkpoint", 2200); } catch (e) {} return r; };
  const _sn2 = snd; snd = function (k) { try { if (S && (k === "shopBuy" || k === "build")) S.lastBuyW = S.wave; } catch (e) {} return _sn2.apply(this, arguments); };
  const _sp2 = snipe; snipe = function () { const k0 = S.kills || 0; const r = _sp2.apply(this, arguments); try { if ((S.kills || 0) - k0 >= 3) rbSay("rb_showoff", 1400); } catch (e) {} return r; };
  const _te2 = tesla; tesla = function () { const r = _te2.apply(this, arguments); try { rbSay("rb_lightup", 400); } catch (e) {} return r; };
  const _lk2 = startLock; startLock = function () { const n0 = S.locks || 0; const r = _lk2.apply(this, arguments); try { if ((S.locks || 0) < n0) rbSay("rb_doors", 900); } catch (e) {} return r; };
  const _hf2 = hkFinish; hkFinish = function () { const r = _hf2.apply(this, arguments); try { if (HK.phase === "done" && !HK.coach) { const win = HK.cells.filter(c => c === HK.me).length > 6; rbSay(win ? "rb_hacked" : "rb_lucky", 2600, true); } } catch (e) {} return r; };
  const _sw2 = startWave; startWave = function () { const r = _sw2.apply(this, arguments); try { if (S.nuts || S.testRun && false) return r; const w = S.wave | 0;
    if (w > 1 && (w - 1) % 30 === 0) rbSay("rb_newground", 7000);
    else { const night = (DAY[wherePos(w).d] || {}).night > 0, prev = (DAY[wherePos(Math.max(1, w - 1)).d] || {}).night > 0; if (night && !prev) rbSay("rb_night", 3500);
      else setTimeout(() => { if (!S.inWave) return; let empty = 0; for (const t of S.towers.values()) if (!t.w.length) empty++;
        if (empty >= 3) rbSay("rb_empty"); else if ((S.gold || 0) >= 600 && w - (S.lastBuyW || 0) >= 2 && w > 3) rbSay("rb_dust"); }, 4500); } } catch (e) {} return r; };
  setInterval(() => { try { if (!S || !S.started || S.over || S.nuts) return;
    if (S.chomp && S.chomp.eaten >= 1 && !S.chomp._said) { S.chomp._said = true; rbSay("rb_picky", 300); }
    if (S.inWave && (S.tons || 0) > 0 && !S.ton && stackHeight() >= 14) rbSay("rb_weight"); } catch (e) {} }, 700);
'''
rep('  window.__rbSay = (k, f) => rbSay(k, 0, f);', '  window.__rbSay = (k, f) => rbSay(k, 0, f);' + JS)
open(dst, 'w', encoding='utf-8').write(s)
print('ok', len(L))
