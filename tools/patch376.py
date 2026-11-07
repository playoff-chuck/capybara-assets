"""V376 (To-do 40, Martin 13:06 «einfach lösen»): Kleinigkeiten nach Kartenszene und Game over.
- Über der Game-over-Karte erscheinen keine Lob-, Orts- oder Funk-Meldungen mehr (praise/toast/announce schweigen, solange ovOver offen ist).
- Nach dem Finale (Welle 150) kommt ein kurzer Abspann (läuft 14 s, Antippen schließt)."""
import sys
src, dst = sys.argv[1], sys.argv[2]
s = open(src, encoding='utf-8').read()
def rep(a, b, cnt=1):
    global s
    n = s.count(a); assert n == cnt, (n, a[:70]); s = s.replace(a, b)
rep('const GAME_VER = "V375";', 'const GAME_VER = "V376";')
rep('function announce(title, sub, tag = "RADIO", hold = 1800) {',
    'function overShown() { const o = document.getElementById("ovOver"); return !!(o && !o.hidden); }   /* V376: Game-over-Karte offen */\n'
    'function announce(title, sub, tag = "RADIO", hold = 1800) {\n  if (overShown()) return;')
rep('function praise(text, tier, speech) {', 'function praise(text, tier, speech) {\n  if (overShown()) return;')
rep('function toast(msg, tag = "REPORT", hold = 1700) {', 'function toast(msg, tag = "REPORT", hold = 1700) {\n  if (overShown()) return;')
rep('setTimeout(() => gameOver("World tour complete"), 1800);',
    'setTimeout(() => gameOver("World tour complete"), 1800); setTimeout(showCredits, 5200);')
rep('function startWave() {',
    'function showCredits() {   /* V376: Abspann nach dem Finale */\n'
    '  if (document.getElementById("credits")) return; const d = document.createElement("div"); d.id = "credits";\n'
    '  const L = ["CAPYBARA SQUAD", "", "WORLD TOUR COMPLETE", "150 waves · 5 continents · 30 places", "", "THE SQUAD", "Rosie · Blue", "The General", "Doc Hazel", "The Paymaster", "", "THE VILLAINS", "Scouts · Brutes · Munchers", "Sprinters · Bombers · Sparky", "Jaguars · Mummies · Tigers · Bears", "The Jaw · the raccoon thief", "", "Made with love for capybaras", "", "THANKS FOR PLAYING!", "See you on the next tour"];\n'
    '  d.innerHTML = `<div class="crRoll">${L.map(t => t ? `<p>${t}</p>` : "<br>").join("")}</div>`;\n'
    '  const close = () => { d.classList.add("out"); setTimeout(() => d.remove(), 600); };\n'
    '  d.addEventListener("click", close); document.body.appendChild(d); setTimeout(close, 14000); try { snd("jingle"); } catch (e) {} }\n'
    'function startWave() {')
rep('.mPin.done i{background:#ffc93c}',
    '.mPin.done i{background:#ffc93c}\n'
    '#credits{position:fixed;inset:0;z-index:2147483100;background:rgba(16,21,13,.94);overflow:hidden;display:flex;justify-content:center;transition:opacity .6s}\n'
    '#credits.out{opacity:0}\n'
    '#credits .crRoll{position:absolute;top:100%;width:100%;max-width:420px;padding:0 16px;box-sizing:border-box;text-align:center;animation:crUp 14s linear forwards}\n'
    '#credits p{margin:0 0 10px;font:400 22px/1.15 var(--f-display,"Bangers",sans-serif);letter-spacing:.05em;color:#fff7e8}\n'
    '#credits p:first-child{font-size:38px;color:#ffd84d}\n'
    '@keyframes crUp{to{transform:translateY(calc(-100% - 100vh))}}\n'
    '@media (prefers-reduced-motion:reduce){#credits .crRoll{animation:none;top:10%}}')
open(dst, 'w', encoding='utf-8').write(s)
print("ok")
