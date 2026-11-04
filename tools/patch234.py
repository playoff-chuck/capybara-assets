"""V234: Spiel direkt von der Karte starten. Karte vom Startbildschirm geöffnet → großer Knopf «PLAY ▶» (bzw.
«CONTINUE ▶» mit Spielstand) und Antippen der rosa Stecknadel des aktuellen Ortes startet sofort das Spiel
(Spielstand fortsetzen oder neue Welttour mit Flug-Intro) – kein Umweg übers Menü."""
import sys
src, dst = sys.argv[1], sys.argv[2]
s = open(src, encoding='utf-8').read()
def rep(a, b, cnt=1):
    global s
    n = s.count(a); assert n == cnt, (n, a[:70]); s = s.replace(a, b)
rep('const GAME_VER = "V233";', 'const GAME_VER = "V234";')
rep('<div class="mapBar"><button type="button" class="mapWorldBtn">WORLD</button><button type="button" class="mapClose">CLOSE</button></div>',
    '<div class="mapBar"><button type="button" class="mapWorldBtn">WORLD</button><button type="button" class="mapPlay">PLAY ▶</button><button type="button" class="mapClose">CLOSE</button></div>')
rep('function openMap(w, why) { clearSeq(); w = w || curWave(); const P = posOf(w); show("browse");',
    '''function openMap(w, why) { clearSeq(); w = w || curWave(); const P = posOf(w); show("browse");
      { const st = document.getElementById("ovStart"), fs = !!(st && !st.hidden && !why); ov.classList.toggle("fromStart", fs);
        const rs = document.getElementById("btnResume"), hasSave = !!(rs && rs.getClientRects().length); ov.querySelector(".mapPlay").textContent = hasSave ? "CONTINUE ▶" : "PLAY ▶"; }''')
js = r'''
  /* V234: Spiel direkt von der Karte starten */
  try { const ov = document.getElementById("ovMap");
    const playFromMap = () => { const rs = document.getElementById("btnResume"), pb = document.querySelector("#ovStart .playBtn");
      const go = rs && rs.getClientRects().length ? rs : pb; ov.querySelector(".mapClose").click(); if (go) setTimeout(() => go.click(), 60); };
    ov.querySelector(".mapPlay").addEventListener("click", e => { e.stopPropagation(); try { snd("start"); } catch (er) {} playFromMap(); });
    ov.querySelector(".mapVp").addEventListener("click", e => { if (!ov.classList.contains("fromStart") || !ov.classList.contains("browse")) return;
      const cur = ov.querySelector(".mPin.cur i"); if (!cur) return; const r = cur.getBoundingClientRect(), cx = r.left + r.width / 2, cy = r.top + r.height / 2;
      if (Math.hypot(e.clientX - cx, e.clientY - cy) < 34) { e.stopImmediatePropagation(); try { snd("start"); } catch (er) {} playFromMap(); } }, true);
  } catch (e) {}
'''
i = s.rfind('})();\n</script>'); s = s[:i] + js + s[i:]
css = '''<style id="v234">
#ovMap .mapPlay{display:none}
#ovMap.browse.fromStart .mapPlay{display:block;min-width:150px!important;background:linear-gradient(180deg,#ffb347,#ff8a1f)!important;color:#fff!important;-webkit-text-stroke:1.5px #3a2414;paint-order:stroke fill;font-size:21px!important;white-space:nowrap;padding:0 14px!important}
#ovMap.browse.fromStart .mapBar .mapClose,#ovMap.browse.fromStart .mapBar .mapWorldBtn{min-width:0!important;padding:0 14px!important;font-size:17px!important}
#ovMap.browse.fromStart .mPin.cur i{cursor:pointer}
#ovMap.browse.fromStart .mPin.cur em::after{content:" ▶";color:#ff8a1f}
</style>
'''
i = s.rfind('</body>'); s = s[:i] + css + s[i:]
open(dst, 'w', encoding='utf-8').write(s); print('ok')
