"""V317: Weltkarte füllt immer den ganzen Bildschirm – keine Streifen oben/unten (Martin 06.11. 12:48:
«Auf der Weltkarte ist links, unten und oben ein Streifenübergang … Das Bild soll den ganzen Screen erfassen.»).
- apply(): Zoom mindestens so groß, dass die Karte Breite UND Höhe des Bildschirms deckt (vorher wurde sie im Hochformat
  mittig mit Streifen gezeigt). Antarktis-Ansicht (free) unten bündig statt mit Rand.
- Flüge: Kamera folgt dem Flugzeug weich (Flugzeug bleibt immer im Bild, auch wenn die Welt nicht mehr ganz drauf passt);
  Kontinentflug zoomt auf den Abflugort statt auf die Weltmitte; Welttour-Start zeigt Südamerika."""
import sys
src, dst = sys.argv[1], sys.argv[2]
s = open(src, encoding='utf-8').read()
def rep(a, b, cnt=1):
    global s
    n = s.count(a); assert n == cnt, (n, a[:70]); s = s.replace(a, b)

rep('const GAME_VER = "V316";', 'const GAME_VER = "V317";')
rep('''function apply(anim) {
      const W = vp.clientWidth, H = vp.clientHeight, mw = BW * cam.k, mh = BW * MAP_AR * cam.k;''',
    '''function apply(anim) {
      const W = vp.clientWidth, H = vp.clientHeight, kk = Math.max(cam.k, W / BW, H / (BW * MAP_AR)), mw = BW * kk, mh = BW * MAP_AR * kk;   /* V317: Karte deckt immer den ganzen Bildschirm */''')
rep('if (cam.free) ty = H * .80 - mh; else if (mh >= H)', 'if (cam.free) ty = Math.max(H - mh, Math.min(0, H * .80 - mh)); else if (mh >= H)')
rep('world.style.transform = `translate(${tx}px,${ty}px) scale(${cam.k})`; world.style.setProperty("--ik", 1 / cam.k);',
    'world.style.transform = `translate(${tx}px,${ty}px) scale(${kk})`; world.style.setProperty("--ik", 1 / kk);')
# Kamera folgt dem Flugzeug
rep('plane.style.setProperty("--px", (x) * BW + "px"); plane.style.setProperty("--py", (y) * BW * MAP_AR + "px");',
    'plane.style.setProperty("--px", (x) * BW + "px"); plane.style.setProperty("--py", (y) * BW * MAP_AR + "px");\n'
    '        if (x >= 0 && x <= 1 && (performance.now() - (window.__camHold || 0)) > 0) { const f = t < 0.15 ? t / 0.15 * 0.12 : 0.12; cam = { ...cam, x: cam.x + (x - cam.x) * f, y: cam.y + (y - cam.y) * f }; apply(0); }   /* V317: Kamera folgt dem Flugzeug */')
i = s.index('function playCont(w, done) {'); j = s.index('function playIntro(done)', i)
body = s[i:j]
old = 'go(worldCam(), 1300);'
assert body.count(old) == 1, body.count(old)
body = body.replace(old, 'go({ ...worldCam(), x: MAP_PTS[oc][5][0], y: MAP_PTS[oc][5][1] }, 1300);   /* V317: auf den Abflugort */')
s = s[:i] + body + s[j:]
# Welttour-Start: Kamera auf Südamerika (Ankunftsort), nicht auf die Weltmitte (Afrika) – Fund Erststart-Test 06.11.
rep('const W0 = worldCam(), RB = MAP_PTS[0][0]; go(W0, 0);', 'const RB = MAP_PTS[0][0], W0 = { ...worldCam(), x: RB[0], y: RB[1] }; go(W0, 0);   /* V317 */')
open(dst, 'w', encoding='utf-8').write(s)
print("ok")
