"""V298 (Martin 19:02): Dev-Leiste: neuer Knopf «AA» (Afrika → Asien). Startet Welle 60 (letzte Welle Afrika) mit nur 2 Monstern,
die nach ~10 s verschwinden; dann läuft der Übergang nach Asien wie im echten Spiel.
Übergang gedrosselt: Wegweiser erst 5 s nach dem letzten Fenster, nach der Kontinent-Szene 6 s Pause vor der ersten Welle,
kein doppeltes «WELCOME TO …»-Banner (Begrüßung läuft beim Ankunftsbild)."""
import sys
src, dst = sys.argv[1], sys.argv[2]
s = open(src, encoding='utf-8').read()
def rep(a, b, cnt=1):
    global s
    n = s.count(a); assert n == cnt, (n, a[:70]); s = s.replace(a, b)
rep('const GAME_VER = "V297";', 'const GAME_VER = "V298";')
rep('''<button id="devBandit">Bandit</button></div>''', '''<button id="devBandit">Bandit</button><button id="devAA">AA</button></div>''')
rep('''      d.addEventListener("click", e => { const b = e.target.closest("button"); if (!b) return; e.stopPropagation();''',
    '''      window.__devAA = () => { try { SFX.init(); snd("confirm"); } catch (e) {} devJump(60); let t0 = 0; const iv = setInterval(() => { try { if (!S || S.over) { clearInterval(iv); return; }
          if (S.wave === 60 && S.inWave) { if (!t0) { t0 = performance.now(); S.toSpawn = Math.min(S.toSpawn, 2); S.waveTotal = Math.min(S.waveTotal || 2, 2); }
            if (performance.now() - t0 > 10000) { S.toSpawn = 0; S.monsters = []; clearInterval(iv); } } else if (S.wave > 60) clearInterval(iv); } catch (e) { clearInterval(iv); } }, 200); };
      d.addEventListener("click", e => { const b = e.target.closest("button"); if (!b) return; e.stopPropagation(); if (b.id === "devAA") { window.__devAA(); return; }''')
# Übergang Afrika → Asien drosseln (gemessen: Orders 1,6 s nach Wellenende, Wegweiser 0,3 s nach Orders, Welle 61 startet sofort nach der Karte)
# 1) Wegweiser erst 5 s nach dem letzten Fenster
rep('if (hkSignFirst()) { if (!S.drop && !S.intro && !S.duel && !S.paused && inPlay() && !hkOfferOn()) showSign(NZ_BASES.indexOf(S.wave));',
    'if (hkSignFirst()) { if (!S.drop && !S.intro && !S.duel && !S.paused && inPlay() && !hkOfferOn() && performance.now() - (window.__evtLast || -1e9) >= 5000) showSign(NZ_BASES.indexOf(S.wave));')
rep('  if (S.toSpawn > 0 || S.monsters.length || S.ordDue || hkOfferOn() || !inPlay()) return;\n  showSign(c);',
    '  if (S.toSpawn > 0 || S.monsters.length || S.ordDue || hkOfferOn() || !inPlay() || performance.now() - (window.__evtLast || -1e9) < 5000) return;\n  showSign(c);')
# 2) Nach der Kontinent-Szene 6 s Pause, bevor die erste Welle startet
rep('play(() => { S.paused = was; S.mapShow = false; busy = false; _sw2.apply(self, a); }); return; } } } catch (e) { busy = false; }',
    'play(() => { S.paused = was; S.mapShow = false; busy = false; if (P.p === 0) { S.mapDoneFor = nw; S.waveCD = 6; return; } _sw2.apply(self, a); }); return; } } } catch (e) { busy = false; }')
rep('try { if (!busy && S && S.started && !S.over && !S.nuts) { const nw = (S.wave || 0) + 1, P = wherePos(nw);',
    'try { if (!busy && S && S.started && !S.over && !S.nuts && S.mapDoneFor !== (S.wave || 0) + 1) { const nw = (S.wave || 0) + 1, P = wherePos(nw);')
# 3) Kein zweites «WELCOME TO …»-Banner, wenn die Begrüßung schon beim Ankunftsbild lief
rep('setTimeout(() => { announce(`WELCOME TO ${P.cont[1]}!`, `${P.place} · a new continent`, "HQ", 3000); if (window.__contSaid !== S.wave) SFX.say(vk); }, 900);',
    'setTimeout(() => { if (window.__contSaid === S.wave) return; announce(`WELCOME TO ${P.cont[1]}!`, `${P.place} · a new continent`, "HQ", 3000); SFX.say(vk); }, 900);')
open(dst, 'w', encoding='utf-8').write(s)
