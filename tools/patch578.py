#!/usr/bin/env python3
# V578 (Martin 11.11. 00:45):
# - «✕ CANCEL» oben im Feld jetzt auch beim Zielen mit Sniper, Mixer (Beton) und Tesla, nicht nur beim Turm
# - CANCEL bringt zurück in das Menü, aus dem die Waffe kam (Shop bzw. Spezial-Tasche); ohne Menü → Shop
import sys
src, dst = sys.argv[1], sys.argv[2]
s = open(src, encoding="utf-8").read()
def rep(a, b, n=1):
    global s
    c = s.count(a); assert c == n, (c, a[:90]); s = s.replace(a, b)
rep('const GAME_VER = "V577";', 'const GAME_VER = "V578";')

rep('''  b.addEventListener("click", e => { e.stopPropagation(); try { if (S && S.mode === "build") { S.mode = null; S.aim = null; snd("uiTap"); } } catch (er) {} b.hidden = true; });
  setInterval(() => { const on = !!(S && S.started && !S.over && S.mode === "build" && !S.paused);''',
'''  const AIM = { build: 1, snipe: 1, mix: 1, tesla: 1 };   /* V578: alle Ziel-Modi */
  const from = () => { try { const sh = document.getElementById("sheet"), si = document.getElementById("sheetIn"); return sh && !sh.hidden ? (si && si.classList.contains("pk") ? "pk" : "shop") : null; } catch (e) { return null; } };
  const _arm = armSpecial; armSpecial = function (k) { const o = from(); const r = _arm.apply(this, arguments); try { if (S && S.mode === k) S.armFrom = o || "shop"; } catch (e) {} return r; };
  const _tb = toggleBuild; toggleBuild = function () { const o = from(); const r = _tb.apply(this, arguments); try { if (S && S.mode === "build") S.armFrom = o || "shop"; } catch (e) {} return r; };
  b.addEventListener("click", e => { e.stopPropagation(); try { if (S && AIM[S.mode]) { const o = S.armFrom || "shop"; S.mode = null; S.aim = null; S.armFrom = null; snd("uiTap"); if (!S.over && !(typeof TUT !== "undefined" && TUT.on)) { if (o === "pk") openPocket(); else { $("sheetIn").classList.remove("pk"); openShop(); } } } } catch (er) {} b.hidden = true; });   /* V578: zurück ins Menü */
  setInterval(() => { const on = !!(S && S.started && !S.over && AIM[S.mode] && !S.paused);''')

open(dst, "w", encoding="utf-8").write(s)
print("ok V578")
