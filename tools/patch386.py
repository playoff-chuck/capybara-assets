"""V386: Meldung + Fenster nie gleichzeitig (To-do 10, Meldungs-Analyse).
Befund (Läufe W1–30): ~16 Überschneidungen je Lauf, fast alle so: Funk-Meldung/Toast startet, 0–2 s später geht ein
Fenster auf (Air Drop, Sale, NEW MONSTER, Boss-Hack, Karte, Wild Cards, Wegweiser) – die Meldung blieb sichtbar.
Regel 4 (Regelwerk): immer nur ein Ding; Funk wartet bei offenen Fenstern.
Neu: Wächter (150 ms). Geht ein Fenster auf, während eine Meldung steht → Meldung sofort weg; Funk-Meldungen und
wichtige Toasts (KEEP_TAGS, Medaillen, Sterne, Checkpoint) kommen nach dem Fenster mit der Restzeit (min. 1,6 s) wieder.
Unwichtige Toasts (Tageszeit) fallen weg.
Aufruf: python3 tools/patch386.py site/index.html site/index.html"""
import re, sys
src, dst = sys.argv[1], sys.argv[2]
s = open(src, encoding='utf-8').read()
def rep(a, b, cnt=1):
    global s
    n = s.count(a); assert n == cnt, (n, a[:70]); s = s.replace(a, b)
m = re.search(r'const GAME_VER = "V(\d+)";', s); old = int(m.group(1)); NEW = old + 1
rep(f'const GAME_VER = "V{old}";', f'const GAME_VER = "V{NEW}";')

rep('''  if (m.kind === "book") bookShow(m.score, m.mark); else if (m.kind === "alert") showAlert(''',
    '''  window.__msgCur = { m, until: performance.now() + m.hold };   /* V%d */
  if (m.kind === "book") bookShow(m.score, m.mark); else if (m.kind === "alert") showAlert(''' % NEW)

rep('''function garble(t) { return String(t || "")''',
'''/* V%d: Fenster geht auf, während eine Meldung steht → Meldung sofort weg; wichtige kommen nach dem Fenster wieder */
setInterval(() => { try {
  const c = window.__msgCur; if (!c || !S) return; const now = performance.now();
  if (now >= c.until) { window.__msgCur = null; return; }
  if (!uiWinOpen()) return;
  window.__msgCur = null; const m = c.m, rest = c.until - now;
  if (m.kind === "alert") { const el = $("alert"); clearTimeout(alertT); ++alertSeq; el.classList.remove("go", "out"); el.hidden = true; S.alert = false; }
  else if (m.kind === "toast") hideToastNow(); else return;
  window.__msgCut = (window.__msgCut || 0) + 1;
  if (!m._re && rest > 700 && (m.kind === "alert" || KEEP_TAGS.has(m.tag) || /MEDAL|STARS|CHECKPOINT/.test(m.title))) MSGQ.unshift(Object.assign({}, m, { hold: Math.max(1600, Math.round(rest)), at: now, _re: 1 }));
  msgBusy = 0; clearTimeout(window.__msgWT); window.__msgWT = setTimeout(msgTick, 500);
} catch (e) {} }, 150);
function garble(t) { return String(t || "")''' % NEW)

open(dst, 'w', encoding='utf-8').write(s)
print("ok V%d" % NEW)
