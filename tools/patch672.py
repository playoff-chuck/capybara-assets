# V672: Diplom-Fanfare ohne Knistern/Knacken: neue Datei (entklickt, keine Übersteuerung) + sanfteres Ausblenden
import sys
src, dst = sys.argv[1], sys.argv[2]
s = open(src, encoding="utf8").read()
def rep(a, b, n=1):
    global s; c = s.count(a); assert c == n, (a[:60], c); s = s.replace(a, b)
rep('new Audio("sfx/fanfare.mp3?v=623")', 'new Audio("sfx/fanfare.mp3?v=672")')
rep('fa.volume = Math.max(0, v0 * (1 - i / 16)); } catch (e) {} if (i >= 16) {', 'fa.volume = Math.max(0, v0 * Math.pow(1 - i / 40, 2)); } catch (e) {} if (i >= 40) {')
rep("if (i >= 40) { clearInterval(iv); try { fa.pause(); } catch (e) {} } }, 20); }, 4100);", "if (i >= 40) { clearInterval(iv); try { fa.pause(); } catch (e) {} } }, 10); }, 4000);   /* V672: weich ausblenden */")
rep('const GAME_VER = "V671"', 'const GAME_VER = "V672"')
open(dst, "w", encoding="utf8").write(s); print("ok")
