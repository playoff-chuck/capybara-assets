"""V373 (To-do 87, Martin): Kontinent-Monster nur auf ihrem Kontinent – Jaguar Südamerika (bis W30), Mumie Afrika (W31–60),
Tiger Asien (W61–90), Bär Nordamerika (W91–120). Danach kommen sie nicht mehr.
To-do 88: In Nuts-Levels nur Waffen/Specials/Monster, die im Hauptspiel bis zur Abstecher-Startwelle vorgestellt wurden."""
import sys
src, dst = sys.argv[1], sys.argv[2]
s = open(src, encoding='utf-8').read()
def rep(a, b, cnt=1):
    global s
    n = s.count(a); assert n == cnt, (n, a[:70]); s = s.replace(a, b)
rep('const GAME_VER = "V372";', 'const GAME_VER = "V373";')
rep('''  else if (w >= (G.bearFrom || 999) && idx % 11 === 7) kind = "bear";
  else if (w >= (G.tigerFrom || 999) && idx % 9 === 4) kind = "tiger";
  else if (w >= (G.mummyFrom || 999) && idx % 8 === 6) kind = "mummy";
  else if (w >= (G.jaguarFrom || 999) && idx % 7 === 1) kind = "jaguar";''',
'''  else if (w >= (G.bearFrom || 999) && w <= 120 && idx % 11 === 7) kind = "bear";        /* V373: nur Nordamerika */
  else if (w >= (G.tigerFrom || 999) && w <= 90 && idx % 9 === 4) kind = "tiger";       /* V373: nur Asien */
  else if (w >= (G.mummyFrom || 999) && w <= 60 && idx % 8 === 6) kind = "mummy";       /* V373: nur Afrika */
  else if (w >= (G.jaguarFrom || 999) && w <= 30 && idx % 7 === 1) kind = "jaguar";     /* V373: nur Südamerika */''')
# To-do 88: Nuts-Levels nur mit Dingen, die im Hauptspiel schon vorgestellt wurden (Stand = Startwelle des Abstechers)
rep('function unlocked(k, wave = Math.max(1, S.wave)) { return wave >= unlockedAt(k); }',
    'function unlocked(k, wave = Math.max(1, S.wave)) { if (S && S.nuts) wave = Math.min(wave, S.nuts.mainW || S.nuts.base); return wave >= unlockedAt(k); }   /* V373: Nuts nur Vorgestelltes */')
rep('  const intro = { volt: "New: Sparky!',
    '  if (S.nuts && kind !== "norm" && monFrom(kind) > (S.nuts.mainW || S.nuts.base)) kind = "norm";   /* V373: Nuts – keine Monster, die im Hauptspiel noch nicht vorgestellt wurden */\n  const intro = { volt: "New: Sparky!')
rep('S.nuts = { c, base: NZ_BASES[c], lvl: 0, cleared: 0, first: NZ.first };',
    'S.nuts = { c, base: NZ_BASES[c], lvl: 0, cleared: 0, first: NZ.first, mainW: Math.max(1, Math.min(NZ_BASES[c], +fr.wave || NZ_BASES[c])) };   /* V373: Stand im Hauptspiel */')
rep('S.snipes = 2; S.mixers = 2; S.teslas = 2; S.chomps = 2; S.tons = 2; S.locks = 2;',
    'S.snipes = 2; S.mixers = 2; S.teslas = 2; S.chomps = 2; S.tons = 2; S.locks = 2; for (const [k, f] of [["snipe", "snipes"], ["mix", "mixers"], ["tesla", "teslas"], ["chomp", "chomps"], ["ton", "tons"], ["lock", "locks"]]) if (!unlocked(k)) S[f] = 0;   /* V373: nur Vorgestelltes */')
open(dst, 'w', encoding='utf-8').write(s)
print("ok")
