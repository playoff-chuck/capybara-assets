"""V288 (Martin 17:16–17:18):
- Kontinent-Begrüßung («Welcome to Africa! Hot sand, cool moves!» usw.) kommt jetzt mit dem Ankunftsbild der Capybaras,
  nicht erst beim Wellenstart (dort entfällt der Spruch, wenn er schon beim Bild lief).
- Letzte Waffen-Vorstellung im alten Fenster ersetzt: «Elite upgrades» (W31, Afrika) als Werbeanzeige im Gratis-Stil
  (Bild intro/in_<held>_elite.webp, «LV 3» → «LV 5», «NEW!», Knopf «AWESOME! · LET'S GO ▶»). Damit laufen alle Waffen/Gadgets als Anzeigen.
- Haupt-Knöpfe in Anzeigen und Neuheiten sofort drückbar (nur «No thanks» 3 s gesperrt).
- Sale-Plaketten auf festen Plätzen (links 40 %/76 %, unten Mitte), nie über Capybara-Gesichtern."""
import sys
src, dst = sys.argv[1], sys.argv[2]
s = open(src, encoding='utf-8').read()
def rep(a, b, cnt=1):
    global s
    n = s.count(a); assert n == cnt, (n, a[:70]); s = s.replace(a, b)
rep('const GAME_VER = "V287";', 'const GAME_VER = "V288";')
# Begrüßung beim Ankunftsbild
rep('arrOrigin(arrC); ov.appendChild(arrC); requestAnimationFrame(() => requestAnimationFrame(() => arrC.classList.add("on")));',
    'arrOrigin(arrC); ov.appendChild(arrC); requestAnimationFrame(() => requestAnimationFrame(() => arrC.classList.add("on"))); setTimeout(() => { try { if (!seqDone) return; const vk = { africa: "welcome_africa", asia: "welcome_asia", namerica: "welcome_namerica" }[ak] || "newcont"; window.__contSaid = w; SFX.say(vk, 1, 1, SFX.reserveVoice(SFX.voiceDur(vk) * 1000 + 400)); } catch (e) {} }, 900);')
rep('announce(`WELCOME TO ${P.cont[1]}!`, `${P.place} · a new continent`, "HQ", 3000); SFX.say(vk);',
    'announce(`WELCOME TO ${P.cont[1]}!`, `${P.place} · a new continent`, "HQ", 3000); if (window.__contSaid !== S.wave) SFX.say(vk);')
# Elite als Anzeige
rep('                 mix: { img: "img/ad_mix.webp",',
    '                 elite: { img: "intro/in_blue_elite.webp", sale: "intro/in_blue_elite.webp", st: [[80, 18], [14, 40], [14, 74]], tag: "NEW POWER", line: "Tower levels 4 and 5 are unlocked. Tap a tower and go elite!" },\n                 mix: { img: "img/ad_mix.webp",')
rep('if (q.k === "ton") { if (!S.tonIntroGift) { S.tonIntroGift = true; S.tons = (S.tons || 0) + 1; } S.adDue.ton = 1; late = true; S.intro = true; S.adOpen = true; show("ton", "free"); }',
    'if (q.k === "ton") { if (!S.tonIntroGift) { S.tonIntroGift = true; S.tons = (S.tons || 0) + 1; } S.adDue.ton = 1; late = true; S.intro = true; S.adOpen = true; show("ton", "free"); }\n          else if (q.k === "elite") { late = true; S.intro = true; S.adOpen = true; show("elite", "free"); }')
rep('''$a("adPic").style.backgroundImage = `url(${a.sale})`; }
        else { s2.textContent = "HOT!";''',
    '''$a("adPic").style.backgroundImage = `url(${a.sale})`;
          if (k === "elite") { let h = "blue"; try { h = heroKey(); } catch (e) {} $a("adPic").style.backgroundImage = `url(intro/in_${h}_elite.webp)`; $a("adPic").style.backgroundPosition = "50% 88%"; $a("saleWas").textContent = "LV 3"; $a("saleNow").textContent = "LV 5"; $a("salePct").textContent = "NEW!"; $a("saleS1").textContent = "NEW!"; s2.textContent = "ELITE"; s3.textContent = "×5"; mg.textContent = "NEW POWER"; on.textContent = "TOWERS GO ELITE!"; $a("adTag").textContent = "NEW"; $a("adPrice").textContent = "ELITE"; } }
        else { s2.textContent = "HOT!";''')
rep('`<button class="btn-accent" id="adFree">AWESOME! · IT\'S FREE ▶</button>`',
    '`<button class="btn-accent" id="adFree">${cur === "elite" ? "AWESOME! · LET\'S GO ▶" : "AWESOME! · IT\'S FREE ▶"}</button>`')
rep('$a("adPic").style.backgroundImage = `url(${sale ? a.sale : a.img})`;', '$a("adPic").style.backgroundImage = `url(${sale ? a.sale : a.img})`; $a("adPic").style.backgroundPosition = "";')
# Martin 17:18/17:19: Haupt-Knöpfe (I WANT IT, IT'S FREE, GOT IT bei Monstern, Lucky Supply, Rufzeichen) sofort drückbar, nicht blass.
# Nur «No thanks/Later» der Werbung bleibt 3 s gesperrt (gegen versehentliches Wegtippen).
rep('if (el && el.classList.contains("lock3") && el.contains(e.target)) { e.stopImmediatePropagation(); e.preventDefault(); return; }',
    'if (el && el.classList.contains("lock3") && el.contains(e.target) && e.target.closest("#adLater")) { e.stopImmediatePropagation(); e.preventDefault(); return; }')
# Sale-Plaketten: feste Plätze links und unten Mitte – nie auf Capybara-Gesichtern (die sitzen rechts im Bild)
rep('if (el && a.st) { let x = Math.max(13, Math.min(87, a.st[n - 1][0])), y = Math.max(15, Math.min(85, a.st[n - 1][1])); if (x > 66 && y < 30) y = 33;',
    'if (el && a.st) { const PS = k === "elite" ? [[80, 30], [14, 30], [80, 72]] : [[14, 40], [14, 76], [52, 86]]; let x = PS[n - 1][0], y = PS[n - 1][1];')
css3 = """
<style id="v288lock">
.lock3 button,.lock3 .btn-accent{pointer-events:auto!important;opacity:1!important;filter:none!important}
.lock3 #adLater{pointer-events:none!important;opacity:.45!important}
</style>
"""
i = s.rindex('</body>'); s = s[:i] + css3 + s[i:]
open(dst, 'w', encoding='utf-8').write(s)
