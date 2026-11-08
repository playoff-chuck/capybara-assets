#!/usr/bin/env python3
"""V446 (Martin 08.11. 12:46):
1. Unkraut-Warnkarte von Blue kommt früh: ~60 s nachdem das Unkraut wurzelt (Spiel steht, «Got it»); bei 2 freien Zeilen nur noch Blues Stimme.
2. Wolf call ist jetzt ein Lucky-Supply-Gewinn (ab Welle 100).
3. Gratis-Ten-ton vor Unkraut-Wellen mit mehreren Samen fällt nicht mehr von allein: Air-Drop-Karte «WEED DEFENSE DROP», Knopf «DROP IT» wirft ihn sofort; Samen warten so lange.
Nutzung: python3 tools/patch446.py src dst"""
import sys
src, dst = sys.argv[1], sys.argv[2]
s = open(src, encoding="utf-8").read()

def rep(a, b, n=1):
    global s
    c = s.count(a)
    assert c == n, (c, a[:80])
    s = s.replace(a, b)

rep('GAME_VER = "V445"', 'GAME_VER = "V446"')

# 1) frühe Karte
rep('    for (const w of D.weeds) {\n',
    '''    if (D.weeds.some(w => w.root != null)) { if (S.inWave && !frozen()) D.weedAge = (D.weedAge || 0) + dt; if (D.weedAge >= 60 && !D.weedW0) { D.weedW0 = true; try { weedCard(); } catch (e) {} } }   /* V446: Karte ~1 min nach dem Wurzeln */
    for (const w of D.weeds) {
''')
rep('if (left <= 2 && !D.weedW2) { D.weedW2 = true; try { window.__rbSay && window.__rbSay("rb_weedlast", true); } catch (e) {} try { weedCard(); } catch (e) {} }   /* V444: Karte */',
    'if (left <= 2 && !D.weedW2) { D.weedW2 = true; try { window.__rbSay && window.__rbSay("rb_weedlast", true); } catch (e) {} if (!D.weedW0) { D.weedW0 = true; try { weedCard(); } catch (e) {} } }   /* V446: Karte spätestens hier */')

# 3) Gratis-Ten-ton als Air-Drop-Karte, Samen warten
rep('const dl = n > 1 ? 3 : 0; if (n > 1) { try { if (!S.ton) { S.tons = (S.tons || 0) + 1; startTon(); } } catch (e) {} }   /* V425: erst Ten-ton, dann Samen */',
    'const dl = n > 1 ? 9999 : 0; D.weedAge = 0; D.weedW0 = false; if (n > 1) { try { S.tons = (S.tons || 0) + 1; if (window.__dropAd) { window.__dropAd("weed"); } else { startTon(); (D.weeds || []).forEach(w => { w.delay = 3; }); } } catch (e) {} }   /* V446: Gratis-Ten-ton als Air-Drop, Samen warten (Notfall 40 s) */')
rep('D.weeds = xs.map(x => ({ x, root: null, h: 0, seedY: -1, growT: Math.random() * 1.5, waves: 0, delay: dl + Math.random() * 0.4 })); }',
    'D.weeds = xs.map(x => ({ x, root: null, h: 0, seedY: -1, growT: Math.random() * 1.5, waves: 0, delay: dl + Math.random() * 0.4 })); if (n > 1) setTimeout(() => { try { (D.weeds || []).forEach(w => { if (w.delay > 100) w.delay = 2 + Math.random() * 0.4; }); } catch (e) {} }, 40000); }')
rep('''                 rot: { img: "img/ad_drop_free.webp", name: `${o.rp || "+90°"} PACKAGE`,''',
    '''                 weed: { img: "img/ad_drop_free.webp", name: "WEED DEFENSE DROP", line: "Weed seeds are about to land. HQ sent a Ten-ton drop – use it NOW to flatten the field before they sprout!", met: ["+1 Ten-ton", "Use it now"], btn: "DROP IT ▶" },   /* V446 */
                 rot: { img: "img/ad_drop_free.webp", name: `${o.rp || "+90°"} PACKAGE`,''')
rep('if (!D) return; cur = "drop"; saleMode = false; isFree = true; dropBtn = D.btn; late = true; S.intro = true; S.adOpen = true;',
    'if (!D) return; cur = "drop"; window.__dropKind = kind; saleMode = false; isFree = true; dropBtn = D.btn; late = true; S.intro = true; S.adOpen = true;')
rep('function close(bought) { ov.classList.remove("on"); ov.hidden = true; const k = cur; cur = null; if (k === "drop") { bought = false; $a("adCard").classList.remove("drop"); }',
    'function close(bought) { ov.classList.remove("on"); ov.hidden = true; const k = cur; cur = null; if (k === "drop") { bought = false; $a("adCard").classList.remove("drop"); if (window.__dropKind === "weed") { window.__dropKind = null; setTimeout(() => { try { if (S && S.started && !S.over && !S.ton) startTon(); } catch (e) {} try { (window.__dist.D.weeds || []).forEach(w => { if (w.delay > 100) w.delay = 2.5 + Math.random() * 0.4; }); } catch (e) {} }, 300); } }   /* V446 */')

# 2) Wolf call im Lucky Supply (ab W100)
rep('const IMG = { snipe: "img/slot_snipe.webp", mix: "img/slot_mix.webp", tesla: "img/slot_tesla.webp", lock: "img/slot_lock.webp", chomp: "img/slot_chomp.webp", ton: "img/slot_ton.webp" };',
    'const IMG = { snipe: "img/slot_snipe.webp", mix: "img/slot_mix.webp", tesla: "img/slot_tesla.webp", lock: "img/slot_lock.webp", chomp: "img/slot_chomp.webp", ton: "img/slot_ton.webp", wolf: "img/wolf_icon.webp" };')
rep('["lock", "Lockdown", "locks"], ["chomp", "Chomper", "chomps"], ["ton", "Ten-ton drop", "tons"]];',
    '["lock", "Lockdown", "locks"], ["chomp", "Chomper", "chomps"], ["ton", "Ten-ton drop", "tons"], ["wolf", "Wolf call", "wolves"]];\n    const PRa = () => (S && (S.wave || 0) >= 100) ? PR : PR.filter(p => p[0] !== "wolf");   /* V446: Wolf call erst ab W100 */')
rep('const p = k === LEN - 1 && last ? last : PR[(k * 5 + i * 2 + Math.floor(Math.random() * 6)) % 6];',
    'const P = PRa(), p = k === LEN - 1 && last ? last : P[(k * 5 + i * 2 + Math.floor(Math.random() * 6)) % P.length];')
rep('prize = (rescue && PR.find(p => p[0] === "ton")) || PR[Math.floor(Math.random() * PR.length)];',
    'prize = (rescue && PR.find(p => p[0] === "ton")) || PRa()[Math.floor(Math.random() * PRa().length)];')
open(dst, "w", encoding="utf-8").write(s)
print("ok", dst)
