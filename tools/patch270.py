"""V270 (Martin 05.11. 15:26): Synchronisation aller Anzeige-Elemente.
- FEHLER behoben: seit V251 wurde beim Wellenstart der Rest der Zeile ignoriert (hinter einem Kommentar) – Welle lief nicht
  richtig an (inWave, Spawn-Zähler, Nuts-Anzahl). Jetzt wieder korrekt.
- Oben links spricht immer nur eine Figur: der Punkte-Bericht von Major Ledger läuft jetzt durch dieselbe Warteschlange wie
  General, Doc Hazel und alle Funkmeldungen (vorher überdeckte er die Sprechblase des Generals).
- Solange ein Fenster offen ist (Neuheit, Anzeige, Lucky Supply, Weltkarte, Rufzeichen, Ortsschild), warten Sprechblasen und
  Lob-Wörter (Splash, Kaboom …) und kommen danach.
- Vorrang: wichtige Meldungen (Alarm, Sonderwelle, Kontinent, Medaille, Neuheiten, Befehle …) laufen vor Lob/Statistik des
  Generals am Wellenende; Lob/Statistik älter als 8 s fällt weg.
- Lob-Wörter im Feld nicht, während oben eine Sprechblase erscheint (≤ 0,4 s davor), und nie zwei gleichzeitig (wie bisher)."""
import sys
src, dst = sys.argv[1], sys.argv[2]
s = open(src, encoding='utf-8').read()
def rep(a, b, cnt=1):
    global s
    n = s.count(a); assert n == cnt, (n, a[:70]); s = s.replace(a, b)
rep('const GAME_VER = "V269";', 'const GAME_VER = "V270";')
# Fenster-offen-Prüfung
rep('function msgPush(m) {', '''function uiWinOpen() { try { const v = id => { const e = document.getElementById(id); return e && !e.hidden && getComputedStyle(e).display !== "none"; };
  return v("ovIntro") || document.body.classList.contains("introWin") || v("ovAd") || v("ovBandit") || v("ovJoin") || document.body.classList.contains("mapUp") || !!(S && (S.joinOpen || S.signOpen || S.banditOpen)); } catch (e) { return false; } }
window.__msgDbg = () => ({ q: MSGQ.map(x => x.title), busy: Math.round(msgBusy - performance.now()), win: uiWinOpen() });
function msgPush(m) {''')
# Vorrang: normale Meldungen vor Lob/Statistik einreihen
rep('  m.at = performance.now(); MSGQ.push(m);', '  m.at = performance.now(); if (!m.low) { const i = MSGQ.findIndex(x => x.low); if (i >= 0) MSGQ.splice(i, 0, m); else MSGQ.push(m); } else MSGQ.push(m);')
rep('  if (msgBusy > performance.now() || !MSGQ.length) return;', '  if (msgBusy > performance.now() || !MSGQ.length) return;\n  if (uiWinOpen()) { clearTimeout(window.__msgWT); window.__msgWT = setTimeout(msgTick, 500); return; }   // V270: Fenster offen → warten')
rep('  if (m.kind === "toast" && age > 6000 && !KEEP_TAGS.has(m.tag)) { msgTick(); return; }   // veraltet',
    '  if (m.kind === "toast" && age > 6000 && !KEEP_TAGS.has(m.tag)) { msgTick(); return; }   // veraltet\n  if (m.low && (age > 8000 || (S && S.radioOut))) { msgTick(); return; }   // V270: Lob/Statistik veraltet\n  window.__msgShowT = performance.now();')
rep('  if (m.kind === "alert") showAlert(m.title, m.sub, m.tag, m.hold); else showToast(m.title, m.sub, m.tag, m.hold);',
    '  if (m.kind === "book") bookShow(m.score, m.mark); else if (m.kind === "alert") showAlert(m.title, m.sub, m.tag, m.hold); else showToast(m.title, m.sub, m.tag, m.hold);')
# Buchhalter in die Schlange
rep('function bookkeeper(score, mark) {\n  const el = $("book");', 'function bookkeeper(score, mark) { msgPush({ kind: "book", title: "book" + mark, sub: "", tag: "GOLD", hold: 3600, score, mark }); }\nfunction bookShow(score, mark) {\n  const el = $("book");')
# Wellenende-Lob als niedrige Priorität
rep('announce(say.toUpperCase(), sub, "HQ", 3200);', 'msgPush({ kind: "alert", title: say.toUpperCase(), sub, tag: "HQ", hold: 3200, low: true });')
# Lob-Wörter: nicht bei offenem Fenster, nicht direkt mit neuer Sprechblase
rep('  if (now - lastPraise < 1500 || SFX.voiceBusy) return;', '  if (now - lastPraise < 1500 || SFX.voiceBusy) return;\n  if (uiWinOpen() || now - (window.__msgShowT || -1e9) < 400) return;   // V270')
# DRINGEND: seit V251 stand der Rest der Wellenstart-Zeile hinter einem Kommentar (inWave/Spawn-Zähler/Nuts-Anzahl wurden nicht gesetzt)
rep("S.waveTotal = S.toSpawn;   // V251: Afrika −25 % Monster if (S.nuts) { S.toSpawn = S.waveTotal = nutsCount(S.nuts.lvl); } S.spawnT = 0; S.spawnIdx = 0; S.inWave = true; S.waveLeaks = 0;",
    "S.waveTotal = S.toSpawn; if (S.nuts) { S.toSpawn = S.waveTotal = nutsCount(S.nuts.lvl); } S.spawnT = 0; S.spawnIdx = 0; S.inWave = true; S.waveLeaks = 0;   // V251/V268: weniger Monster ab W21 (Kommentar ans Zeilenende, V270)")
open(dst, 'w', encoding='utf-8').write(s); print('ok')
