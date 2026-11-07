"""V383 (Martin 07.11. 14:33): Beim Dieb sieht man das Sniper-Fadenkreuz nicht (es lag nur im Spielfeld).
Jetzt hängt ein Fadenkreuz am Finger/Cursor, über allem, auch über dem Dieb. Sobald Sniper oder Tesla scharf ist, springt es zuerst auf den Dieb
und folgt dann dem Finger."""
import sys
src, dst = sys.argv[1], sys.argv[2]
s = open(src, encoding='utf-8').read()
def rep(a, b, cnt=1):
    global s
    n = s.count(a); assert n == cnt, (n, a[:70]); s = s.replace(a, b)
rep('const GAME_VER = "V382";', 'const GAME_VER = "V383";')
rep('  document.body.appendChild(el); const g = el.getContext("2d");',
    '''  document.body.appendChild(el); const g = el.getContext("2d");
  /* V383: Fadenkreuz am Finger, über dem Dieb */
  const scope = document.createElement("div"); scope.id = "thiefScope"; scope.setAttribute("aria-hidden", "true");
  scope.innerHTML = '<svg viewBox="0 0 84 84" width="84" height="84"><g fill="none" stroke="currentColor" stroke-linecap="round"><circle cx="42" cy="42" r="26" stroke-width="3.5"/><circle cx="42" cy="42" r="10" stroke-width="2.5"/><path d="M42 4v18M42 62v18M4 42h18M62 42h18" stroke-width="3.5"/></g><circle cx="42" cy="42" r="2.6" fill="currentColor"/><g fill="none" stroke="#fff" stroke-opacity=".75" stroke-linecap="round"><circle cx="42" cy="42" r="28.5" stroke-width="1.2"/></g></svg>';
  scope.style.cssText = "position:fixed;left:-42px;top:-42px;width:84px;height:84px;z-index:2147483001;pointer-events:none;display:none;filter:drop-shadow(0 0 3px rgba(0,0,0,.6));will-change:transform";
  document.body.appendChild(scope);
  let scopeP = null, scopeM = null;
  const scopeSet = e => { scopeP = [e.clientX, e.clientY]; }; document.addEventListener("pointermove", scopeSet, true); document.addEventListener("pointerdown", scopeSet, true);
  const scopeTick = (tx, ty) => { const m = typeof S !== "undefined" && S && (S.mode === "snipe" || S.mode === "tesla") ? S.mode : null, on = !!m && el.style.display === "block";
    if (m !== scopeM) { scopeP = null; scopeM = m; }   /* gerade scharf gemacht: zuerst auf den Dieb */
    if (!on) { if (scope.style.display !== "none") scope.style.display = "none"; return; }
    const p = scopeP || [tx, ty], pulse = 1 + 0.06 * Math.sin(performance.now() / 140); scope.style.display = "block"; scope.style.color = m === "tesla" ? "#c58bff" : "#e04a2e";
    scope.style.transform = `translate(${p[0].toFixed(1)}px,${p[1].toFixed(1)}px) scale(${pulse.toFixed(3)})`; };
  let scopeT = [0, 0]; const scopeLoop = () => { try { scopeTick(scopeT[0], scopeT[1]); } catch (e) {} requestAnimationFrame(scopeLoop); }; requestAnimationFrame(scopeLoop);   /* läuft auch, wenn das Spiel beim Zielen steht */''')
rep('  window.__thiefPos = T => { if (!T) { el.style.display = "none"; return; }',
    '  window.__thiefPos = T => { if (!T) { el.style.display = "none"; return; }')
rep('scale(${sc.toFixed(3)})`; sprite(T); };',
    'scale(${sc.toFixed(3)})`; sprite(T); scopeT = [x, feet - SZ * sc * 0.5 + 5]; };')
open(dst, 'w', encoding='utf-8').write(s)
print("ok")
