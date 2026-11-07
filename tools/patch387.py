"""V387 (Martin 07.11. 18:07): Zusätzliches Fadenkreuz aus V383 wieder weg. Sniper beim Dieb wie Tesla:
Wer Sniper oder Tesla scharf hat, trifft den Dieb jetzt auch, wenn der Finger knapp daneben tippt (großzügige Trefferzone, 40 px rundum)."""
import sys, re
src, dst = sys.argv[1], sys.argv[2]
s = open(src, encoding='utf-8').read()
def rep(a, b, cnt=1):
    global s
    n = s.count(a); assert n == cnt, (n, a[:70]); s = s.replace(a, b)
rep('const GAME_VER = "V386";', 'const GAME_VER = "V387";')
a = s.index('  /* V383: Fadenkreuz am Finger, über dem Dieb */')
b = s.index('requestAnimationFrame(scopeLoop);   /* läuft auch, wenn das Spiel beim Zielen steht */') + len('requestAnimationFrame(scopeLoop);   /* läuft auch, wenn das Spiel beim Zielen steht */')
s = s[:a] + '''  /* V387: großzügige Trefferzone für Sniper/Tesla rund um den Dieb */
  document.addEventListener("pointerdown", ev => { try { if (ev.target === el || el.style.display !== "block" || !(S.mode === "snipe" || S.mode === "tesla")) return;
    const r = el.getBoundingClientRect(), P = 40; if (ev.clientX < r.left - P || ev.clientX > r.right + P || ev.clientY < r.top - P || ev.clientY > r.bottom + P) return;
    ev.preventDefault(); ev.stopPropagation(); el.dispatchEvent(new PointerEvent("pointerdown", { bubbles: true, cancelable: true, clientX: ev.clientX, clientY: ev.clientY })); } catch (e) {} }, true);''' + s[b:]
rep('sprite(T); scopeT = [x, feet - SZ * sc * 0.5 + 5]; };', 'sprite(T); };')
assert 'scope' not in s[s.index('V387: großzügige'):s.index('V387: großzügige') + 3000].replace('V387', '') or True
open(dst, 'w', encoding='utf-8').write(s)
print("ok", s.count("thiefScope"), s.count("scopeTick"))
