"""V355 (To-do 89, Martin «1a»): neuer Kontinent = Spielfeld ganz leer (keine Start-Steine, keine Türme),
alle Türme samt Waffen und Upgrades zum vollen Preis zurück als Gold. Auch ohne Türme eine kurze Meldung."""
import sys
src, dst = sys.argv[1], sys.argv[2]
s = open(src, encoding='utf-8').read()
def rep(a, b, cnt=1):
    global s
    n = s.count(a); assert n == cnt, (n, a[:70]); s = s.replace(a, b)
rep('const GAME_VER = "V354";', 'const GAME_VER = "V355";')
rep('S.grid = new Uint8Array(NN); S.towers = new Map(); seedGarbage(); try { if (S.sel) closeSheet(); } catch (e) {}',
    'S.grid = new Uint8Array(NN); S.towers = new Map(); try { if (S.sel) closeSheet(); } catch (e) {}   /* V355: ganz leer, keine Start-Steine */')
rep('if (n) { S.gold += sum; announce(`TOWERS SOLD · +${sum} GOLD`, `New continent, fresh start: ${n} tower${n > 1 ? "s" : ""} sold at full price. The gold is in your account.`, "GOLD", 6500); } };',
    'if (n) { S.gold += sum; announce(`TOWERS SOLD · +${sum} GOLD`, `New continent, empty field: ${n} tower${n > 1 ? "s" : ""} and all weapons sold at full price. The gold is in your account.`, "GOLD", 6500); } else toast("NEW CONTINENT · EMPTY FIELD", "HQ", 1800); };')
open(dst, 'w', encoding='utf-8').write(s)
print("ok")
