"""V239: Dev-Leiste oben rechts im Startbildschirm (nur Dev-Modus, 7× Logo): Welle wählen + GO, Schnellwahl
5/15/31/61/91/121, Specials, Test from 0. Die alten Dev-Knöpfe unten (von Karten-/Flugzeug-Knopf verdeckt) sind ausgeblendet."""
import sys
src, dst = sys.argv[1], sys.argv[2]
s = open(src, encoding='utf-8').read()
def rep(a, b, cnt=1):
    global s
    n = s.count(a); assert n == cnt, (n, a[:70]); s = s.replace(a, b)
rep('const GAME_VER = "V238";', 'const GAME_VER = "V239";')
css = '''
<style id="v239dev">
#devBar{position:fixed;z-index:60;top:calc(env(safe-area-inset-top,0px) + 8px);right:calc(max(12px,env(safe-area-inset-right,0px)) + 50px);width:min(196px,calc(100vw - 196px));box-sizing:border-box;padding:6px;background:#fff6e6;border:2.5px solid #3a2a1a;border-radius:12px;box-shadow:0 4px 0 rgba(58,42,26,.35);display:grid;grid-template-columns:auto 1fr auto;gap:5px;align-items:center;font:900 11px/1 system-ui;color:#3a2a1a}
#devBar[hidden]{display:none}
#devBar .dTag{background:#e84f5c;color:#fff;border-radius:6px;padding:4px 5px 3px;letter-spacing:.5px}
#devBar input{width:100%;min-width:0;box-sizing:border-box;height:30px;border:2px solid #3a2a1a;border-radius:8px;font:900 15px/1 system-ui;text-align:center;padding:0;background:#fff;color:#3a2a1a}
#devBar button{height:30px!important;min-height:30px!important;margin:0!important;padding:0 8px!important;border-radius:8px!important;font:900 12px/1 system-ui!important;white-space:nowrap}
#devBar .dRow{grid-column:1/-1;display:grid;gap:4px}
#devBar .dQ{grid-template-columns:repeat(6,1fr)}
#devBar .dQ button{padding:0!important;font-size:11px!important;background:#fff!important;color:#3a2a1a!important;border:2px solid #3a2a1a!important}
#devBar .dT{grid-template-columns:1fr 1fr}
#devBar .dT button{background:#3a2a1a!important;color:#fff6e6!important;border:0!important;font-size:11px!important}
#startMain .startFoot .devOnly{display:none!important}
</style>
'''
js = '''
  /* V239: Dev-Leiste oben rechts */
  try { const sm = document.getElementById("startMain"); if (sm) { const d = document.createElement("div"); d.id = "devBar"; d.className = "devOnly"; d.hidden = LS.get("tarnturm-dev") !== "1";
      d.innerHTML = '<span class="dTag">DEV</span><input id="devWave" type="number" min="1" max="150" value="31" inputmode="numeric" aria-label="Start wave"><button class="btn-accent" id="devGo">GO ▶</button>'
        + '<div class="dRow dQ">' + [5, 15, 31, 61, 91, 121].map(w => '<button data-w="' + w + '">' + w + '</button>').join("") + '</div>'
        + '<div class="dRow dT"><button id="devSpec">Specials</button><button id="devZero">Test from 0</button></div>';
      sm.appendChild(d);
      const go = w => { w = Math.max(1, Math.min(150, w | 0 || 1)); try { SFX.init(); snd("confirm"); } catch (e) {} devJump(w); };
      d.addEventListener("click", e => { const b = e.target.closest("button"); if (!b) return; e.stopPropagation();
        if (b.dataset.w) { document.getElementById("devWave").value = b.dataset.w; go(+b.dataset.w); }
        else if (b.id === "devGo") go(+document.getElementById("devWave").value);
        else if (b.id === "devSpec") { const x = document.getElementById("btnSpecials"); if (x) x.click(); }
        else if (b.id === "devZero") { const x = document.getElementById("btn711Test"); if (x) x.click(); } });
      document.getElementById("devWave").addEventListener("keydown", e => { e.stopPropagation(); if (e.key === "Enter") go(+e.target.value); }); } } catch (e) { console.error("devBar", e); }
'''
i = s.rfind('</body>'); s = s[:i] + css + s[i:]
i = s.rfind('})();\n</script>'); s = s[:i] + js + s[i:]
open(dst, 'w', encoding='utf-8').write(s); print('ok')
