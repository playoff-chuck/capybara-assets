import sys, os, subprocess
# V723 (Martin 15.11.2026 20:28): Beim Tod groß und klar: wie weit man gekommen ist und ab welcher Welle man weiterspielt.
#  Neuer Block #overWhere unter dem Titel: «DU HAST ERREICHT · WELLE 92» | «WEITER AB · WELLE 97 · CANYON» (bzw. «NEUSTART AB · WELLE 1»).
#  Weiter-Knopf: «▶ WEITER AB WELLE 97».
src, dst = sys.argv[1], sys.argv[2]
s = open(src, encoding="utf-8").read()
def rep(a, b, n=1):
    global s
    c = s.count(a); assert c == n, (a[:60], c); s = s.replace(a, b)
rep('const GAME_VER = "V722";', 'const GAME_VER = "V723";')
rep('<h2 id="overTitle">FALLEN</h2>', '<h2 id="overTitle">FALLEN</h2><div id="overWhere" hidden><div class="owBox owGot"><small>YOU REACHED WAVE</small><b id="owGot">1</b><em id="owGotP"></em></div><div class="owArrow">➜</div><div class="owBox owNext"><small id="owNextL">YOU CONTINUE FROM WAVE</small><b id="owNext">1</b><em id="owNextP"></em></div></div>')
rep('bc.innerHTML = `CONTINUE · WAVE ${cp + 1} · ${String(wherePos(cp + 1).place || "")}`;',
    'bc.innerHTML = `▶ CONTINUE FROM WAVE ${cp + 1}`;')
rep('const _go = gameOver; gameOver = function () { try { if (S && !S.nuts && !S.testRun) bump(S.wave); } catch (e) {} const r = _go.apply(this, arguments);',
    '''const _go = gameOver; gameOver = function () { try { if (S && !S.nuts && !S.testRun) bump(S.wave); } catch (e) {} const r = _go.apply(this, arguments);
    try { const ow = $("overWhere"); if (ow) { const dead = S && !S.won && !S.nuts && !S.replay; ow.hidden = !dead; if (dead) { const cp = window.__cpGet(), nx = cp >= 5 ? cp + 1 : 1, w = Math.max(1, S.wave | 0);   /* V723 */
        $("owGot").textContent = String(w); $("owGotP").textContent = String(wherePos(w).place || ""); $("owNextL").textContent = cp >= 5 ? "YOU CONTINUE FROM WAVE" : "YOU START AGAIN FROM WAVE"; $("owNext").textContent = String(nx); $("owNextP").textContent = String(wherePos(nx).place || ""); } } } catch (e) {}''')
rep('<style id="v720css">', '''<style id="v723css">
#overWhere{display:grid;grid-template-columns:1fr auto 1fr;align-items:stretch;gap:6px;margin:6px 0 4px}
#overWhere[hidden]{display:none}
#overWhere .owBox{display:flex;flex-direction:column;align-items:center;justify-content:center;border-radius:14px;padding:7px 6px 6px;border:2.5px solid #3a2414;box-shadow:0 3px 0 #3a2414;min-width:0}
#overWhere .owGot{background:#ffe1dc}#overWhere .owNext{background:#d9f5c9}
#overWhere small{font:800 11px/1.1 var(--f-ui,system-ui);letter-spacing:.06em;color:#6b4a35;text-transform:uppercase;text-align:center}
#overWhere b{font:400 44px/1 var(--f-display,"Bangers",sans-serif);letter-spacing:.02em;color:#3a2414;margin-top:3px;white-space:nowrap}
#overWhere .owGot b{color:#c62d24}#overWhere .owNext b{color:#2f7d1e}
#overWhere em{font:700 11.5px/1.1 var(--f-ui,system-ui);font-style:normal;color:#6b4a35;margin-top:2px;text-align:center;overflow:hidden;text-overflow:ellipsis;white-space:nowrap;max-width:100%}
#overWhere .owArrow{align-self:center;font:700 22px/1 system-ui;color:#3a2414}
@media (max-height:700px){#overWhere b{font-size:34px}#overWhere small,#overWhere em{font-size:10px}}
</style>
<style id="v720css">''')
open(dst, "w", encoding="utf-8").write(s)
subprocess.run([sys.executable, os.path.join(os.path.dirname(os.path.abspath(__file__)), "lang723.py"), os.path.join(os.path.dirname(os.path.abspath(dst)), "lang")], check=True)
