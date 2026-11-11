#!/usr/bin/env python3
# V623 (Martin 11.11. 13:14): Diplom-Fanfare aus Suno («Brass Fanfare», Ausschnitt A: 0–5 s, schnelles Ausblenden 0,6 s) statt synthetischem Tusch.
# Vorher: /root/fanfare/fanfare.mp3 nach site/sfx/fanfare.mp3.
import sys, os, shutil
site = sys.argv[1]; p = os.path.join(site, "index.html"); s = open(p, encoding="utf-8").read()
dst = os.path.join(site, "sfx", "fanfare.mp3")
if not os.path.exists(dst): shutil.copy("/root/fanfare/fanfare.mp3", dst)
def rep(a, b, n=1):
    global s
    c = s.count(a); assert c == n, (c, a[:90]); s = s.replace(a, b)
rep('const GAME_VER = "V622";', 'const GAME_VER = "V623";')
rep('function certTusch() {   /* V605: festlicher Tusch zum Diplom */\n  if (SFX.muted || SFX.vol === 0) return;',
    'function certTusch() {   /* V605: festlicher Tusch zum Diplom · V623: Suno-Fanfare */\n  if (SFX.muted || SFX.vol === 0) return;\n'
    '  try { const fa = new Audio("sfx/fanfare.mp3?v=623"); fa.volume = Math.min(1, 0.95 * Math.pow(SFX.vol || 0.3, 0.5)); const pr = fa.play(); if (pr && pr.catch) pr.catch(() => {}); return; } catch (e) {}')
rep('SFX.say("cert_done", 1, 1, "cert_done"); } catch (e) {} }, 1200);', 'SFX.say("cert_done", 1, 1, "cert_done"); } catch (e) {} }, 4400);   /* V623: Spruch nach der Fanfare */')
open(p, "w", encoding="utf-8").write(s)
print("ok V623")
