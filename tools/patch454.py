#!/usr/bin/env python3
"""V454 – Nuts-Abstecher neu (Martin 08.11. 13:55):
- Start mit 0 Gold (kein Turm-Gold mehr), Grundausstattung nur je 2 Specials; je geschafftem Level +1 000 Gold.
- Lucky Supply alle 5 Level (vor L6, L11, L16, L21, L26) – das einzige Event.
- Boss-Level L10/L20/L30: Kontinent-Boss (Jaguar/Mummy/Tiger/Grizzly, groß, 10× HP) führt die Welle an; Sieg +500 Gold.
- Höhlen-Look im Nuts-Feld (dunkler, Felswände, Tropfsteine) – per CSS, kein neues Bild.
Nutzung: python3 tools/patch454.py src dst"""
import sys
src, dst = sys.argv[1], sys.argv[2]
s = open(src, encoding="utf-8").read()

def rep(a, b, n=1):
    global s
    c = s.count(a)
    assert c == n, (c, a[:80])
    s = s.replace(a, b)

rep('const GAME_VER = "V453";', 'const GAME_VER = "V454";')

# Wirtschaft
rep('const NZ_KIT = { gold: 600, towerGold: 1000, lives: 5 };', 'const NZ_KIT = { gold: 0, towerGold: 0, lives: 5, perLevel: 1000, bossGold: 500 };   /* V454: Start bei 0 Gold, +1000 je Level */')
rep('  const n = S.nuts; n.cleared = n.lvl; const g = 40 + 10 * n.lvl; S.gold += g; lvLabel();',
    '  const n = S.nuts; n.cleared = n.lvl; const boss = n.lvl % 10 === 0, g = NZ_KIT.perLevel + (boss ? NZ_KIT.bossGold : 0); S.gold += g; lvLabel();   /* V454 */\n'
    '  if (boss) setTimeout(() => toast(`BOSS DOWN · +${NZ_KIT.bossGold} gold`, "NUTS", 2200), 2600);\n'
    '  if (n.lvl % 5 === 0 && n.lvl < NZ_MAX) setTimeout(() => { try { if (S && S.nuts && !S.over && window.__luckyOpen) window.__luckyOpen(); } catch (e) {} }, 3200);   /* V454: Lucky Supply alle 5 Level */')
rep('setTimeout(() => toast("SQUAD KIT · 2× every special · +1000 gold for towers", "ARMORY", 2600), 6200);',
    'setTimeout(() => toast("SQUAD KIT · 2× every special · 0 gold · +1000 per level", "ARMORY", 2600), 6200);')
rep('announce("NUTS DETOUR!", `${nzName(c)} · ${NZ_MAX} levels · no mercy`, "ALERT", 2800);',
    'announce("NUTS DETOUR!", `${nzName(c)} · ${NZ_MAX} levels · no mercy · boss every 10`, "ALERT", 2800);')

# Lucky Supply von außen öffnen
rep('    setInterval(() => { try { if (ov.hidden && calm()) open(false); } catch (e) {} }, 500);',
    '    setInterval(() => { try { if (ov.hidden && calm()) open(false); } catch (e) {} }, 500);\n'
    '    window.__luckyOpen = () => { try { if (ov.hidden && S && S.started && !S.over && !S.paused && !S.drop && !S.duel) open(true); } catch (e) {} };   /* V454: Nuts-Lucky */')

# Boss-Level: erstes Monster der Welle ist der Kontinent-Boss
rep('''    if (S.nuts) for (let i = n0; i < S.monsters.length; i++) { const m = S.monsters[i]; const f = nutsHp(S.nuts.lvl); m.hp *= f; m.max *= f; m.speed *= nutsSpd(S.nuts.lvl); }
    return r; };''',
'''    if (S.nuts) for (let i = n0; i < S.monsters.length; i++) { const m = S.monsters[i]; const f = nutsHp(S.nuts.lvl); m.hp *= f; m.max *= f; m.speed *= nutsSpd(S.nuts.lvl);
      if (S.nuts.lvl % 10 === 0 && !S.nuts.bossOut) {   /* V454: Boss-Level L10/20/30 */
        S.nuts.bossOut = S.nuts.lvl; const bk = ["jaguar", "mummy", "tiger", "bear"][S.nuts.c] || "kiefer"; m.kind = monFrom(bk) <= (S.nuts.mainW || S.nuts.base) ? bk : "kiefer";
        m.hp *= 10; m.max = m.hp; m.speed *= 0.7; m.big = 1.7; m.boss = true; m.reward = Math.round(m.reward * 5);
        setTimeout(() => { try { announce("BOSS LEVEL!", `${MON_INFO.find(x => x[0] === m.kind)?.[1] || "The boss"} leads the pack · splat it for +${NZ_KIT.bossGold} gold`, "ALERT", 2600); snd("siren"); } catch (e) {} }, 400); } }
    return r; };''')
