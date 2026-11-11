#!/usr/bin/env python3
# V627 (Martin 11.11. 13:39/13:40):
# 1) Score-, Herz/Gold- und Steine-Feld wackelten 1–2 px: placeDJ richtete sie nach dem Bildrand des Generals aus, der sich dreht (genIdle).
#    Jetzt Layoutmaße (style.left + offsetWidth) statt getBoundingClientRect → Felder stehen fest.
# 2) Musik-Wächter: nach jeder Absenkung (Durchsagen, Tipps, Laden, Duell) zurück auf den Standardpegel, sobald kein Ausblenden mehr läuft.
#    Zusätzlich window.__TPdbg() für die Pegelmessung.
# 3) Erster (Gratis-)Boss-Hack: bei 6:6 kein zweites Duell.
import sys, os
site = sys.argv[1]; p = os.path.join(site, "index.html"); s = open(p, encoding="utf-8").read()
def rep(a, b, n=1):
    global s
    c = s.count(a); assert c == n, (c, a[:90]); s = s.replace(a, b)
rep('const GAME_VER = "V626";', 'const GAME_VER = "V627";')
rep('gR = ga && ga.getBoundingClientRect().width ? ga.getBoundingClientRect().right : 64',
    'gR = ga && ga.offsetWidth ? (parseFloat(ga.style.left) || 4) + ga.offsetWidth : 64')   # V627: Drehung des Generals verschiebt nichts mehr
rep('function tpFade(to, sec) { const a = TP.el; if (!a) return; clearInterval(tpFadeT);',
    'function tpFade(to, sec) { const a = TP.el; if (!a) return; TP.want = to; clearInterval(tpFadeT);')
rep('let tpFadeT = null;', '''let tpFadeT = null;
setInterval(() => { try { const a = TP.el; if (!a || !TP.key || TP.paused || TP.stopping || TP.pend || a.paused || tpFadeT !== null || !(TP.want == null || TP.want >= 0.5)) return;
  const t = TP_VOL(); if (Math.abs(a.volume - t) > 0.02) tpFade(0.5, 0.8); } catch (e) {} }, 1000);   /* V627: Musik-Wächter – immer zurück auf Standardpegel */
window.__TPdbg = () => { try { return { vol: TP.el ? +TP.el.volume.toFixed(3) : null, std: +TP_VOL().toFixed(3), want: TP.want, paused: !!TP.paused, elPaused: TP.el ? TP.el.paused : null, key: TP.key, fading: tpFadeT !== null }; } catch (e) { return null; } };''')
rep('if (mine === 6) { toast("DRAW · 6 : 6 · the circuit rewires", "HACK", 1800); startDuel(true); return; }',
    'if (mine === 6 && !window.__hkFree) { toast("DRAW · 6 : 6 · the circuit rewires", "HACK", 1800); startDuel(true); return; }   /* V627: Gratis-Hack nur einmal */')
rep('try { if (hb.classList.contains("hkFirst") && !S.testRun) LS.set("capy-hk-first", "1");', 'try { window.__hkFree = hb.classList.contains("hkFirst") ? 1 : 0; if (hb.classList.contains("hkFirst") && !S.testRun) LS.set("capy-hk-first", "1");')
open(p, "w", encoding="utf-8").write(s)
print("ok V627")
