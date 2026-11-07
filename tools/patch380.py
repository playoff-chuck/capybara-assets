"""V380 (Martin 07.11. 13:37): Weltkarte im Kreis scrollen. Beim freien Ansehen (browse) läuft die Karte links und rechts endlos weiter:
zwei Kopien des Kartenbildes daneben, an den Nähten 5 % weich überblendet. Die Kamera springt unsichtbar zurück, sobald sie über eine Naht geht.
Senkrecht bleibt die Karte begrenzt. Antippen eines Kontinents klappt auch auf den Kopien."""
import sys
src, dst = sys.argv[1], sys.argv[2]
s = open(src, encoding='utf-8').read()
def rep(a, b, cnt=1):
    global s
    n = s.count(a); assert n == cnt, (n, a[:70]); s = s.replace(a, b)
rep('const GAME_VER = "V379";', 'const GAME_VER = "V380";')
rep('<img class="mapImg" src="img/worldmap.webp" alt="World map" draggable="false">',
    '<img class="mapImg" src="img/worldmap.webp" alt="World map" draggable="false"><img class="mapImg mapWrap wL" src="img/worldmap.webp" alt="" draggable="false"><img class="mapImg mapWrap wR" src="img/worldmap.webp" alt="" draggable="false">')
rep('      if (mw >= W) tx = Math.min(0, Math.max(W - mw, tx)); else tx = (W - mw) / 2;',
    '      if (mode === "browse" && !cam.free) { const P = WRAP_P; cam.x = ((cam.x % P) + P) % P; tx = W / 2 - cam.x * mw; }   /* V380: im Kreis */\n'
    '      else if (mw >= W) tx = Math.min(0, Math.max(W - mw, tx)); else tx = (W - mw) / 2;')
rep('    let cam = { x: .5, y: .5, k: 1 }, BW = 400, mode = null, seqT = [], seqDone = null;',
    '    let cam = { x: .5, y: .5, k: 1 }, BW = 400, mode = null, seqT = [], seqDone = null; const WRAP_P = 0.95;')
rep('cam.x = Math.max(0, Math.min(1, cam.x)); cam.y = Math.max(0, Math.min(1, cam.y)); window.__camHold = 0; apply(0); });',
    'cam.y = Math.max(0, Math.min(1, cam.y)); window.__camHold = 0; apply(0); });')
rep('const r = world.getBoundingClientRect(), nx = (e.clientX - r.left) / r.width, ny = (e.clientY - r.top) / r.height;',
    'const r = world.getBoundingClientRect(), ny = (e.clientY - r.top) / r.height; let nx = (e.clientX - r.left) / r.width; nx = ((nx % WRAP_P) + WRAP_P) % WRAP_P;')
rep('#ovMap .mapImg{position:absolute;inset:0;width:100%;height:100%;max-width:none!important;display:block;pointer-events:none}',
    '#ovMap .mapImg{position:absolute;inset:0;width:100%;height:100%;max-width:none!important;display:block;pointer-events:none}\n'
    '#ovMap .mapWrap{display:none}\n'
    '#ovMap.browse .mapWrap{display:block}\n'
    '#ovMap .mapWrap.wR{left:95%;right:auto;-webkit-mask-image:linear-gradient(to right,transparent 0,#000 5%);mask-image:linear-gradient(to right,transparent 0,#000 5%)}\n'
    '#ovMap .mapWrap.wL{left:-95%;right:auto;-webkit-mask-image:linear-gradient(to right,#000 95%,transparent 100%);mask-image:linear-gradient(to right,#000 95%,transparent 100%)}')
open(dst, 'w', encoding='utf-8').write(s)
print("ok")
