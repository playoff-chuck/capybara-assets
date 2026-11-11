#!/usr/bin/env python3
# V622 (Martin 11.11. 13:12): Coach-Tipps nicht mehr als Einblendung beim Öffnen des Hacks, sondern beim Drücken auf Start
# (Duell starten, auch Probelauf) – die ersten 2 Male, dann erst das Duell. Bild höher (Gesicht + Hals sichtbar), Tipps kleiner.
import sys, os
site = sys.argv[1]; p = os.path.join(site, "index.html"); s = open(p, encoding="utf-8").read()
def rep(a, b, n=1):
    global s
    c = s.count(a); assert c == n, (c, a[:90]); s = s.replace(a, b)
rep('const GAME_VER = "V621";', 'const GAME_VER = "V622";')
# Auslöser: startDuel statt openHack, 2 Mal
rep('''  const need = () => { try { const th = !!(S && S.testRun && S.testKind === "hack"); return (LS.get("capy-hk-tips") !== "1" || th) && S && S.started && !S.over && !S.nuts && (!S.testRun || th) && !S.replay; } catch (e) { return false; } };''',
    '''  const cnt = () => { try { return LS.get("capy-hk-tips") === "1" ? 1 : (+LS.get("capy-hk-tipsN") || 0); } catch (e) { return 9; } };   /* V622: die ersten 2 Duelle */
  const need = () => { try { const th = !!(S && S.testRun && S.testKind === "hack"); return (cnt() < 2 || th) && HK.phase === "bet" && S && S.started && !S.over && !S.nuts && (!S.testRun || th) && !S.replay; } catch (e) { return false; } };''')
rep('try { LS.set("capy-hk-tips", "1"); } catch (x) {}', 'try { LS.set("capy-hk-tipsN", String(cnt() + 1)); LS.set("capy-hk-tips", "0"); } catch (x) {}')
rep('''  const _oh = openHack; openHack = function (force) { if (!need() || (!force && !hkOfferOn())) return _oh.apply(this, arguments); show(() => _oh(true)); };''',
    '''  const _sd = startDuel; startDuel = function (keep) { if (!need()) return _sd.apply(this, arguments); const a = arguments; show(() => _sd.apply(this, a)); };   /* V622: beim Start des Duells */''')
# Layout: Bild höher, Tipps kleiner
rep('background:#14240f url("img/hk_tips.webp?v=619") center top/cover no-repeat}', 'background:#0d1f0b url("img/hk_tips.webp?v=619") center -7vh/max(100%,56vh) auto no-repeat}')
rep('#ovHkTips::before{content:"";position:absolute;inset:0;background:linear-gradient(180deg,rgba(10,16,6,.78) 0,rgba(10,16,6,.15) 22%,rgba(10,16,6,0) 38%,rgba(10,20,8,.55) 55%,rgba(8,18,8,.9) 100%);pointer-events:none}',
    '#ovHkTips::before{content:"";position:absolute;inset:0;background:linear-gradient(180deg,rgba(10,16,6,.75) 0,rgba(10,16,6,.1) 18%,rgba(10,16,6,0) 50%,rgba(10,20,8,.5) 62%,rgba(8,18,8,.92) 78%);pointer-events:none}')
rep('#ovHkTips ol{list-style:none;margin:0 0 10px;padding:0;display:grid;gap:7px}', '#ovHkTips ol{list-style:none;margin:0 0 8px;padding:0;display:grid;gap:5px}')
rep('#ovHkTips li{display:flex;gap:10px;align-items:center;background:#fff6dc;border:3px solid #3a2414;border-radius:16px;padding:8px 10px;box-shadow:0 3px 0 #3a2414}',
    '#ovHkTips li{display:flex;gap:8px;align-items:center;background:#fff6dc;border:2px solid #3a2414;border-radius:12px;padding:5px 9px;box-shadow:0 2px 0 #3a2414}')
rep('#ovHkTips li>i{flex:0 0 34px;height:34px;', '#ovHkTips li>i{flex:0 0 26px;height:26px;font-size:15px!important;')
rep('#ovHkTips li b{display:block;font:400 19px/1 Bangers', '#ovHkTips li b{display:block;font:400 15px/1 Bangers')
rep('#ovHkTips li span{display:block;font:700 14px/1.25 "Baloo 2",sans-serif;color:#3a2414}', '#ovHkTips li span{display:block;font:700 12px/1.2 "Baloo 2",sans-serif;color:#3a2414}')
rep('padding:13px 10px;font:400 24px/1 Bangers', 'padding:10px 10px;font:400 21px/1 Bangers')
rep('@media (max-height:700px){#ovHkTips li{padding:6px 9px}#ovHkTips li span{font-size:13px}#ovHkTips li b{font-size:17px}#ovHkTips h2{font-size:34px}#ovHkTips .htSub{display:none}}',
    '@media (max-height:700px){#ovHkTips li{padding:4px 8px}#ovHkTips li span{font-size:11.5px}#ovHkTips li b{font-size:14px}#ovHkTips h2{font-size:32px}#ovHkTips .htSub{display:none}}')
open(p, "w", encoding="utf-8").write(s)
print("ok V622")
