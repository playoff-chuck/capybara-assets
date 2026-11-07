"""V401: Testlink ?test=wolfad (Martin, 07.11.): springt in Welle 99, zeigt die Wolf-Werbung, genug Gold zum Kaufen;
in Welle 100 kommt danach der Dieb. ?test=thief: Hinweis nennt jetzt den Wolf statt Sniper/Tesla.
Aufruf: python3 tools/patch401.py site/index.html site/index.html"""
import re, sys
src, dst = sys.argv[1], sys.argv[2]
s = open(src, encoding='utf-8').read()
def rep(a, b, cnt=1):
    global s
    n = s.count(a); assert n == cnt, (n, a[:70]); s = s.replace(a, b)
m = re.search(r'const GAME_VER = "V(\d+)";', s); old = int(m.group(1)); NEW = old + 1
rep(f'const GAME_VER = "V{old}";', f'const GAME_VER = "V{NEW}";')
rep('''      if (!calm() || !window.__offerOK()) return; S.wolfAdW = w; late = true; S.intro = true; S.adOpen = true; show("wolf", false); } catch (e) {} }, 900);''',
    '''      if (!calm() || !window.__offerOK()) return; S.wolfAdW = w; late = true; S.intro = true; S.adOpen = true; show("wolf", false); } catch (e) {} }, 900);
    window.__wolfAd = () => { if (!S || !S.started || S.over || !ov.hidden) return false; S.wolfAdW = S.wave; late = true; S.intro = true; S.adOpen = true; show("wolf", false); return true; };   /* V%d: Test */''' % NEW)
rep('''      else toast(`TEST · ${kind.toUpperCase()} starts a few seconds into wave ${w} · 2 Sniper + 2 Tesla in Pocket`, "HQ", 3000); }''',
    '''      else if (kind === "thief") toast(`TEST · THIEF comes a few seconds into wave ${w} · buy a WOLF CALL in the shop`, "HQ", 3000);
      else toast(`TEST · ${kind.toUpperCase()} starts a few seconds into wave ${w} · 2 Sniper + 2 Tesla in Pocket`, "HQ", 3000); }
    if (kind === "wolfad") { S.gold = Math.max(S.gold, 900); S.wolves = 0; let n = 0; const tick = () => { if (++n > 120) return; if (S.inWave && window.__wolfAd && window.__wolfAd()) return; setTimeout(tick, 500); }; setTimeout(tick, 1500);
      toast("TEST · Wolf ad comes in wave 99 · the thief follows in wave 100", "HQ", 3000); }''')
rep('''const map = { blk: 65, mag: 80, weed: 92, thief: 100, egg1: 2,''', '''const map = { blk: 65, mag: 80, weed: 92, thief: 100, wolfad: 99, egg1: 2,''')
open(dst, 'w', encoding='utf-8').write(s); print("ok V%d" % NEW)
