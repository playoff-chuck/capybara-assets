"""V261 (Martin 05.11. 13:59): Tutorial-Pfeil groß, gelb, Comic-Stil – in jedem Schritt:
DROP-Knopf → SHOP-Knopf → im Shop auf PLACE → auf einen gelandeten Block → im Turm-Menü auf MG → dann auf Done.
Auch die Erstes-Mal-Hinweise nutzen den neuen Pfeil. Pfeil fängt keine Tipps ab (pointer-events:none)."""
import sys
src, dst = sys.argv[1], sys.argv[2]
s = open(src, encoding='utf-8').read()
def rep(a, b, cnt=1):
    global s
    n = s.count(a); assert n == cnt, (n, a[:70]); s = s.replace(a, b)
rep('const GAME_VER = "V260";', 'const GAME_VER = "V261";')
css = r'''
<style id="v261arrow">
#coachArrow{visibility:hidden!important}
#comicArrow{position:fixed;left:0;top:0;width:64px;height:84px;z-index:99990;pointer-events:none;display:none;transform:translate(-50%,0);filter:drop-shadow(0 4px 0 rgba(0,0,0,.35))}
#comicArrow svg{width:100%;height:100%;display:block;animation:caBob .6s ease-in-out infinite alternate}
#comicArrow.up svg{transform:rotate(180deg);animation-name:caBobU}
@keyframes caBob{from{translate:0 -10px}to{translate:0 4px}}
@keyframes caBobU{from{translate:0 10px}to{translate:0 -4px}}
@media (prefers-reduced-motion:reduce){#comicArrow svg{animation:none}}
</style>
'''
js = r'''
  /* V261: großer gelber Comic-Pfeil fürs Tutorial (jeder Schritt) und die Hinweise */
  try { (() => {
    const ca = document.createElement("div"); ca.id = "comicArrow";
    ca.innerHTML = '<svg viewBox="0 0 64 84"><path d="M20 4 Q32 1 44 4 L45 44 L60 44 Q63 46 61 49 L34 81 Q32 83 30 81 L3 49 Q1 46 4 44 L19 44 Z" fill="#ffd23a" stroke="#17150c" stroke-width="4.5" stroke-linejoin="round"/><path d="M25 9 L26 47 L14 49" fill="none" stroke="#fff6b0" stroke-width="4" stroke-linecap="round" stroke-linejoin="round" opacity=".9"/><path d="M40 10 L40 48 L52 49 L33 72" fill="none" stroke="#e0a21a" stroke-width="3" stroke-linecap="round" stroke-linejoin="round" opacity=".7"/></svg>';
    document.body.appendChild(ca);
    const vis = el => { if (!el) return null; const r = el.getBoundingClientRect(); return r.width > 2 && r.height > 2 && r.bottom > 0 && r.top < innerHeight ? r : null; };
    const btnTxt = (re) => [...document.querySelectorAll("#sheet button")].find(b => re.test(b.textContent) && vis(b));
    const sheetUp = () => { const sh = document.getElementById("sheet"); return sh && !sh.hidden && vis(sh) && (S.shop || S.sel); };
    function block() { try { let best = -1; for (let i = 0; i < S.grid.length; i++) { if (!S.grid[i] || S.towers.has(i) || (typeof TNT !== "undefined" && S.grid[i] === TNT)) continue; const x = i % GW, y = (i / GW) | 0; if (best < 0) best = i; else { const by = (best / GW) | 0, bx = best % GW; if (y < by || (y === by && Math.abs(x - 5.5) < Math.abs(bx - 5.5))) best = i; } }
        if (best < 0) return null; const p = cvPt(best % GW + 0.5, ((best / GW) | 0) + 0.5), cs = p.cs || 20; return { left: p.x - cs / 2, right: p.x + cs / 2, top: p.y - cs / 2, bottom: p.y + cs / 2, width: cs, height: cs }; } catch (e) { return null; } }
    function towerR() { try { for (const t of S.towers.values()) if (!t.w.length) { const p = cvPt(t.x + 0.5, t.y + 0.5), cs = p.cs || 20; return { left: p.x - cs / 2, right: p.x + cs / 2, top: p.y - cs / 2, bottom: p.y + cs / 2, width: cs, height: cs }; } } catch (e) {} return null; }
    function target() {
      const c = document.getElementById("coach"); if (!c || c.hidden || document.body.classList.contains("mapUp") || (S && S.paused) || document.hidden) return null;
      if (typeof TUT !== "undefined" && TUT.on) {
        const k = TUT.step;
        if (k === 0) return vis(document.getElementById("bDrop"));
        if (k === 1) { if (sheetUp() && S.shop) { const b = btnTxt(/PLACE/); if (b) return vis(b); } return vis(document.getElementById("bBuild")); }
        if (k === 2) { if (S.mode === "build") return block(); if (sheetUp() && S.shop) { const b = btnTxt(/PLACE/); if (b) return vis(b); } return vis(document.getElementById("bBuild")); }
        if (k === 3) { if (sheetUp() && S.sel) { const armed = S.sel.w && S.sel.w.length; const b = armed ? document.getElementById("sClose") : document.querySelector('#sheet [data-buy="mg"]'); return vis(b); } return towerR(); }
        return null;
      }
      const a = document.getElementById("coachArrow"); if (a && a.style.display === "block") { const r = a.getBoundingClientRect(); return { hint: true, up: a.textContent === "▲", x: r.left + r.width / 2, y: a.textContent === "▲" ? r.top : r.bottom }; }
      return null;
    }
    let last = "";
    function tick() {
      let r = null; try { r = target(); } catch (e) {}
      if (!r) { if (last !== "none") { ca.style.display = "none"; last = "none"; } return; }
      let x, y, up;
      if (r.hint) { x = r.x; up = r.up; y = up ? r.y : r.y - 84; }
      else { x = r.left + r.width / 2; up = r.top < 96; y = up ? r.bottom + 2 : r.top - 86; }
      x = Math.max(34, Math.min(innerWidth - 34, x));
      const key = Math.round(x) + "," + Math.round(y) + up;
      if (key !== last) { ca.style.display = "block"; ca.classList.toggle("up", up); ca.style.left = x + "px"; ca.style.top = y + "px"; last = key; }
    }
    setInterval(tick, 120);
    window.__TT && (window.__TT.comicArrow = tick);
  })(); } catch (e) { console.error("comicArrow", e); }
'''
i = s.rfind('</body>'); s = s[:i] + css + s[i:]
i = s.rfind('})();\n</script>'); s = s[:i] + js + s[i:]
open(dst, 'w', encoding='utf-8').write(s); print('ok')
