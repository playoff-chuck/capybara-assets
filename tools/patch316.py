"""V316: Rettungs-Lucky-Supply ab Welle 30 (Martin 06.11. 12:39: «Bau noch einen Lucky Supply ein, wenn der Spieler in
Schwierigkeiten gerät, ab Level 30 … Die Steine gehen bis 5 Felder unter der Decke … Lucky Supply mit dem 10-Tonnen-Gewicht
und gleich annehmen und anwenden.»).
- Auslöser: Welle ≥ 30, kein Nuts-Abstecher, Stapel reicht bis 5 Felder unter die Decke (stackTopRow() ≤ 5),
  am Spielscreen, 5 s nach dem letzten Fenster, kein Ten-ton gerade im Fall; höchstens einmal je 8 Wellen.
  Rettung geht vor den Angebots-Takt (zählt danach aber als Angebot).
- Automat zeigt immer den Ten-ton; nach dem Gewinn heißt der Knopf «DROP IT ▶» und der Ten-ton fällt sofort.
- Der normale Lucky-Supply-Rhythmus (banditNext) bleibt unberührt.
Dazu (Martin 12:44, «AA»): Kontinent-Feier kam beim zweiten «AA» nicht mehr (window.__celFor blieb stehen) → wird beim
Schließen des Wegweisers zurückgesetzt; Feier-Ebene schluckt alle Tipps (3,3 s, nicht wegdrückbar).
Wild Cards (Martin 12:45): Dauer steht jetzt groß im Kopf («lasts 20 waves – until wave N», «Now»-Effekte einmalig), Meldung nach Wahl «WILD CARD · UNTIL WAVE N».
Martin 12:47/12:48: kein Spielscreen-Blitzer nach dem Wegweiser (Wegweiser bleibt bis die Karte da ist); kein Zwischenscreen
nach dem Ankunftsbild: vom Bild mit den zwei Capybaras direkt zum Spielscreen (Martin 12:50), Ankunftsbild 2,5 s, Karte 0,8 s früher zu."""
import sys
src, dst = sys.argv[1], sys.argv[2]
s = open(src, encoding='utf-8').read()
def rep(a, b, cnt=1):
    global s
    n = s.count(a); assert n == cnt, (n, a[:70]); s = s.replace(a, b)

rep('const GAME_VER = "V315";', 'const GAME_VER = "V316";')
rep('let st = 0, prize = null, wasPaused = false;', 'let st = 0, prize = null, wasPaused = false, rescue = false;')
rep('function open(force) {\n      if (!ov.hidden) return; st = 0; prize = PR[Math.floor(Math.random() * PR.length)];',
    'function open(force, resc) {\n      if (!ov.hidden) return; st = 0; rescue = !!resc; prize = (rescue && PR.find(p => p[0] === "ton")) || PR[Math.floor(Math.random() * PR.length)];')
rep('$b("bdSub").textContent = "One spin on the house, squad!";',
    '$b("bdSub").textContent = rescue ? "Mayday! The stack is high – HQ sends heavy help!" : "One spin on the house, squad!";')
rep('if (S) { window.__offerLast = performance.now(); S.banditDone = true; S.banditNext = (S.wave || 1) + 5 + Math.floor(Math.random() * 3); wasPaused = !!S.intro; S.intro = true; S.banditOpen = true; }',
    'if (S) { window.__offerLast = performance.now(); if (rescue) S.rescueW = S.wave || 0; else { S.banditDone = true; S.banditNext = (S.wave || 1) + 5 + Math.floor(Math.random() * 3); } wasPaused = !!S.intro; S.intro = true; S.banditOpen = true; }')
rep('$b("bdResS").textContent = `+1 in your Pocket · now ×${S ? S[prize[2]] : 1}`; $b("bdGo").disabled = false; $b("bdGo").textContent = "COLLECT ▶";',
    '$b("bdResS").textContent = rescue ? "Drops right now – flattens your stack!" : `+1 in your Pocket · now ×${S ? S[prize[2]] : 1}`; $b("bdGo").disabled = false; $b("bdGo").textContent = rescue ? "DROP IT ▶" : "COLLECT ▶";')
rep('try { toast(`${prize[1].toUpperCase()} · in your Pocket`, "SUPPLY", 2200); } catch (e) {} }',
    'if (rescue) { rescue = false; setTimeout(() => { try { if (S && S.started && !S.over) startTon(); } catch (e) { console.error("rescueTon", e); } }, 260); return; }   /* V316: Rettung – sofort abwerfen */\n'
    '      try { toast(`${prize[1].toUpperCase()} · in your Pocket`, "SUPPLY", 2200); } catch (e) {} }')
