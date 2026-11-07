"""V366 (Martin 07.11. 08:17): Zu Martins Stimme immer nur Blue zeigen, nie Rosie.
- Sprechblasen der Rosie-&-Blue-Sprüche: immer Blue.
- Trostkarte bei Game over (dazu spricht Blue «rb_tea») und Siegkarte («godlike»): immer Blue.
Punkt 7 – Sprüche verdrängen nichts mehr:
- Läuft ein Rosie-&-Blue-Spruch (rb_…), unterbricht ihn jede andere Sprachmeldung (vorher fiel die andere Meldung ganz weg).
- Ein Spruch wartet, solange die Sprechblase für einen Spezialwaffen-Ruf steht, und schließt sie nicht mehr vorzeitig."""
import sys
src, dst = sys.argv[1], sys.argv[2]
s = open(src, encoding='utf-8').read()
def rep(a, b, cnt=1):
    global s
    n = s.count(a); assert n == cnt, (n, a[:70]); s = s.replace(a, b)
rep('const GAME_VER = "V365";', 'const GAME_VER = "V366";')
rep('const who = ROSIE_K.includes(key) ? "rosie" : "blue";', 'const who = "blue";   // V366: Martins Stimme = immer Blue')
rep('const c = document.querySelector("#ovOver .comfort"), b = buddyKey();', 'const c = document.querySelector("#ovOver .comfort"), b = "blue";   // V366: dazu spricht Martins Stimme -> Blue')
rep('if (s) s.textContent = (buddyKey() === "rosie" ? "ROSIE" : "BLUE") + " SAYS";', 'if (s) s.textContent = "BLUE SAYS";')
rep('    if (curVoice) return;                                                     // es läuft schon eine Meldung: die neue fällt komplett weg',
    '    if (curVoice && !(curVoice.__rb && !/^rb_/.test(String(text)))) return;   // es läuft schon eine Meldung: die neue fällt komplett weg – außer ein Rosie-&-Blue-Spruch (V366)\n    if (curVoice) { try { curVoice.stop(); } catch (e) {} curVoice = null; }')
rep('src.start(t0); curVoice = src;', 'src.start(t0); curVoice = src; src.__rb = /^rb_/.test(String(text));')
rep('void el.offsetWidth; el.classList.add("on"); clearTimeout(bT); bT = setTimeout(() => el.classList.remove("on"), 2800); }',
    'void el.offsetWidth; el.classList.add("on"); clearTimeout(bT); const mine = el.querySelector(".say").innerHTML; bT = setTimeout(() => { if (el.querySelector(".say").innerHTML === mine) el.classList.remove("on"); }, 2800); }')
rep('const busy = SFX.voiceBusy || (!force &&', 'const bb = document.getElementById("buddy"), busy = SFX.voiceBusy || !!(bb && bb.classList.contains("on")) || (!force &&')
open(dst, 'w', encoding='utf-8').write(s)
print("ok")
