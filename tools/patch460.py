#!/usr/bin/env python3
"""V460 – Spanisch (lang/es.json) + Sprachschicht robuster:
- Zahlen-Muster erkennt auch negative Zahlen; bereits übersetzte Texte (Rücklesen aus dem DOM) werden erkannt und nicht als «fehlend» gezählt.
- Reiterleisten (MEDALS · HALL OF FAME · SQUAD, Guide-Reiter) schrumpfen die Schrift bei langen Wörtern statt umzubrechen.
Nutzung: python3 tools/patch460.py src dst"""
import sys
src, dst = sys.argv[1], sys.argv[2]
s = open(src, encoding="utf-8").read()

def rep(a, b, n=1):
    global s
    c = s.count(a)
    assert c == n, (c, a[:80])
    s = s.replace(a, b)

rep('const GAME_VER = "V459";', 'const GAME_VER = "V460";')
rep('const I18N_NUM = /\\d[\\d.,:/]*\\d|\\d/g, I18N_WS = /\\s+/g;', 'const I18N_NUM = /[-−]?\\d[\\d.,:/]*\\d|[-−]?\\d/g, I18N_WS = /\\s+/g;')
rep('  let v = I18N.cache.get(key); if (v === undefined) { v = i18nLookup(key); if (v == null) { I18N.miss.add(key); v = null; } I18N.cache.set(key, v); }',
    '  let v = I18N.cache.get(key); if (v === undefined) { v = i18nLookup(key); if (v == null) { if (!(I18N.rev && (I18N.rev.has(key) || I18N.rev.has(key.replace(I18N_NUM, "#"))))) I18N.miss.add(key); v = null; } I18N.cache.set(key, v); }   /* V460: Rückübersetztes nicht als fehlend zählen */')
rep("I18N.dict = d || {}; I18N.names = Object.keys(I18N.dict)",
    "I18N.dict = d || {}; I18N.rev = new Set(Object.values(I18N.dict)); I18N.names = Object.keys(I18N.dict)")
# Reiter: Schrift passt sich an
rep('#awBar button{flex:1;min-width:0;padding:9px 2px 7px;border-radius:12px;border:3px solid #3a2a1a;background:#fff6e6;color:#3a2a1a;font:400 17px/1 Bangers,system-ui!important;',
    '#awBar button{flex:1;min-width:0;padding:9px 2px 7px;border-radius:12px;border:3px solid #3a2a1a;background:#fff6e6;color:#3a2a1a;font:400 clamp(12px,4.1vw,17px)/1 Bangers,system-ui!important;white-space:nowrap;overflow:hidden;text-overflow:ellipsis;')
rep('#ovDaily .dlRow button{min-height:36px;padding:4px 12px;font-size:14px;border-radius:999px}',
    '#ovDaily .dlRow button{min-height:36px;padding:4px 10px;font-size:13px;border-radius:999px;white-space:nowrap}#ovDaily .dlChain i small{font-size:8px}')

# Weltall hinter der Karte, nur angedeutet (Martin 16:19): dunkles Blau, wenige Sterne, zarter Nebel
rep('#ovMap{background:#7fb9b6!important}',
    '#ovMap{background:#0b1230 radial-gradient(ellipse 70% 40% at 50% 0%,rgba(90,110,190,.28),transparent 70%),radial-gradient(ellipse 60% 35% at 50% 100%,rgba(120,80,160,.22),transparent 70%),'
    'radial-gradient(1.2px 1.2px at 12% 18%,rgba(255,255,255,.9),transparent 60%),radial-gradient(1px 1px at 28% 9%,rgba(255,255,255,.7),transparent 60%),radial-gradient(1.4px 1.4px at 41% 23%,rgba(255,255,255,.85),transparent 60%),radial-gradient(1px 1px at 63% 14%,rgba(255,255,255,.6),transparent 60%),radial-gradient(1.3px 1.3px at 78% 20%,rgba(255,255,255,.8),transparent 60%),radial-gradient(1px 1px at 90% 7%,rgba(255,255,255,.7),transparent 60%),'
    'radial-gradient(1.2px 1.2px at 8% 84%,rgba(255,255,255,.8),transparent 60%),radial-gradient(1px 1px at 22% 93%,rgba(255,255,255,.6),transparent 60%),radial-gradient(1.4px 1.4px at 47% 88%,rgba(255,255,255,.85),transparent 60%),radial-gradient(1px 1px at 69% 95%,rgba(255,255,255,.7),transparent 60%),radial-gradient(1.2px 1.2px at 84% 86%,rgba(255,255,255,.8),transparent 60%),radial-gradient(1px 1px at 95% 78%,rgba(255,255,255,.6),transparent 60%)!important}')

# Zahnrad-Fenster: größer, nicht scrollbar – passt sich dem Bildschirm an (Martin 16:19)
rep('#ovSettings{z-index:65;overflow-y:auto!important;justify-content:flex-start!important;padding-top:calc(env(safe-area-inset-top,0px) + 56px)!important;padding-bottom:24px!important}',
    '#ovSettings{z-index:65;overflow:hidden!important;justify-content:center!important;padding:calc(env(safe-area-inset-top,0px) + 10px) 10px calc(env(safe-area-inset-bottom,0px) + 10px)!important}')
rep('#ovSettings .joinBox{width:min(380px,100%)!important;max-height:none!important;overflow:visible!important;flex:0 0 auto}#ovSettings .hpAv{width:84px!important;height:98px!important}',
    '#ovSettings .joinBox{width:min(400px,100%)!important;max-height:none!important;overflow:visible!important;flex:0 0 auto;transform-origin:50% 50%;gap:9px!important;padding:14px 16px 16px!important}#ovSettings .hpAv{width:96px!important;height:112px!important}#ovSettings .setRow button{min-height:48px}')
rep('try { i18nSetRow(); } catch (e) {}   /* V457: Flaggen im Zahnrad-Menü */',
    '''try { i18nSetRow(); } catch (e) {}   /* V457: Flaggen im Zahnrad-Menü */
(function () { const ov = document.getElementById("ovSettings"), box = ov && ov.querySelector(".joinBox"); if (!box) return;   /* V460: Fenster so groß wie möglich, nie scrollen */
  const fit = () => { box.style.transform = ""; const avail = innerHeight - 20, h = box.getBoundingClientRect().height; const r = box.getBoundingClientRect(), k = Math.min(1, (innerWidth - 20) / Math.max(1, r.width), Math.max(0.6, avail / Math.max(1, h))); box.style.transform = `scale(${k.toFixed(3)})`; };
  new MutationObserver(() => { if (!ov.hidden) requestAnimationFrame(fit); }).observe(ov, { attributes: true, attributeFilter: ["hidden"] }); addEventListener("resize", () => { if (!ov.hidden) fit(); }); })();''')

open(dst, "w", encoding="utf-8").write(s)
print("ok", dst)
