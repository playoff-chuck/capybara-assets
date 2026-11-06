"""V340 (Martin 06.11. 23:50, Screenshots): Reste der Sprechblasen von Rosie/Blue hingen am Bildschirmrand («THAT ON…», «BIG…», «BUILD.»).
Ursache: die Sprechblase ist breiter als die Figur; beim Wegfahren (−130 % der Figurbreite) blieb ein Stück im Bild.
Jetzt blendet die Sprechblase beim Wegfahren aus und ist versteckt, solange die Figur weg ist."""
import sys
src, dst = sys.argv[1], sys.argv[2]
s = open(src, encoding='utf-8').read()
def rep(a, b, cnt=1):
    global s
    n = s.count(a); assert n == cnt, (n, a[:70]); s = s.replace(a, b)
rep('const GAME_VER = "V339";', 'const GAME_VER = "V340";')
rep('#buddy.l .say::after{left:30%}', '#buddy.l .say::after{left:30%}\n#buddy:not(.on) .say{opacity:0;visibility:hidden;transition:opacity .2s,visibility 0s .2s}\n#buddy.on .say{opacity:1;visibility:visible;transition:opacity .15s .1s}')
open(dst, 'w', encoding='utf-8').write(s)
print("ok")
