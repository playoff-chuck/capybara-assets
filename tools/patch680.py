# V680 (Martin 12.11. 18:26, Foto): Boss-Hack zeigte ab dem 3. Hack ein leeres Einsatz-Fenster (nur Bild, «BOSS», «HACK!»,
# ohne Einsatz und ohne Skip). Ursache: first() lieferte nach dem ersten Hack «undefined» statt false;
# classList.toggle("hkFirst", undefined) schaltet dann bei jedem Aufruf um, statt die Klasse zu entfernen –
# jedes zweite Mal blieb die Erst-Hack-Ansicht (Einsatz, Chips, Skip versteckt) stehen, und «HACK!» setzte unbemerkt 25 % Gold.
import sys
src, dst = sys.argv[1], sys.argv[2]
s = open(src, encoding="utf8").read()
def rep(a, b, n=1):
    global s; c = s.count(a); assert c == n, (a[:60], c); s = s.replace(a, b)
rep('try { const f = first(); hb.classList.toggle("hkFirst", f); fst.hidden = !f;',
    'try { const f = !!first(); hb.classList.toggle("hkFirst", f); fst.hidden = !f;   /* V680: immer true/false */')
rep('const GAME_VER = "V679"', 'const GAME_VER = "V680"')
open(dst, "w", encoding="utf8").write(s); print("ok", len(s))
