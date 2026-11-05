"""V265 (Martin 05.11. 15:02–15:06):
- Lucky Supply nicht mehr nur einmal: erstmals ab ~60 s Spielzeit, danach alle 5–7 Wellen, jeweils mindestens 45 s nach jedem anderen Fenster.
- Sale-Anzeigen jetzt auch für Chomper (W17), Tesla storm (W21) und Lockdown (W25) (Nano Banana Pro, je ca. 0,14 $).
- Anzeigen kommen nicht mehr starr zur Freischalt-Welle: dort erscheint nur das normale Neuheiten-Fenster; die Anzeige folgt
  später, sobald der Spieler das Gold (und bei Kanone/Frost einen freien Turmplatz) hat – an einer ruhigen Stelle und
  mindestens 45 s nach jedem anderen Fenster/Ereignis (Neuheit, Anzeige, Bandit, Karte, Boss, Rufzeichen, Ortsschild …).
- Ten-ton: das Geschenk kommt wie bisher mit dem Neuheiten-Fenster; die Sale-Anzeige später (600 Gold)."""
import sys
src, dst = sys.argv[1], sys.argv[2]
s = open(src, encoding='utf-8').read()
def rep(a, b, cnt=1):
    global s
    n = s.count(a); assert n == cnt, (n, a[:70]); s = s.replace(a, b)
rep('const GAME_VER = "V264";', 'const GAME_VER = "V265";')
rep('''                 mix: { img: "img/ad_mix.webp",''', '''                 chomp: { img: "img/ad_chomp_sale.webp", sale: "img/ad_chomp_sale.webp", st: [[11, 37], [12, 74], [88, 18]], tag: "NEW GEAR", line: "Steel jaws run the ring backwards – eating everything!" },
                 tesla: { img: "img/ad_tesla_sale.webp", sale: "img/ad_tesla_sale.webp", st: [[11, 37], [12, 74], [88, 18]], tag: "NEW GEAR", line: "4×4 lightning strike. Splats count triple!" },
                 lock: { img: "img/ad_lock_sale.webp", sale: "img/ad_lock_sale.webp", st: [[11, 37], [12, 74], [88, 18]], tag: "NEW GEAR", line: "Freeze time for 8 s – cleared lines explode together!" },
                 mix: { img: "img/ad_mix.webp",''')
rep('k === "snipe" ? SNIPE_COST : TON_COST;', 'k === "snipe" ? SNIPE_COST : k === "chomp" ? CHOMP_COST : k === "tesla" ? TESLA_COST : k === "lock" ? LOCK_COST : TON_COST;')
rep('else if (k === "snipe") S.snipes = (S.snipes || 0) + 1; else S.tons = (S.tons || 0) + 1;',
    'else if (k === "snipe") S.snipes = (S.snipes || 0) + 1; else if (k === "chomp") S.chomps = (S.chomps || 0) + 1; else if (k === "tesla") S.teslas = (S.teslas || 0) + 1; else if (k === "lock") S.locks = (S.locks || 0) + 1; else S.tons = (S.tons || 0) + 1;')
# Freischaltung: nur vormerken, Anzeige kommt später
rep('if (q && q.t === "gear" && AD[q.k] && (S.wave || 0) <= 14 && !S.nuts) {', 'if (q && q.t === "gear" && AD[q.k] && !S.nuts) {')
rep('const recent = performance.now() - (window.__adLast || -1e9) < 45000;\n          if (q.k === "ton") { if (!recent) show("ton", false); S.adDue.ton = 1; }',
    'S.adDue[q.k] = 1;   // V265: Anzeige immer später, wenn bezahlbar und ruhig (Neuheiten-Fenster bleibt)\n          if (false) {}')
rep('else if (!why(q.k) && !recent) show(q.k, true);', 'else if (false) show(q.k, true);')
rep('else { S.adDue[q.k] = 1; $("ovIntro").hidden = true; try { closeIntro(); } catch (e) {} }   // sonst später, wenn nutzbar', '')
rep('for (const k of ["kan", "frost", "mix", "snipe", "ton"]) if (S.adDue[k] && !why(k))', 'for (const k of ["kan", "frost", "mix", "snipe", "ton", "chomp", "tesla", "lock"]) if (S.adDue[k] && !why(k))')
rep('if (!S || !S.adDue || !calm() || performance.now() - (window.__adLast || -1e9) < 45000) return;',
    'if (!S || !S.adDue || !calm() || performance.now() - Math.max(window.__adLast || -1e9, window.__evtLast || -1e9) < 45000) return;')
# Check news: neue Anzeigen mit aufnehmen
rep('const AD = ["kan", "ton", "mix", "frost", "snipe"];', 'const AD = ["kan", "ton", "mix", "frost", "snipe", "chomp", "tesla", "lock"];')
js = r'''
  /* V265: letzte Zeit eines sichtbaren Fensters/Ereignisses merken (Abstand für Anzeigen) */
  try { setInterval(() => { try { if (!S || !S.started) return; const v = id => { const e = document.getElementById(id); return e && !e.hidden && getComputedStyle(e).display !== "none"; };
      const b = document.body.classList;
      if (S.intro || S.alert || S.duel || S.drop || S.ordersOpen || S.signOpen || S.joinOpen || S.banditOpen || S.mapShow || S.mapFly || S.paused || b.contains("mapUp") || b.contains("introWin")
          || v("ovIntro") || v("ovAd") || v("ovBandit") || (typeof hkOfferOn === "function" && hkOfferOn()) || (typeof TUT !== "undefined" && TUT.on)) window.__evtLast = performance.now();
    } catch (e) {} }, 300); } catch (e) {}
'''
i = s.rfind('})();\n</script>'); s = s[:i] + js + s[i:]
open(dst, 'w', encoding='utf-8').write(s); print('ok')
# Nachtrag 15:06: Lucky Supply alle 5–7 Wellen (erstmals ab ~60 s), mindestens 45 s nach jedem anderen Fenster
s = open(dst, encoding='utf-8').read()
rep('if (S) { S.banditDone = true; wasPaused = !!S.intro;', 'if (S) { S.banditDone = true; S.banditNext = (S.wave || 1) + 5 + Math.floor(Math.random() * 3); wasPaused = !!S.intro;')
rep('if (typeof SAVE_KEYS !== "undefined" && !SAVE_KEYS.includes("banditDone")) SAVE_KEYS.push("banditDone");', 'if (typeof SAVE_KEYS !== "undefined") ["banditDone", "banditNext"].forEach(k => { if (!SAVE_KEYS.includes(k)) SAVE_KEYS.push(k); });')
rep('const calm = () => S && S.started && !S.over && !S.nuts && !S.banditDone && (S.playT || 0) >= 60 && !S.inWave',
    'const calm = () => S && S.started && !S.over && !S.nuts && (S.banditNext ? (S.wave || 0) >= S.banditNext : !S.banditDone) && (S.playT || 0) >= 60 && performance.now() - Math.max(window.__evtLast || -1e9, window.__adLast || -1e9) >= 45000 && !S.inWave')
rep('iw: S.introWave, bd: S.banditDone,', 'iw: S.introWave, bd: S.banditDone, bn: S.banditNext,')
rep('S.introWave = z.iw; S.banditDone = z.bd;', 'S.introWave = z.iw; S.banditDone = z.bd; S.banditNext = z.bn;')
open(dst, 'w', encoding='utf-8').write(s); print('ok3')
