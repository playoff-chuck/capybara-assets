#!/usr/bin/env python3
# V669 (Martin 12.11. 15:57): Tutorial nach Unterbrechung fortsetzen.
# Ursache: Wechselt man die App, wird das Spiel auf dem Handy oft neu geladen und aus dem Spielstand fortgesetzt (loadGame).
# Dieser Weg startete das Tutorial nie – man war raus. Jetzt: aktuelle Lektion wird gemerkt («capy-tut-at»); wird ein
# Spielstand geladen und das Tutorial ist noch nicht abgeschlossen, geht es an der gemerkten Lektion weiter.
import sys, os
site = sys.argv[1]; p = os.path.join(site, "index.html"); s = open(p, encoding="utf-8").read()
def rep(a, b, n=1):
    global s
    c = s.count(a); assert c == n, (c, a[:90]); s = s.replace(a, b)
rep('const GAME_VER = "V668";', 'const GAME_VER = "V669";')
rep('function tutShow() { const st = TUT_STEPS[TUT.step];', 'function tutShow() { try { LS.set("capy-tut-at", String(TUT.step)); } catch (e) {} const st = TUT_STEPS[TUT.step];   /* V669: Lektion merken */')
rep('LS.set("tarnturm-tut", "1");', 'LS.set("tarnturm-tut", "1"); try { LS.del("capy-tut-at"); } catch (e) {}')
rep('const TUT = { on: false, step: 0, t: 0 };',
    '''const TUT = { on: false, step: 0, t: 0 };
setInterval(() => { try { const at = LS.get("capy-tut-at");   /* V669: Tutorial nach Neuladen/Fortsetzen weiterführen */
    if (at == null || TUT.on || LS.get("tarnturm-tut") === "1" || !S || !S.started || S.over || S.testRun || S.nuts || S.replay || S.paused) return;
    const st = document.getElementById("ovStart"); if (st && !st.hidden) return;
    tutStart(); const k = Math.max(0, Math.min(TUT_STEPS.length - 1, +at || 0)); if (k) { TUT.step = k; TUT.t = 0; tutShow(); } } catch (e) { console.error("tutResume", e); } }, 1000);''')
open(p, "w", encoding="utf-8").write(s); print("ok V669")
