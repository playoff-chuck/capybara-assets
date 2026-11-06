"""V325 (Martin 06.11. 21:59: «83 noch immer Spruch mit soldier»): keine «soldier»-Sprüche mehr.
«Soldier wounded!» (Sonderwelle Wounded, z. B. W83) → «Mayday! Mayday!»; alle anderen Clips mit «soldier» werden nicht mehr gespielt
(Good job / Stay frosty / Rise and shine / Eyes up, soldier · «Feel better, soldier!» beim Medkit)."""
import sys
src, dst = sys.argv[1], sys.argv[2]
s = open(src, encoding='utf-8').read()
def rep(a, b, cnt=1):
    global s
    n = s.count(a); assert n == cnt, (n, a[:70]); s = s.replace(a, b)
rep('const GAME_VER = "V324";', 'const GAME_VER = "V325";')
JS = r'''
/* V325: keine «soldier»-Sprüche */
try { (() => { const sy = SFX.say; SFX.say = function (k) { try { const t = String((typeof VOICE_TEXT !== "undefined" && VOICE_TEXT[k]) || k || "");
      if (/soldier/i.test(t)) { if (/wounded/i.test(t)) { const a = [...arguments]; a[0] = "Mayday! Mayday!"; return sy.apply(SFX, a); } return; } } catch (e) {} return sy.apply(SFX, arguments); }; })(); } catch (e) { console.error("v325", e); }
'''
anchor = '})();\n</script>'
p = s.rindex(anchor); s = s[:p] + JS + s[p:]
open(dst, 'w', encoding='utf-8').write(s)
print("ok")
