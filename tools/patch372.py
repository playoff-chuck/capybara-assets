"""V372 (Martin 07.11. 09:50): «Vibrationen von Anfang an zu viel, schon bei App-Start. Nur gelegentlich nutzen.»
- Nie im Menü/beim Start und nicht in den ersten 60 s Spielzeit.
- Nur noch seltene, wichtige Momente: 3+ Reihen auf einmal, Leben verloren, Boss-Signal, Lucky-Supply-Jackpot, Seitenwechsel (Sidewinder), Game over.
- Keine Vibration mehr für 1–2 Reihen, Shop-Kauf, Air Drop.
- Höchstens eine Vibration je 20 s (Game over ausgenommen); alles läuft über denselben Begrenzer und den Schalter im Pausemenü."""
import sys
src, dst = sys.argv[1], sys.argv[2]
s = open(src, encoding='utf-8').read()
def rep(a, b, cnt=1):
    global s
    n = s.count(a); assert n == cnt, (n, a[:70]); s = s.replace(a, b)
rep('const GAME_VER = "V371";', 'const GAME_VER = "V372";')
rep('''      function buzz(pat, strong) { if (!can || !on || document.hidden) return; const now = performance.now(); if (now - lastAny < 300) return;
        while (hist.length && now - hist[0] > 60000) hist.shift();
        if (!strong && (hist.length >= 7 || now - lastLight < 4000)) return;''',
'''      function buzz(pat, strong, must) { if (!can || !on || document.hidden) return; const now = performance.now();
        if (!must && (typeof S === "undefined" || !S || !S.started || S.over || (S.playT || 0) < 60 || now - lastAny < 20000)) return;   /* V372: nur gelegentlich, nie beim Start */
        while (hist.length && now - hist[0] > 60000) hist.shift();''')
rep('if (on) buzz([25], true); });', 'if (on) buzz([25], true, true); });')
rep('if (pl != null && S.lines > pl && !S.over) { const d = S.lines - pl; buzz(d >= 3 ? [60, 50, 60] : [d === 2 ? 55 : 40], false);   /* V321: spürbar */ }',
    'if (pl != null && S.lines - pl >= 3 && !S.over) buzz([60, 50, 60], true);   /* V372: nur große Reihen */')
rep('if (S.over && !pOver) buzz([60, 80, 60], true);', 'if (S.over && !pOver) buzz([60, 80, 60], true, true);')
rep('try { window.__vib && window.__vib([20], true); } catch (e) {} close(true);', 'close(true);')
rep('try { window.__vib && window.__vib([20, 40, 20], true); } catch (e) {} }', '}')
rep('try { if (navigator.vibrate) navigator.vibrate([30, 60, 30]); } catch (e) {}', 'try { window.__vib && window.__vib([30, 60, 30], true); } catch (e) {}')
rep('snd("siren"); try { if (navigator.vibrate) navigator.vibrate(50); } catch (e) {}', 'snd("siren"); try { window.__vib && window.__vib([50], true); } catch (e) {}')
rep('const hist = []; let lastAny = 0, lastLight = 0;', 'const hist = []; let lastAny = -1e9, lastLight = -1e9;')
open(dst, 'w', encoding='utf-8').write(s)
print("ok")
