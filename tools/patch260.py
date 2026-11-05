"""V260 (Martin 05.11. 13:56–13:59):
- Begrüßung statt doppeltem «Let's go»: beim Welttour-Start auf der Karte «Welcome to Capybara World!» und neuer Clip in Martins
  Stimme «Welcome to Capybara World! Here we go!» (HeyGen, voice/welcome.mp3, 2,7 s, 0,001 $). Der «Let's go»-Spruch beim
  Spielstart entfällt, wenn gerade das Karten-Intro lief.
- Frost (Welle 11) und Sniper strike (Welle 13) ebenfalls als Sale-Anzeige (Nano Banana Pro). Frost wie die Kanone: erst wenn ein
  Turm mit freiem Platz + Gold da ist (wird sofort montiert); Sniper erst mit 200 Gold (in die Pocket).
- «Street player» behält die Einstellung «Intros: off», damit man nach dem Zurücksetzen normal durchspielen kann."""
import sys, base64
src, dst = sys.argv[1], sys.argv[2]
s = open(src, encoding='utf-8').read()
def rep(a, b, cnt=1):
    global s
    n = s.count(a); assert n == cnt, (n, a[:70]); s = s.replace(a, b)
rep('const GAME_VER = "V259";', 'const GAME_VER = "V260";')
b64 = base64.b64encode(open(sys.argv[3], 'rb').read()).decode()
rep('const VOICE_TEXT = {', 'const VOICE_TEXT = {"welcome": "Welcome to Capybara World! Here we go!", ')
rep('const VOICE = {', 'const VOICE = {"welcome":"' + b64 + '",')
rep('label("", "The world tour begins", "5 continents · 30 places · 150 waves");', 'label("", "Welcome to Capybara World!", "5 continents · 30 places · 150 waves"); window.__introAt = performance.now();')
rep('try { SFX.say && SFX.say("newcont"); } catch (e) {} });', 'try { SFX.say && SFX.say("welcome", 1.0, 1.0, "welcome"); } catch (e) {} });')
rep('setTimeout(() => SFX.say(pool[Math.floor(Math.random() * pool.length)], 1.1, 1.05), 400); }',
    'setTimeout(() => { if (performance.now() - (window.__introAt || -1e9) < 25000) return; SFX.say(pool[Math.floor(Math.random() * pool.length)], 1.1, 1.05); }, 400); }')
# Anzeigen Frost + Sniper
rep('''                 mix: { img: "img/ad_mix.webp",''', '''                 frost: { img: "img/ad_frost_sale.webp", sale: "img/ad_frost_sale.webp", st: [[11, 37], [12, 74], [88, 18]], tag: "NEW GEAR", line: "Slows everything it hits. Pair it with an MG." },
                 snipe: { img: "img/ad_snipe_sale.webp", sale: "img/ad_snipe_sale.webp", st: [[80, 16], [11, 49], [12.5, 79]], tag: "NEW GEAR", line: "One shot wipes a 2×2 patch – splats all around it!" },
                 mix: { img: "img/ad_mix.webp",''')
rep("if (q && q.t === \"gear\" && AD[q.k] && (S.wave || 0) <= 10 && !S.nuts) {", "if (q && q.t === \"gear\" && AD[q.k] && (S.wave || 0) <= 14 && !S.nuts) {")
rep('const price = k => k === "kan" ? WEAP.kan.cost : k === "mix" ? MIX_COST : TON_COST;',
    'const TOWERW = { kan: 1, frost: 1 }; const price = k => TOWERW[k] ? WEAP[k].cost : k === "mix" ? MIX_COST : k === "snipe" ? SNIPE_COST : TON_COST;')
rep('if (k === "kan" && !slotTower()) return', 'if (TOWERW[k] && !slotTower()) return')
rep('if (k === "kan") { const t = slotTower(); if (!t) { paint(); return; } t.w.push({ type: "kan", lvl: 1, cd: 0 }); }',
    'if (TOWERW[k]) { const t = slotTower(); if (!t) { paint(); return; } t.w.push({ type: k, lvl: 1, cd: 0 }); }')
rep('else if (k === "mix") S.mixers = (S.mixers || 0) + 1; else S.tons = (S.tons || 0) + 1;',
    'else if (k === "mix") S.mixers = (S.mixers || 0) + 1; else if (k === "snipe") S.snipes = (S.snipes || 0) + 1; else S.tons = (S.tons || 0) + 1;')
rep('for (const k of ["kan", "mix", "ton"]) if (S.adDue[k] && !why(k))', 'for (const k of ["kan", "frost", "mix", "snipe", "ton"]) if (S.adDue[k] && !why(k))')
rep('${k === "kan" ? "mounted on your tower" : "in your Pocket"}', '${TOWERW[k] ? "mounted on your tower" : "in your Pocket"}')
rep('const keep = ["tarnturm-dev"];', 'const keep = ["tarnturm-dev", "tarnturm-devnointro"];')
open(dst, 'w', encoding='utf-8').write(s); print('ok')