rep('if (S.nuts) { S.wave = S.nuts.base - 1; S.nuts.lvl++; }', 'if (S.nuts) { S.wave = S.nuts.base - 1; S.nuts.lvl++; S.nuts.bossOut = 0; }')
# Großer Boss beim Zeichnen
rep('const ph=m.ph||0,r=s*(MON_R[k]||0.33),bob=Math.abs', 'const ph=m.ph||0,r=s*(MON_R[k]||0.33)*(m.big||1),bob=Math.abs')
rep('setTimeout(() => announce(`NUTS LEVEL ${S.nuts.lvl}/${NZ_MAX}`, `${S.toSpawn} monsters · faster · tougher`, "ALERT", 1600), 60);',
    'if (S.nuts.lvl % 10 !== 0) setTimeout(() => announce(`NUTS LEVEL ${S.nuts.lvl}/${NZ_MAX}`, `${S.toSpawn} monsters · faster · tougher`, "ALERT", 1600), 60);')

# Höhlen-Look
rep('body.inNuts #sky{filter:brightness(.5) saturate(.75) sepia(.25) hue-rotate(-18deg)!important}',
    'body.inNuts #sky{filter:brightness(.28) saturate(.6) sepia(.45) hue-rotate(-22deg) contrast(1.15)!important}\n'
    'body.inNuts::before{content:"";position:fixed;inset:0;pointer-events:none;z-index:3;background:'
    'radial-gradient(ellipse 14% 30% at 4% 20%,rgba(20,8,6,.95),transparent 70%),radial-gradient(ellipse 12% 26% at 2% 62%,rgba(20,8,6,.95),transparent 70%),'
    'radial-gradient(ellipse 14% 30% at 96% 28%,rgba(20,8,6,.95),transparent 70%),radial-gradient(ellipse 12% 26% at 98% 70%,rgba(20,8,6,.95),transparent 70%),'
    'radial-gradient(ellipse 9% 16% at 18% -2%,rgba(26,10,8,.98),transparent 70%),radial-gradient(ellipse 7% 20% at 36% -4%,rgba(26,10,8,.98),transparent 70%),'
    'radial-gradient(ellipse 10% 18% at 58% -3%,rgba(26,10,8,.98),transparent 70%),radial-gradient(ellipse 8% 22% at 80% -5%,rgba(26,10,8,.98),transparent 70%),'
    'linear-gradient(180deg,rgba(18,6,4,.75),rgba(18,6,4,0) 18%,rgba(18,6,4,0) 82%,rgba(18,6,4,.7))}\n'
    'body.inNuts::after{background:radial-gradient(ellipse at center,rgba(0,0,0,0) 48%,rgba(120,8,8,.5) 100%)!important}')
rep('const NUTS_D = { t: "", n: "NUTS", th: "moon", field: "rgba(52,18,14,.42)",',
    'const NUTS_D = { t: "", n: "NUTS", th: "moon", field: "rgba(34,12,10,.58)",')

open(dst, "w", encoding="utf-8").write(s)
print("ok", dst)

# --- Nachtrag (Martin 13:58): Fallschirm-Schwingen weicher – zwei Bilder überblenden, 320 ms je Bild ---
s = open(dst, encoding="utf-8").read()
rep('<img class="wpSpr" src="img/${sp}_1.webp" alt=""></div>`',
    '<img class="wpSpr" src="img/${sp}_1.webp" alt=""><img class="wpSpr wpSpr2" src="img/${sp}_2.webp" alt=""></div>`')
