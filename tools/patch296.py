"""V296 (Martin 18:24): Kartenszenen (Ortswechsel, Kontinentflug, Welttour-Start) lassen sich erst nach 3 s wegtippen;
«tap to skip» erscheint erst dann. Schützt vor versehentlichem Wegdrücken."""
import sys
src, dst = sys.argv[1], sys.argv[2]
s = open(src, encoding='utf-8').read()
def rep(a, b, cnt=1):
    global s
    n = s.count(a); assert n == cnt, (n, a[:70]); s = s.replace(a, b)
rep('const GAME_VER = "V295";', 'const GAME_VER = "V296";')
rep('function show(m) { mode = m; layout();', 'function show(m) { mode = m; mapShownAt = performance.now(); ov.classList.remove("skipOk"); clearTimeout(skipT); skipT = setTimeout(() => ov.classList.add("skipOk"), 3000); layout();')
rep('ov.addEventListener("click", () => { if (mode === "auto") hide(); });', 'let mapShownAt = 0, skipT = null;\n    ov.addEventListener("click", () => { if (mode === "auto" && performance.now() - mapShownAt >= 3000) hide(); });')
css = r'''
<style id="v296skip">
#ovMap.auto:not(.skipOk) .mapSkip{visibility:hidden}
</style>
'''
i = s.rindex('</body>'); s = s[:i] + css + s[i:]
open(dst, 'w', encoding='utf-8').write(s)
