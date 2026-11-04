"""V211: Dev-Werkzeuge wieder per 7× Tippen aufs Logo (ganzes Logo oben links, auch das Bild-Logo);
«New world tour» zeigt wieder die Startauswahl (PLAY / Checkpoints wie «ab Welle 20») statt sofort zu starten."""
import sys
src, dst = sys.argv[1], sys.argv[2]
s = open(src, encoding='utf-8').read()
def rep(a, b, cnt=1):
    global s
    n = s.count(a); assert n == cnt, (n, a[:70]); s = s.replace(a, b)
rep('const GAME_VER = "V210";', 'const GAME_VER = "V211";')
rep('''        arm = 0; nb.textContent = "New world tour"; nb.classList.remove("armed"); try { LS.del("tarnturm-save"); } catch (er) {}
        const p = document.querySelector("#modeList button"); if (p) p.click(); }); }''',
    '''        arm = 0; nb.textContent = "New world tour"; nb.classList.remove("armed"); try { LS.del("tarnturm-save"); } catch (er) {}
        res.hidden = true; document.body.classList.remove("hasSave"); nb.hidden = true; try { renderModes(); } catch (er) {} }); }''')
js = '''
  /* V211: 7× aufs Logo (auch Bild-Logo / Schriftzug) → Dev-Werkzeuge */
  try { document.addEventListener("pointerdown", e => { const t = e.target; if (!t || !t.closest) return; const b = t.closest(".brand, .logoFull, #brandLogo"); if (!b || t.closest(".logo")) return;
      const lg = document.querySelector(".logo"); if (lg) lg.dispatchEvent(new PointerEvent("pointerdown", { bubbles: false })); }, true); } catch (e) {}
'''
i = s.rfind('})();\n</script>'); s = s[:i] + js + s[i:]
open(dst, 'w', encoding='utf-8').write(s); print('ok')
