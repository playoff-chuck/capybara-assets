#!/usr/bin/env python3
"""V516: HQ-Reparatur-Spielstand: Beim Start fragt das Spiel einmal pro Sitzung /api/pin?code=<Cloud-Code>.
Liegt dort ein von HQ hinterlegter Stand (z. B. wiederhergestellter Nuts-Abstecher), wird er übernommen und neu geladen.
Aufruf: python3 tools/patch516.py site/index.html"""
import sys
p = sys.argv[1]; s = open(p, encoding="utf-8").read()
def rep(a, b, n=1):
    global s
    c = s.count(a); assert c == n, (c, a[:80]); s = s.replace(a, b)
rep('const GAME_VER = "V515";', 'const GAME_VER = "V516";')
rep('''    ov.addEventListener("click", e => { e.stopPropagation(); const b = e.target.closest("button"); if (!b) { if (e.target === ov) close(); return; }''',
    '''    (async () => { try { const c = code(false); if (!c || sessionStorage.getItem("capy-pinchk")) return; sessionStorage.setItem("capy-pinchk", "1");   /* V516 */
        const r = await fetch(API_BASE + "/pin?code=" + c, { cache: "no-store" }); if (!r.ok) return; const d = await r.json(); if (!d || !d.data) return;
        const keep = new Set(["tarnturm-dev"]); const rm = []; for (let i = 0; i < localStorage.length; i++) { const k = localStorage.key(i); if (k && /^(tarnturm|capy)-/.test(k) && !keep.has(k)) rm.push(k); }
        rm.forEach(k => localStorage.removeItem(k)); Object.entries(d.data).forEach(([k, v]) => { if (/^(tarnturm|capy)-/.test(k) && typeof v === "string") localStorage.setItem(k, v); });
        localStorage.setItem("capy-cloud", c); localStorage.setItem("capy-reset", "276"); localStorage.setItem("capy-pinmsg", "1"); location.reload(); } catch (e) {} })();
    setTimeout(() => { try { if (localStorage.getItem("capy-pinmsg")) { localStorage.removeItem("capy-pinmsg"); toast("SAVE RESTORED BY HQ · your progress is back", "HQ", 3500); } } catch (e) {} }, 2500);
    ov.addEventListener("click", e => { e.stopPropagation(); const b = e.target.closest("button"); if (!b) { if (e.target === ov) close(); return; }''')
open(p, "w", encoding="utf-8").write(s); print("ok V516")
