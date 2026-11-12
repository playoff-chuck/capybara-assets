#!/usr/bin/env python3
# V661 (Martin 12.11. 13:50): Umfrage «How do you like the game?» hält das Spiel an (nichts läuft hinten weiter).
# Musik blendet 1,5 s vorher aus, dann kommt das Fenster; nach der Antwort blendet die Musik wieder ein (1,5 s) und das Spiel läuft weiter.
import sys, os
site = sys.argv[1]; p = os.path.join(site, "index.html"); s = open(p, encoding="utf-8").read()
def rep(a, b, n=1):
    global s
    c = s.count(a); assert c == n, (c, a[:90]); s = s.replace(a, b)
rep('const GAME_VER = "V660";', 'const GAME_VER = "V661";')
# Merker «offen» + Halten/Musik
rep('let pT = 0, pAt = 0;',
    '''let pT = 0, pAt = 0, pOpen = false;
    const pMusicOut = sec => { try { if (typeof TP !== "undefined" && TP.el && !TP.el.paused) tpFade(0.0001, sec); } catch (e) {} };
    const pMusicIn = () => { try { if (typeof TP !== "undefined" && TP.el && TP.key && !TP.paused) tpFade(0.5, 1.5); } catch (e) {} };
    const pHold = () => { try { if (S && S.started && !S.over) S.coachHold = true; } catch (e) {} };   /* V661: Spiel steht */''')
rep('''pAt = at; try { LS.set("capy-poll-" + at, "s"); } catch (e) {}   /* V659: "s" = gezeigt, offen */''',
    '''pAt = at; try { LS.set("capy-poll-" + at, "s"); } catch (e) {}   /* V659: "s" = gezeigt, offen */
      pOpen = true; pHold(); pMusicOut(0.3);   /* V661 */''')
rep('''if (!b) return; const v = +b.dataset.v; ev("poll", { v, at: pAt }); try { LS.set("capy-poll-" + pAt, "1"); } catch (er) {}''',
    '''if (!b) return; if (!pOpen) return; const v = +b.dataset.v; ev("poll", { v, at: pAt }); try { LS.set("capy-poll-" + pAt, "1"); } catch (er) {}
      pOpen = false; try { if (S) { S.coachHold = false; window.__evLast = performance.now(); } } catch (er) {} pMusicIn();   /* V661: weiter + Musik ein */''')
rep('''setTimeout(() => pollShow(at), 1500); }   /* V659: sofort, über allem */''',
    '''pHold(); pMusicOut(1.5); setTimeout(() => pollShow(at), 1500); }   /* V659/V661: Musik 1,5 s aus, dann Fenster */''')
rep('''else if (document.body.lastElementChild !== pc) document.body.appendChild(pc); } catch (e) {} }, 700);''',
    '''else if (document.body.lastElementChild !== pc) document.body.appendChild(pc); } catch (e) {} }, 700);
    setInterval(() => { if (!pOpen || pc.hidden) return; pHold();   /* V661: solange offen bleibt das Spiel stehen und die Musik aus */
      try { if (typeof TP !== "undefined" && TP.el && !TP.el.paused && TP.el.volume > 0.004 && (TP.want == null || TP.want >= 0.5)) tpFade(0.0001, 0.3); } catch (e) {} }, 150);''')
open(p, "w", encoding="utf-8").write(s); print("ok V661")
