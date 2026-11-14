import sys
# V712: Nordamerika (und jeder nächste Kontinent) ist beim Hinflug und danach nicht mehr grau/gesperrt (Martin 14.11.2026 22:31: «Flugzeug flog in den gesperrten Kontinent»).
#  Grau galt bisher bis Bestwelle ≥ Kontinent×30+1; die Bestwelle (Checkpoint) hinkt aber hinterher. Jetzt zählt auch die laufende Welle.
#  Dazu: Brett-Wackeln beim Kippen nur noch nach oben/seitlich (Knöpfe darunter werden nicht berührt, Megatest B13).
src, dst = sys.argv[1], sys.argv[2]
s = open(src, encoding="utf-8").read()
def rep(a, b, n=1):
    global s
    c = s.count(a); assert c == n, (a[:60], c); s = s.replace(a, b)
rep('const GAME_VER = "V711";', 'const GAME_VER = "V712";')
rep('let b = 0; try { b = dailyBestW(); } catch (e) {} return b < c * 30 + 1; }   /* V636 */',
    'let b = 0; try { b = dailyBestW(); } catch (e) {} try { if (S && S.started && !S.nuts && !S.testRun) b = Math.max(b, (S.wave | 0) + 1); } catch (e) {} return b < c * 30 + 1; }   /* V636 · V712: laufende Welle zählt mit */')
rep('@keyframes tiltShake{0%,100%{translate:0 0}25%{translate:4px -3px}50%{translate:-4px 2px}75%{translate:3px 3px}}',
    '@keyframes tiltShake{0%,100%{translate:0 0}25%{translate:4px -3px}50%{translate:-4px -1px}75%{translate:3px -2px}}')
open(dst, "w", encoding="utf-8").write(s)
print("ok")
