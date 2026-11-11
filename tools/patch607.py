#!/usr/bin/env python3
# V607 (Martin 11.11. 08:37/08:38): General-Meldungen um ~75 % reduzieren, höchstens 1 pro 25 s.
# Bleibt (ohne Wartezeit, setzt aber die 25 s neu): Warnungen (ALERT/SYSTEM/HACK), neuer Kontinent, neue Monster (INCOMING), Spezialwellen
# (Sonar, Hagel, Laser, Lockdown), Boss, Mission erfüllt, Monster-Rush, Checkpoint, Tutorial fertig, Elite-Turm.
# Fällt immer weg: REINFORCEMENTS, Entwarnungen (WEEDS WITHERED, SIGNAL BACK, MAGNET GONE), HQ SUPPLY, 3 MISSIONS FOR YOU.
# Orts-/Tageszeit-Ansage nur noch beim Ortswechsel (nicht mehr jede Welle). Alles andere: nur wenn seit der letzten General-Meldung ≥ 25 s.
# Buchhalter und Tutorial unverändert.
import sys
src, dst = sys.argv[1], sys.argv[2]
s = open(src, encoding="utf-8").read()
def rep(a, b, n=1):
    global s
    c = s.count(a); assert c == n, (c, a[:90]); s = s.replace(a, b)
rep('const GAME_VER = "V606";', 'const GAME_VER = "V607";')
rep('''  try { if (certQuiet() && m.title !== "MONSTER RUSH!") return; } catch (e) {}   /* V595 · V600: Rush-Banner darf */''',
    '''  try { if (certQuiet() && m.title !== "MONSTER RUSH!") return; } catch (e) {}   /* V595 · V600: Rush-Banner darf */
  try { if (S && S.started && !(typeof TUT !== "undefined" && TUT.on) && m.kind !== "book") {   /* V607: General höchstens 1 pro 25 s */
      const T = String(m.title || ""), tg = String(m.tag || "");
      if (/^(REINFORCEMENTS|WEEDS WITHERED|SIGNAL BACK|MAGNET GONE|HQ SUPPLY|3 MISSIONS FOR YOU)/.test(T)) return;
      const vip = tg === "ALERT" || tg === "SYSTEM" || tg === "HACK" || /^(WELCOME TO|INCOMING|MISSION COMPLETE|BOSS|NEW:|MONSTER RUSH|TUTORIAL DONE|CHECKPOINT|SONAR MODE|HAILSTORM|LASER SHOW|LOCKDOWN|ELITE TOWER|WORLD TOUR COMPLETE)/.test(T);
      const now = performance.now(); if (!vip && now - (window.__genT || -1e9) < 25000) return; window.__genT = now; } } catch (e) {}''')
rep('toast(P.d === 0 ? `${P.place} · ${D.t} ${D.n}` : `${D.t} · ${D.n}`, P.d === 0 ? P.cont[1] : P.place, 1700);',
    'if (P.d === 0) toast(`${P.place} · ${D.t} ${D.n}`, P.cont[1], 1700);   /* V607: nur beim Ortswechsel */')
open(dst, "w", encoding="utf-8").write(s)
print("ok", dst)
