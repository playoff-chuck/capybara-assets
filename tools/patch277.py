"""V277 (Martin 16:11): Ankunftsbild (Capybaras auf dem Kontinent) baut sich aus dem Landepunkt heraus auf –
wachsender Kreis (clip-path) mit Ursprung am rosa Punkt, Bild zoomt vom selben Punkt aus. Gilt für Welttour-Start und Kontinentflüge."""
import sys
src, dst = sys.argv[1], sys.argv[2]
s = open(src, encoding='utf-8').read()
def rep(a, b, cnt=1):
    global s
    n = s.count(a); assert n == cnt, (n, a[:70]); s = s.replace(a, b)
rep('const GAME_VER = "V276";', 'const GAME_VER = "V277";')
rep('    function setMe(pt, on) {',
    '    function arrOrigin(el) { try { const o = ov.getBoundingClientRect(), r = me.getBoundingClientRect(); let x = r.left + r.width / 2 - o.left, y = r.top + r.height / 2 - o.top;\n'
    '        if (x < 0 || y < 0 || x > o.width || y > o.height) { x = o.width / 2; y = o.height / 2; }\n'
    '        el.style.setProperty("--ox", x + "px"); el.style.setProperty("--oy", y + "px"); el.classList.add("fromPt"); } catch (e) {} }\n'
    '    function setMe(pt, on) {')
rep('ov.appendChild(arrC); requestAnimationFrame(() => arrC.classList.add("on"));',
    'arrOrigin(arrC); ov.appendChild(arrC); requestAnimationFrame(() => requestAnimationFrame(() => arrC.classList.add("on")));')
rep('        ov.appendChild(arr); requestAnimationFrame(() => arr.classList.add("on"));',
    '        arrOrigin(arr); ov.appendChild(arr); requestAnimationFrame(() => requestAnimationFrame(() => arr.classList.add("on")));')
css = r'''
<style id="v277arr">
#ovMap .mapArrive.fromPt{opacity:1;clip-path:circle(0px at var(--ox,50%) var(--oy,50%));transition:clip-path 1.4s cubic-bezier(.55,0,.3,1)}
#ovMap .mapArrive.fromPt.on{clip-path:circle(150vmax at var(--ox,50%) var(--oy,50%))}
#ovMap .mapArrive.fromPt img{transform-origin:var(--ox,50%) var(--oy,50%);transform:scale(1.35);transition:transform 4.5s cubic-bezier(.2,.7,.3,1)}
#ovMap .mapArrive.fromPt.on img{transform:scale(1)}
</style>
'''
i = s.rindex('</body>'); s = s[:i] + css + s[i:]
open(dst, 'w', encoding='utf-8').write(s)
