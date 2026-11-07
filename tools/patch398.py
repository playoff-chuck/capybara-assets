"""V398: Wolf call im Shop wie die anderen Specials: eine Kachel mit BUY + USE ×n (statt zwei breiter Kacheln).
Aufruf: python3 tools/patch398.py site/index.html site/index.html"""
import re, sys
src, dst = sys.argv[1], sys.argv[2]
s = open(src, encoding='utf-8').read()
def rep(a, b, cnt=1):
    global s
    n = s.count(a); assert n == cnt, (n, a[:70]); s = s.replace(a, b)
m = re.search(r'const GAME_VER = "V(\d+)";', s); old = int(m.group(1)); NEW = old + 1
rep(f'const GAME_VER = "V{old}";', f'const GAME_VER = "V{NEW}";')
rep('const OWN = { snipe: S.snipes, tesla: S.teslas, mix: S.mixers, chomp: S.chomps, ton: S.tons, lock: S.locks, coach: coachLeft() };',
    'const OWN = { snipe: S.snipes, tesla: S.teslas, mix: S.mixers, chomp: S.chomps, ton: S.tons, lock: S.locks, wolf: S.wolves || 0, coach: coachLeft() };')
rep('''  if (S.wolves > 0) rows.push([WOLF_W - 0.1, shopItem("shop", "wolfuse", ICON.tesla, "Wolf call", `×${S.wolves}`, "Howl now: a thief runs off and drops your gold. No thief? Then it's wasted.", "USE", false, "btn-accent")]);
''', '')
open(dst, 'w', encoding='utf-8').write(s); print("ok V%d" % NEW)
