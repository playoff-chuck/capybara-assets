"""V235: Nuts-Abstecher nicht mehr spartanisch. Bisher stand der Abstecher immer auf Welle 30/60/… = «22:00 NIGHT»
→ Nachthimmel und fast deckendes Feld (88 %). Jetzt eigener Nuts-Look: Wahrzeichen-Hintergrund des Kontinents
sichtbar, rot glühender Abendhimmel, Feld durchscheinend (42 %)."""
import sys
src, dst = sys.argv[1], sys.argv[2]
s = open(src, encoding='utf-8').read()
def rep(a, b, cnt=1):
    global s
    n = s.count(a); assert n == cnt, (n, a[:70]); s = s.replace(a, b)
rep('const GAME_VER = "V234";', 'const GAME_VER = "V235";')
rep('function wherePos(w) {', 'const NUTS_D = { t: "", n: "NUTS", th: "moon", field: "rgba(52,18,14,.42)", f: "sepia(.2) saturate(1.35) brightness(.92) hue-rotate(-10deg)", night: .12, tint: "linear-gradient(180deg,rgba(210,40,30,.34),rgba(90,12,10,.22))" };\nfunction wherePos(w) {')
rep('const P = wherePos(live ? S.wave || 1 : 1), D = live ? DAY[P.d] : DAY[1];\n  const key = P.cont[0] + "|" + P.p + "|" + (live ? P.d : "menu");',
    'const P = wherePos(live ? S.wave || 1 : 1), D = live ? (S.nuts ? NUTS_D : DAY[P.d]) : DAY[1];\n  const key = P.cont[0] + "|" + P.p + "|" + (live ? (S.nuts ? "nuts" : P.d) : "menu");')
rep('return DAY[wherePos(S.wave || 1).d].th; }', 'return (S.nuts ? NUTS_D : DAY[wherePos(S.wave || 1).d]).th; }')
rep('DAY[wherePos(S.wave || 1).d].field : TH.field;', '(S.nuts ? NUTS_D : DAY[wherePos(S.wave || 1).d]).field : TH.field;')
i = s.rfind('})();\n</script>'); s = s[:i] + '\n  try { window.__TT && (window.__TT.startDetour = c => startDetour(c)); } catch (e) {}\n' + s[i:]
open(dst, 'w', encoding='utf-8').write(s); print('ok')
