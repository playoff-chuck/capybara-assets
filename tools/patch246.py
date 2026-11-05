"""V246: Neue Bilder (Nano Banana Pro, 05.11.2026): Orts-Hintergruende fuer South America, North America und Antarctica
(je 6, bg/pl_<kont>_<0-5>.webp) und Ankunftsbilder fuer Africa, Asia, North America, Antarctica (img/arrive_<kont>.webp),
gezeigt nach dem Kontinent-Flug wie das Startbild in Suedamerika. Antarctica nutzt intern den Schluessel "asia" -> eigene
Hintergruende ueber den Kontinent-Index."""
import sys
src, dst = sys.argv[1], sys.argv[2]
s = open(src, encoding='utf-8').read()
def rep(a, b, cnt=1):
    global s
    n = s.count(a); assert n == cnt, (n, a[:70]); s = s.replace(a, b)
rep('const GAME_VER = "V245";', 'const GAME_VER = "V246";')
rep('const PLACE_BG = { africa: [0, 1, 2, 3, 4, 5].map(i => `bg/pl_africa_${i}.webp`), asia: [0, 1, 2, 3, 4, 5].map(i => `bg/pl_asia_${i}.webp`) };',
    'const PLACE_BG = Object.fromEntries(["samerica", "africa", "asia", "namerica", "antarctica"].map(k => [k, [0, 1, 2, 3, 4, 5].map(i => `bg/pl_${k}_${i}.webp`)]));   // V246: alle 5 Kontinente')
rep('const im = SKY_BG[P.cont[0]], pl = (PLACE_BG[P.cont[0]] || [])[P.p];',
    'const im = SKY_BG[P.cont[0]], pl = (PLACE_BG[P.c === 4 ? "antarctica" : P.cont[0]] || [])[P.p];')
# Ankunftsbild nach dem Kontinent-Flug
rep('function playCont(w, done) { const P = posOf(w), oc = Math.max(0, P.c - 1); seqDone = done;',
    'function playCont(w, done) { const P = posOf(w), oc = Math.max(0, P.c - 1); let arrC = null; seqDone = () => { try { arrC && arrC.remove(); } catch (e) {} if (done) done(); };')
rep("""label(contName(P.c), `Welcome to ${nice(contName(P.c))}!`, `First stop: ${nice(CONTS[P.c][2][0])}`); fx("tonHit");""",
    """label(contName(P.c), `Welcome to ${nice(contName(P.c))}!`, `First stop: ${nice(CONTS[P.c][2][0])}`); fx("tonHit");
        const ak = ["samerica", "africa", "asia", "namerica", "antarctica"][P.c];
        if (ak && P.c > 0) setTimeout(() => { try { if (!seqDone) return; arrC = document.createElement("div"); arrC.className = "mapArrive"; arrC.innerHTML = `<img src="img/arrive_${ak}.webp" alt=""><div class="maTxt"><small>WORLD TOUR · CONTINENT ${P.c + 1} OF 5</small><b>${contName(P.c)}</b><span>${nice(CONTS[P.c][2][0])} · wave ${w}</span></div>`; ov.appendChild(arrC); requestAnimationFrame(() => arrC.classList.add("on")); } catch (e) {} }, 700);""")
rep('      at(11000, hide); }\n    function playIntro(done)', '      at(12600, hide); }\n    function playIntro(done)')
open(dst, 'w', encoding='utf-8').write(s); print('ok')
