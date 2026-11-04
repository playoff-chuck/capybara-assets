"""V229: Weltkarten-Intro (Flugzeug nach South America) kommt sofort nach PLAY bei jeder neuen Welttour – vor dem
Spielfeld, nicht erst beim Start der ersten Welle. Wellenstart, der währenddessen kommt, wird danach nachgeholt."""
import sys
src, dst = sys.argv[1], sys.argv[2]
s = open(src, encoding='utf-8').read()
def rep(a, b, cnt=1):
    global s
    n = s.count(a); assert n == cnt, (n, a[:70]); s = s.replace(a, b)
rep('const GAME_VER = "V228";', 'const GAME_VER = "V229";')
rep('let busy = false;', 'let busy = false, pendSW = null;')
rep('if (nw === 1 && !LS.get("tarnturm-mapintro")) { play = playIntro; LS.set("tarnturm-mapintro", "1"); }\n          else if (nw > 1', 'if (nw > 1')
rep('if (busy) return; return _sw2.apply(this, a); };', '''if (busy) { pendSW = [this, a]; return; } return _sw2.apply(this, a); };
    const _sg = startGame; startGame = function (m, fromWave) { const r = _sg.apply(this, arguments);
      try { if (!fromWave && S && S.started && !S.over && !S.nuts) { busy = true; const was = S.paused; S.paused = true; S.mapShow = true;
          playIntro(() => { S.paused = was; S.mapShow = false; busy = false; if (pendSW) { const [t, aa] = pendSW; pendSW = null; _sw2.apply(t, aa); } });
          setTimeout(() => { try { if (S.wave > 0 || S.nuts) hide(); } catch (e) {} }, 0); } } catch (e) { busy = false; }
      return r; };''')
rep('function playIntro(done) { seqDone = done; show("auto"); drawPins(0);', 'function playIntro(done) { seqDone = done; show("auto"); drawPins(-1);')
rep('at(3700, () => { setMe(MAP_PTS[0][0], true);', 'at(3700, () => { drawPins(0); setMe(MAP_PTS[0][0], true);')
open(dst, 'w', encoding='utf-8').write(s); print('ok')