rep('if (spr) { const im = d.querySelector(".wpSpr"); const seq = [1, 2, 3, 4, 5, 6, 5, 4, 3, 2]; let i = 0; const iv = setInterval(() => { if (!document.body.contains(d)) { clearInterval(iv); return; } i = (i + 1) % seq.length; im.src = `img/${sp}_${seq[i]}.webp`; }, 150); }',
    'if (spr) { const ims = [d.querySelector(".wpSpr"), d.querySelector(".wpSpr2")]; const seq = [1, 2, 3, 4, 5, 6, 5, 4, 3, 2]; let i = 0, top = 0; const iv = setInterval(() => { if (!document.body.contains(d)) { clearInterval(iv); return; } i = (i + 1) % seq.length; top = 1 - top; ims[top].src = `img/${sp}_${seq[i]}.webp`; ims[top].style.opacity = "1"; ims[1 - top].style.opacity = "0"; }, 320); }   /* V454: weich überblendet statt hartem Bildwechsel */')
rep('.wpChute.spr .wpSpr{position:absolute;left:-44px;top:-110px;width:88px;height:110px;max-width:none;object-fit:contain;transform:scale(.2);transform-origin:50% 100%;animation:wowOpen .35s ease-out 1.25s forwards;filter:drop-shadow(0 3px 3px rgba(0,0,0,.35))}',
    '.wpChute.spr .wpSpr{position:absolute;left:-44px;top:-110px;width:88px;height:110px;max-width:none;object-fit:contain;transform:scale(.2);transform-origin:50% 100%;animation:wowOpen .35s ease-out 1.25s forwards;filter:drop-shadow(0 3px 3px rgba(0,0,0,.35));transition:opacity .3s ease-in-out}.wpChute.spr .wpSpr2{opacity:0}')
open(dst, "w", encoding="utf-8").write(s)
print("ok chute")

# --- Nachtrag (Martin 14:00/14:01): Hall of Fame in derselben Schrift/Form wie Medals & Squad; runde X-Knöpfe überall; Weltkarte unten mit Comic-Rand ---
s = open(dst, encoding="utf-8").read()
rep('.hs h4{color:var(--ink)!important;font-family:var(--f-display)!important}',
    '.hs h4{color:var(--ink)!important;font-family:Bangers,system-ui!important;font-size:18px!important;letter-spacing:.5px!important;text-align:left;margin:10px 0 4px!important;font-weight:400}   /* V454: wie .albSec */\n'
    '#ovHs .hs{font-family:"Baloo 2",system-ui,sans-serif;font-size:15px}#ovHs .hs .row{padding:3px 6px;line-height:1.25}#ovHs .hs .row span:nth-child(2){font-weight:700}#ovHs .hs .row span:nth-child(1){font-weight:700;color:#7a6650}\n'
    '#hsPlaces .prCont{text-align:left!important;font:400 14px/1.2 Bangers,system-ui!important;letter-spacing:.5px!important;opacity:.8!important}#hsPlaces .prKey{text-align:left}\n'
    '.albX,#ovHs .hsBox .albX{width:40px!important;height:40px!important;min-height:0!important;padding:0!important;line-height:1!important;aspect-ratio:1/1}')
rep('#ovMap .mapVp{position:absolute;inset:0;overflow:hidden}',
    '#ovMap .mapVp{position:absolute;inset:0;overflow:hidden}\n'
    '#ovMap .mapVp::after{content:"";position:absolute;left:-6px;right:-6px;bottom:-6px;height:calc(env(safe-area-inset-bottom,0px) + 20px);background:#3a2414;border-top:4px solid #fff7e8;box-shadow:0 -4px 0 #3a2414,0 -10px 18px rgba(0,0,0,.35);border-radius:18px 18px 0 0;pointer-events:none;z-index:4}   /* V454: Comic-Rand unten (Martin 08.11. 14:01) */\n'
    '#ovMap .mapVp::before{content:"";position:absolute;left:0;right:0;bottom:calc(env(safe-area-inset-bottom,0px) + 12px);height:70px;background:linear-gradient(180deg,rgba(58,36,20,0),rgba(58,36,20,.5));pointer-events:none;z-index:4}   /* dazu Ausblenden über dem Rand */\n'
    '#ovMap .mapBar,#ovMap .mapRose,#ovMap .mapReplay{z-index:6}'
    '#ovMap.auto .mapVp::after{display:none}')
open(dst, "w", encoding="utf-8").write(s)
print("ok hof/map")
