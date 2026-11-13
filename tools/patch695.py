# V695 (Megatest 13.11., Punkt 5 – von Martin genehmigt): fehlende Übersetzungen RU/ES/PT.
# 1) i18nLookup: Text mit Name UND Zahl («The Jaw leads the pack · splat it for +500 gold») findet jetzt das Muster «@ … +# …».
# 2) Neue Schlüssel stehen in tools/lang695.py (Bug, Vollbild, Grafik MINIMAL, Checkpoint-Teile, BOSS DOWN, −90°-Paket, FROM … WITH LOVE, SALE, Bewertungs-Etiketten).
import sys
src, dst = sys.argv[1], sys.argv[2]
s = open(src, encoding="utf8").read()
def rep(a, b, n=1):
    global s; c = s.count(a); assert c == n, (a[:70], c); s = s.replace(a, b)
rep('GAME_VER = "V694"', 'GAME_VER = "V695"')
rep('''const pat = key.split(nm).join("@"), v = D[pat]; if (v != null) return v.split("@").join(D[nm] != null ? D[nm] : nm); } }''',
'''const pat = key.split(nm).join("@"), v = D[pat]; if (v != null) return v.split("@").join(D[nm] != null ? D[nm] : nm);
    if (nums && !/\\d/.test(nm)) { const v2 = D[pat.replace(I18N_NUM, "#")]; if (v2 != null) { let i = 0; return v2.replace(/#/g, () => nums[i++] ?? "#").split("@").join(D[nm] != null ? D[nm] : nm); } } } }   /* V695: Name + Zahl im selben Text */''')
open(dst, "w", encoding="utf8").write(s)
print("ok V695")
