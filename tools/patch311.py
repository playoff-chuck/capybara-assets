"""V311: Angebote kommen öfter durch (Martin 06.11. 09:55/09:56).
Testlauf W1–W60 zeigte: Lucky Supply (nach W2 erst W37) und Rufzeichen-Abfrage (W16/W44 statt ab W7) kamen kaum
durch, weil Boss-Hack und Sale-Anzeigen den 2-min-Takt belegten.
1. Angebots-Takt 95 s statt 120 s («statt 2 Minuten Takt 1 min 35 Sekunden»). 30 s Abstand nach Fenstern bleibt.
2. Vorrang: Ist Lucky Supply oder die Rufzeichen-Abfrage fällig, warten Sale-Anzeigen («Lucky Supply und Rufzeichen
   haben Vorrang vor Sale-Anzeigen. Ok»). Sicherung: höchstens bis Ende der nächsten Welle, dann darf die Sale-Anzeige
   trotzdem (falls Lucky/Rufzeichen aus anderem Grund nicht kommen können). Späte Waffen-Anzeigen sind laut Martin ok."""
import sys
src, dst = sys.argv[1], sys.argv[2]
s = open(src, encoding='utf-8').read()
def rep(a, b, cnt=1):
    global s
    n = s.count(a); assert n == cnt, (n, a[:70]); s = s.replace(a, b)

rep('const GAME_VER = "V310";', 'const GAME_VER = "V311";')
rep('performance.now() - (window.__offerLast || -1e9) >= 120000);',
    'performance.now() - (window.__offerLast || -1e9) >= 95000);   /* V311: Takt 95 s */')
rep('function joined() { return LS.get("tarnturm-join") === "1"; }',
    'function joined() { return LS.get("tarnturm-join") === "1"; }\n'
    '/* V311: Lucky Supply oder Rufzeichen fällig → Sale-Anzeigen warten */\n'
    'window.__prioDue = () => { try { if (!S || !S.started || S.over || S.nuts || S.testRun) return false;\n'
    '  const lucky = (S.banditNext ? (S.wave || 0) >= S.banditNext : !S.banditDone) && (S.playT || 0) >= 60;\n'
    '  const join = !joined() && (S.wave || 0) >= 7; return lucky || join; } catch (e) { return false; } };')
rep('setInterval(() => { try { if (!S || !S.adDue || !calm() || !window.__offerOK()) return; for (const k of ["kan",',
    'setInterval(() => { try { if (!S || !S.adDue || !calm() || !window.__offerOK()) return;\n'
    '      if (window.__prioDue && window.__prioDue()) { if (S.prioW == null) S.prioW = S.wave || 0; if ((S.wave || 0) <= S.prioW + 1) return; } else S.prioW = null;   /* V311: Vorrang Lucky/Rufzeichen */\n'
    '      for (const k of ["kan",')
open(dst, 'w', encoding='utf-8').write(s)
print("ok")