rep("    window.__TT && (window.__TT.bandit = { open, spin, close });",
    "    /* V316: Rettungs-Lucky-Supply ab Welle 30, wenn der Stapel 5 Felder unter die Decke reicht */\n"
    "    setInterval(() => { try { if (!ov.hidden || !S || !S.started || S.over || S.nuts || S.won || (S.wave || 0) < 30 || S.ton) return;\n"
    "        if ((S.wave || 0) < (S.rescueW || -99) + 8) return; if (stackTopRow() > 5) return;\n"
    "        if (!window.__playScreen() || performance.now() - (window.__evtLast || -1e9) < 5000) return;\n"
    "        open(true, true); } catch (e) {} }, 400);\n"
    "    window.__TT && (window.__TT.bandit = { open, spin, close, rescue: () => open(true, true) });")
# «AA» Martin 12:44: Feier kam beim zweiten Mal nicht (window.__celFor blieb auf Welle 60) und soll 3 s nicht wegdrückbar sein
rep('function closeSign() { ovSign.hidden = true; if (S) { S.intro = false; S.signOpen = 0; } }',
    'function closeSign() { ovSign.hidden = true; window.__celFor = null; if (S) { S.intro = false; S.signOpen = 0; } }')
rep('#gameCel{position:fixed;inset:0;z-index:80;pointer-events:none}', '#gameCel{position:fixed;inset:0;z-index:80;pointer-events:auto}')
rep('const host = document.createElement("div"); host.id = "gameCel"; host.hidden = true; document.body.appendChild(host);',
    'const host = document.createElement("div"); host.id = "gameCel"; host.hidden = true; document.body.appendChild(host);\n'
    '  ["pointerdown", "pointerup", "click", "touchstart", "touchend"].forEach(t => host.addEventListener(t, e => { e.stopPropagation(); e.preventDefault(); }, { passive: false }));   /* V316: Feier 3 s nicht wegdrückbar */')
# Martin 12:47: nach dem Wegweiser blinkt kurz der Spielscreen (1 Frame) → Wegweiser bleibt sichtbar, bis die Karte da ist
rep('closeSign(); window.__fromSign = true; toast(`NUTS DETOUR · any time later from the pause menu`, "HQ", 2400); if (S && !S.inWave) S.waveCD = Math.min(S.waveCD || 0, 0.02); });',
    'window.__celFor = null; if (S) { S.intro = false; S.signOpen = 0; } window.__fromSign = true; toast(`NUTS DETOUR · any time later from the pause menu`, "HQ", 2400); if (S && !S.inWave) S.waveCD = Math.min(S.waveCD || 0, 0.02);\n'
    '  { const t0 = performance.now(), keep = () => { if (document.body.classList.contains("mapUp") || (S && S.mapShow) || performance.now() - t0 > 2500) { setTimeout(() => { ovSign.hidden = true; }, 120); return; } requestAnimationFrame(keep); }; requestAnimationFrame(keep); } });   /* V316: Wegweiser bis zur Karte stehen lassen */')
# Martin 12:48: nach «Welcome to Asia» noch ein Zwischenscreen (Karte 1,6 s) → Karte schließt, sobald das Ankunftsbild in den Punkt geschrumpft ist
rep('at(11000 - sk, () => { try { arrC && arrC.classList.remove("on"); } catch (e) {} });', '')
rep('at(12600 - sk, hide); }', 'at(11800 - sk, hide); }   /* V316: Ankunftsbild 2,5 s, dann direkt zum Spielscreen (Martin 12:50) */')
# Wild Cards: Dauer klar kommunizieren (Martin 12:45: «unklar, für wie lange die gelten»). Gilt bis zur nächsten Wahl = 20 Wellen
rep('<p>Pick one · it stays until the next wild cards.</p>', '<p id="ordDur">Pick one · it stays until the next wild cards.</p>')
rep('$("ordTitle").textContent = `PICK A WILD CARD · WAVE ${S.wave}`;',
    '$("ordTitle").textContent = `PICK A WILD CARD · WAVE ${S.wave}`; $("ordDur").innerHTML = `Pick one · <b>it lasts 20 waves – until wave ${S.wave + 20}</b><br>«Now» effects happen once, right away.`;')
rep('announce(o.name, `${o.plus} · ${o.minus}`, "ORDERS", 2200);', 'announce(o.name, `${o.plus} · ${o.minus}`, `WILD CARD · UNTIL WAVE ${(S.wave || 0) + 20}`, 2600);')
q = s.rindex('</body>'); s = s[:q] + '<style>\n.ordHead #ordDur{font-size:14px!important;line-height:1.35;color:#fff7e8!important;opacity:1!important}\n.ordHead #ordDur b{color:#ffd84d;font-weight:800}\n</style>\n' + s[q:]
open(dst, 'w', encoding='utf-8').write(s)
print("ok")
