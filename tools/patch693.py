# V693 (Martin 12.11. 22:52): Spielstärke des Bosses nur noch als kleiner Buchstabe oben rechts in der Ergebniskarte (nur Dev-Modus).
import sys
src, dst = sys.argv[1], sys.argv[2]
s = open(src, encoding="utf8").read()
def rep(a, b, n=1):
    global s; c = s.count(a); assert c == n, (a[:70], c); s = s.replace(a, b)
rep('$("hkDevT").textContent = `dev: BOSS ${HK.type} (${(BOSS_T[HK.type] || {}).txt})`;', '$("hkDevT").textContent = HK.type || ""; $("hkDevT").title = `BOSS ${HK.type} (${(BOSS_T[HK.type] || {}).txt})`;   /* V693: nur der Buchstabe */')
rep('#ovHack #hackRes.hkNew .hkDevT{color:rgba(255,236,210,.55)!important}', '#ovHack #hackRes.hkNew .hkDevT{position:absolute;top:7px;right:10px;z-index:8;margin:0!important;font:700 11px/1 var(--f-ui,"Baloo 2",sans-serif)!important;color:rgba(255,255,255,.7)!important;text-shadow:0 1px 2px rgba(0,0,0,.8);pointer-events:none}')
rep('const GAME_VER = "V692"', 'const GAME_VER = "V693"')
open(dst, "w", encoding="utf8").write(s); print("ok", len(s))
