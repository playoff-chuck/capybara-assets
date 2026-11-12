# V688 (Martin 12.11. 20:11: «Die Musik geht einfach weiter»): Beim Ortswechsel holte der Musik-Wächter (V365, alle 0,5 s)
# die ausgeblendete Level-Musik nach ~2 s wieder auf Standardpegel – in der langen Streifen-Pause lief sie deshalb weiter.
# Jetzt: 1,5 s ausblenden, dann anhalten und für die Dauer des Übergangs sperren (window.__tpHush); am Ende 2 s wieder einblenden.
import sys
src, dst = sys.argv[1], sys.argv[2]
s = open(src, encoding="utf8").read()
def rep(a, b, n=1):
    global s; c = s.count(a); assert c == n, (a[:70], c); s = s.replace(a, b)
rep('''      try { if (typeof TP !== "undefined" && TP.el && TP.key && !TP.el.paused) tpFade(0.0001, 1.5); else if (SFX.music && SFX.music.dim) SFX.music.dim(0.02); } catch (e) {}   /* 0–1,5 s Musik klingt aus */
      let end = null, gone = false, tap = null;''',
'''      let hadTP = false, musBack = false; clearTimeout(window.__celHushT);
      const lvlBack = () => { if (musBack) return; musBack = true; clearTimeout(window.__celHushT); window.__tpHush = false;   /* V688: Level-Musik 2 s wieder ein */
        try { if (hadTP && TP.el && TP.key && !TP.paused && SFX.music.on && !document.hidden && TP.el.paused) { TP.el.volume = 0; const p = TP.el.play(); if (p && p.catch) p.catch(() => {}); tpFade(0.5, 2.0); } } catch (e) {} };
      try { if (typeof TP !== "undefined" && TP.el && TP.key && !TP.el.paused) { hadTP = true; window.__tpHush = true; tpFade(0.0001, 1.5); setTimeout(() => { try { if (window.__tpHush && !musBack) TP.el.pause(); } catch (e) {} }, 1560); window.__celHushT = setTimeout(lvlBack, 60000); }
            else if (SFX.music && SFX.music.dim) SFX.music.dim(0.02); } catch (e) {}   /* 0–1,5 s Musik klingt aus, bleibt bis zum Ende des Übergangs aus */
      let end = null, gone = false, tap = null;''')
rep('blk.classList.remove("on"); hide(); }); };   /* Level blendet wieder ein */', 'blk.classList.remove("on"); hide(); setTimeout(lvlBack, 400); }); };   /* Level blendet wieder ein, Musik kommt zurück */')
# Chor: das Vorladen 15 s nach dem Start rief load() auch auf, wenn der Chor schon lief (Test-Link: Streifen nach ~9 s) → Chor brach ab.
rep('try { setTimeout(() => { try { mk().load(); } catch (e) {} }, 15000); } catch (e) {}', 'try { setTimeout(() => { try { if (!a) mk().load(); } catch (e) {} }, 15000); } catch (e) {}   /* V688: nie neu laden, wenn er schon existiert */')
rep('const GAME_VER = "V687"', 'const GAME_VER = "V688"')
open(dst, "w", encoding="utf8").write(s); print("ok", len(s))
