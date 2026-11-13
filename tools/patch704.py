# V704 (Martin 13.11. 23:40): Tipp «USE YOUR SPECIAL» (tontut) nur bis Welle 15.
# Ab W16 wird der Tipp still als erledigt markiert; geschenkte Specials landen ohne Fenster in der Tasche.
import sys
src, dst = sys.argv[1], sys.argv[2]
s = open(src, encoding="utf8").read()
def rep(a, b, n=1):
    global s; c = s.count(a); assert c == n, (a[:80], c); s = s.replace(a, b)
rep('GAME_VER = "V703"', 'GAME_VER = "V704"')
rep('if (LS.get("capy-tut-sp") === "1") return;',
    'if (LS.get("capy-tut-sp") === "1") return;\n    if ((S.wave | 0) > 15) { try { LS.set("capy-tut-sp", "1"); } catch (e) {} return; }   /* V704: nur bis W15 */')
open(dst, "w", encoding="utf8").write(s)
print("ok V704")
