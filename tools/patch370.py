"""V370 (Martin 07.11., Bildschirmvideo): Flug «zeigt ihn, stockt, zeigt ihn noch einmal».
Ursache: (1) Kamera-Schwenks (go mit Dauer) liefen als CSS-Übergang, die Flugzeug-Verfolgung setzte die Kamera aber jedes Bild
ohne Übergang -> das Bild sprang hart ans Schwenk-Ende. Die Sperre window.__camHold wurde nie gesetzt.
(2) Der Welttour-Start zeigte zuerst River Bank (das Ziel), dann Sprung nach Osten und Flug zurück.
Jetzt: go() sperrt die Verfolgung für die Dauer des Schwenks; der Start-Flug beginnt mit der Kamera dort, wo das Flugzeug hereinkommt."""
import sys
src, dst = sys.argv[1], sys.argv[2]
s = open(src, encoding='utf-8').read()
def rep(a, b, cnt=1):
    global s
    n = s.count(a); assert n == cnt, (n, a[:70]); s = s.replace(a, b)
rep('const GAME_VER = "V369";', 'const GAME_VER = "V370";')
rep('function go(c, ms) { cam = c; apply(ms); }',
    'function go(c, ms) { cam = c; window.__camHold = ms ? performance.now() + ms : 0; apply(ms); }   /* V370: Verfolgung pausiert, solange der Schwenk läuft */')
rep('const RB = MAP_PTS[0][0], W0 = { ...worldCam(), x: RB[0], y: RB[1] }; go(W0, 0);',
    'const RB = MAP_PTS[0][0], W0 = { ...worldCam(), x: RB[0], y: RB[1] }; go({ ...W0, x: .86, y: .3 }, 0);   /* V370: Start dort, wo das Flugzeug hereinkommt, nicht am Ziel */')
open(dst, 'w', encoding='utf-8').write(s)
print("ok")
