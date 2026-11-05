"""V249: Musik pausiert im Pausemenü auch ab Welle 31 (Afrika/Asien-Stücke fehlten in TRK_ORDER → playing war 0 → nie pausiert);
Fade-out beim Pausieren 1,5 s (Regel Martin 05.11.: Musik blendet im Pausemenü innerhalb von 2 s aus, beim Weiterspielen geht sie weiter).
Kontinentwechsel – das Flugzeug fliegt genau vom letzten Ort des alten Kontinents zum ersten Ort des neuen
(dort, wo man startet) und landet auf dem rosa Punkt; der rosa Punkt erscheint im Moment der Landung (vorher flog es
von Kontinentmitte zu Kontinentmitte und der Punkt kam erst 1,2 s später woanders)."""
import sys
src, dst = sys.argv[1], sys.argv[2]
s = open(src, encoding='utf-8').read()
def rep(a, b, cnt=1):
    global s
    n = s.count(a); assert n == cnt, (n, a[:70]); s = s.replace(a, b)
rep('const GAME_VER = "V248";', 'const GAME_VER = "V249";')
rep('flyPlane(cen(oc), cen(P.c), 3000); });', 'flyPlane(MAP_PTS[oc][5], MAP_PTS[P.c][0], 3000); });\n      at(7420, () => { setMe(MAP_PTS[P.c][0], true); });')
rep('d("playing", () => TP.key ? (TP.wave === 0 ? 0 : TRK_ORDER.indexOf(TP.key) + 1) : gp.call(M));', 'd("playing", () => TP.key ? (TP.wave === 0 ? 0 : (TRK_ORDER.indexOf(TP.key) < 0 ? 90 : TRK_ORDER.indexOf(TP.key) + 1)) : gp.call(M));')
rep('if (pz) { tpFade(0.0001, 0.3); setTimeout(() => { if (TP.paused) TP.el.pause(); }, 320); }', 'if (pz) { tpFade(0.0001, 1.5); setTimeout(() => { if (TP.paused) TP.el.pause(); }, 1600); }')
rep('bus.gain.exponentialRampToValueAtTime(pz ? 0.0001 : LVL * sonarLvl, ac.currentTime + 0.25);', 'bus.gain.exponentialRampToValueAtTime(pz ? 0.0001 : LVL * sonarLvl, ac.currentTime + (pz ? 1.5 : 0.25));')
open(dst, 'w', encoding='utf-8').write(s); print('ok')
