"""V273 (Martin 05.11. 15:45): Fenster (Anzeige, Neuheit, Lucky Supply, Rufzeichen) lassen sich erst nach 3 s wegtippen –
Knöpfe sind solange gedimmt, Tipps werden ignoriert. Das Spiel steht wie bisher, die Musik läuft weiter."""
import sys
src, dst = sys.argv[1], sys.argv[2]
s = open(src, encoding='utf-8').read()
def rep(a, b, cnt=1):
    global s
    n = s.count(a); assert n == cnt, (n, a[:70]); s = s.replace(a, b)
rep('const GAME_VER = "V272";', 'const GAME_VER = "V273";')
css = r'''
<style id="v273lock">
.lock3 button,.lock3 .btn-accent{pointer-events:none!important;opacity:.5;filter:grayscale(.3);transition:opacity .3s}
</style>
'''
js = r'''
  /* V273: 3 s Sperre gegen versehentliches Wegtippen */
  try { (() => { const IDS = ["ovAd", "ovIntro", "ovBandit", "ovJoin"], was = {}, until = {};
    const vis = el => el && !el.hidden && getComputedStyle(el).display !== "none";
    setInterval(() => { const now = performance.now(); for (const id of IDS) { const el = document.getElementById(id); const v = vis(el) || (id === "ovIntro" && document.body.classList.contains("introWin"));
        if (v && !was[id]) { until[id] = now + 3000; el && el.classList.add("lock3"); }
        if (el && until[id] && now >= until[id]) { el.classList.remove("lock3"); until[id] = 0; }
        was[id] = v; } }, 100);
    document.addEventListener("click", e => { for (const id of IDS) { const el = document.getElementById(id); if (el && el.classList.contains("lock3") && el.contains(e.target)) { e.stopImmediatePropagation(); e.preventDefault(); return; } } }, true);
  })(); } catch (e) { console.error("lock3", e); }
'''
i = s.rfind('</body>'); s = s[:i] + css + s[i:]
i = s.rfind('})();\n</script>'); s = s[:i] + js + s[i:]
open(dst, 'w', encoding='utf-8').write(s); print('ok')
