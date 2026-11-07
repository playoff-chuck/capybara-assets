#!/usr/bin/env python3
# V422 (Martin 07.11. 23:16): Gratis-Waffen per Air Drop um ein Drittel seltener –
# Ten-ton-Geschenke nur noch W8 und W22 (vorher 8/14/22); Lucky Supply (Gratis-Special) alle 9–13 Wellen statt 7–10 (ab W60: 7–9 statt 5–7);
# Rettungs-Lucky frühestens 12 Wellen nach dem letzten statt 8.
import sys
src, dst = sys.argv[1], sys.argv[2]
s = open(src, encoding="utf-8").read()
def rep(a, b, n=1):
    global s
    assert s.count(a) == n, (s.count(a), a[:80])
    s = s.replace(a, b)
rep('const GAME_VER = "V421";', 'const GAME_VER = "V422";')
rep("const tg = [8, 14, 22].includes(S.wave)", "const tg = [8, 22].includes(S.wave)")
rep('for (const k of ["kan", "frost", "mix", "snipe", "ton", "chomp", "tesla", "lock"]) if (S.adDue[k] && !why(k) && !(k === "ton" && [8, 14, 22].some(',
    'for (const k of ["kan", "frost", "mix", "snipe", "ton", "chomp", "tesla", "lock"]) if (S.adDue[k] && !why(k) && !(k === "ton" && [8, 22].some(')
rep('S.banditNext = (S.wave || 1) + ((S.wave || 1) < 60 ? 7 + Math.floor(Math.random() * 4) : 5 + Math.floor(Math.random() * 3));',
    'S.banditNext = (S.wave || 1) + ((S.wave || 1) < 60 ? 9 + Math.floor(Math.random() * 5) : 7 + Math.floor(Math.random() * 3));   /* V422: ein Drittel seltener */')
rep("if ((S.wave || 0) < (S.rescueW || -99) + 8) return;", "if ((S.wave || 0) < (S.rescueW || -99) + 12) return;   /* V422 */")
open(dst, "w", encoding="utf-8").write(s)
print("ok")
