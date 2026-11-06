"""V314: Vorrang für Lucky Supply / Rufzeichen wirksam machen (Testlauf V311, 06.11.).
Gemessen mit V311 (Takt 95 s + Vorrang): Lucky Supply W2, W7, dann erst W47/W55; Rufzeichen W17 (vorher W44).
Ursache: Die Sicherung ließ Sale-Anzeigen schon nach 1 Welle wieder durch, und Boss-Hack-Anzeigen achteten gar nicht
auf den Vorrang – Lucky Supply darf aber nur in der kurzen Wellenpause kommen und fand so kaum einen freien Takt.
Jetzt: Sale-Anzeigen warten bis zu 4 Wellen; Boss-Hack wartet ebenfalls, solange Lucky/Rufzeichen fällig sind,
außer er ist schon 2 Wellen überfällig (bestehende Ausnahme)."""
import sys
src, dst = sys.argv[1], sys.argv[2]
s = open(src, encoding='utf-8').read()
def rep(a, b, cnt=1):
    global s
    n = s.count(a); assert n == cnt, (n, a[:70]); s = s.replace(a, b)

rep('const GAME_VER = "V313";', 'const GAME_VER = "V314";')
rep('if ((S.wave || 0) <= S.prioW + 1) return;', 'if ((S.wave || 0) <= S.prioW + 4) return;   /* V314: bis zu 4 Wellen */')
rep('window.__offerOK((S.wave || 0) >= S.hackPending + 2)) {',
    'window.__offerOK((S.wave || 0) >= S.hackPending + 2) && ((S.wave || 0) >= S.hackPending + 2 || !(window.__prioDue && window.__prioDue()))) {   /* V314: Boss-Hack lässt Lucky/Rufzeichen vor */')
open(dst, 'w', encoding='utf-8').write(s)
print("ok")
