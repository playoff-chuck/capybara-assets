#!/usr/bin/env python3
# V571 (Martin 10.11. 23:36, Video mit Kommentar): Kurs nachgeschärft
# - Flugzeug auf der Karte: Ton erst, wenn das Flugzeug ins Bild fliegt
# - Hut-Knopf «ОБУЧЕНИЕ»: Schrift passt in den Knopf
# - Streifen: Bambus-Rahmen sichtbar, Lektions-Symbole farbig (nicht grau), kleine Nummer an offenen Lektionen
# - Lob kommt von Blu (weiße Sprechblase, Martins Stimme), nie über offenem Laden/Turm-Menü; grüne Pille weg
# - Im Kurs nur Kurs-Meldungen: keine anderen Blu-Sprüche, Toasts, Uhrzeit-/Wellen-Meldungen, Ansager-Stimmen
# - Lektion 7 (Ring): Pfeil bleibt fest rechts oben
# - Lektion 9 (Spezialmittel): Laden scrollt selbst zum Sniper, Pfeil sofort; beim Zielen Erklärung (Monster + Blöcke 2×2)
# - Lektion 10: erst fertig, wenn der zweite Turm gebaut UND bewaffnet ist
# - Urkunde sofort nach Lektion 10; Air Drop (Zehntonne) erst nach der Urkunde; Lucky Supply erst 2 Wellen nach dem Kurs
import sys
src, dst = sys.argv[1], sys.argv[2]
s = open(src, encoding="utf-8").read()
def rep(a, b, n=1):
    global s
    c = s.count(a); assert c == n, (c, a[:90]); s = s.replace(a, b)
rep('const GAME_VER = "V570";', 'const GAME_VER = "V571";')

# Flugzeug-Ton synchron
rep('      step(t0); try { window.__planeSnd && window.__planeSnd(ms, a[0] > 1 || a[0] < 0); } catch (e) {} }',
    '''      step(t0); try { const off = a[0] > 1 || a[0] < 0; let dl = 0; if (off && b[0] !== a[0]) { const bx = a[0] > 1 ? 1 : 0, ee = Math.max(0, Math.min(1, (bx - a[0]) / (b[0] - a[0]))); dl = Math.max(0, Math.acos(1 - 2 * ee) / Math.PI * ms - 150); }   /* V571: Ton erst, wenn das Flugzeug ins Bild kommt */
        setTimeout(() => { try { window.__planeSnd && window.__planeSnd(ms - dl, off); } catch (e) {} }, dl); } catch (e) {} }''')

# Lektion 9: Scrollen + Zielen; Lektion 10: bewaffnen
rep('enter: () => { S.snipes = (S.snipes | 0) + 1; TUT.e.sn = S.snipes; }',
    'enter: () => { S.snipes = (S.snipes | 0) + 1; TUT.e.sn = S.snipes; TUT.scr = 0; TUT.aim = null; }')
rep('"Towers can fall when their block disappears – then just build a new one. Two towers at the edge hold the ring much better."',
    '"Towers can fall when their block disappears – then just build a new one. Build a second tower at the edge and arm it."')
rep('done: () => S.towers.size > TUT.e.tw || TUT.t >= 45 }',
    'done: () => !S.sel && !S.shop && S.mode !== "build" && ((S.towers.size > TUT.e.tw && [...S.towers.values()].reduce((a, t) => a + t.w.length, 0) > TUT.e.wp) || TUT.t >= 75) }')
rep('  const st = TUT_STEPS[TUT.step]; TUT.t += dt;\n',
    '''  const st = TUT_STEPS[TUT.step]; TUT.t += dt;
  if (st.ar === "spec") { const aim = S.mode === "snipe"; if (aim !== TUT.aim) { TUT.aim = aim; $("coachT").textContent = aim ? "AIM AT A SPOT!" : st.t; $("coachS").textContent = aim ? "Tap a spot on the field: the sniper splats every monster there and clears a 2×2 patch of blocks." : st.s; } }   /* V571 */
''')
rep('''        if (ar === "spec") { const pk = S.shop && document.getElementById("sheetIn") && document.getElementById("sheetIn").classList.contains("pk"); if (pk) return vis(document.querySelector('#sheetIn [data-pocket="snipe"]')); if (S.mode === "snipe" || sheetUp()) return null; return vis(document.getElementById("bBuild")); }
        const k = { drop: 0, splat: 0, build: 1, edge: 2, tower2: 2, arm: 3, rot: 4, ring: 5 }[ar];''',
    '''        if (ar === "spec") { const pk = S.shop && document.getElementById("sheetIn") && document.getElementById("sheetIn").classList.contains("pk"); if (pk) { const bq = document.querySelector('#sheetIn [data-pocket="snipe"]'); if (bq && !TUT.scr) { TUT.scr = 1; try { bq.scrollIntoView({ block: "center" }); } catch (e) {} } return vis(bq); } TUT.scr = 0; if (S.mode === "snipe" || sheetUp()) return null; return vis(document.getElementById("bBuild")); }   /* V571: Laden scrollt selbst zum Sniper */
        let k = { drop: 0, splat: 0, build: 1, edge: 2, tower2: 2, arm: 3, rot: 4, ring: 5 }[ar]; if (ar === "tower2" && S.sel) k = 3;   /* V571: zweiten Turm auch bewaffnen */''')
# Ring-Pfeil fest rechts oben
rep('          try { const m = S.monsters.find(q => q && !q.dead && q.cy >= 1); if (m) { const pt = cvPt(m.cx + 0.5, m.cy + 0.5); if (pt && pt.y > b.top + 110) { x = pt.x; y = pt.y; } } } catch (e) {}\n', '')

# Lob durch Blu statt grüner Pille
a = s.index("    done(i) { doneN = Math.max(doneN, i + 1);"); b = s.index("    hide() {", a)
s = s[:a] + '''    done(i) { doneN = Math.max(doneN, i + 1); paint(i + 1); const d = D(i); if (d) { d.classList.remove("pop"); void d.offsetWidth; d.classList.add("pop"); }
      try { snd("uiTap"); } catch (e) {}
      try { window.__rbSay && window.__rbSay(TUT_PRAISE[i % TUT_PRAISE.length], true); } catch (e) {} },   /* V571: Lob von Blu (Sprechblase + Martins Stimme) */
''' + s[b:]
rep('const TUT_SNAP = () =>', '''const TUT_PRAISE = ["goodjob", "nice", "great", "nailedit", "smooth", "terrific", "awesome", "brilliant", "fantastic", "outstanding"];   /* V571 */
window.__tutKeys = new Set(TUT_PRAISE);
const TUT_SNAP = () =>''')

# Blu: im Kurs nur Kurs-Lob
rep('      if (!S || !S.started || (S.over && key !== "rb_tea")) return;\n',
    '      if (!S || !S.started || (S.over && key !== "rb_tea")) return;\n      if (typeof TUT !== "undefined" && TUT.on && !(window.__tutKeys && window.__tutKeys.has(key))) return;   /* V571: im Kurs nur Kurs-Lob */\n')

# Urkunde sofort, Air Drop danach, Lucky Supply später
rep('SFX.say("Nice!"); window.__tutSumPend = performance.now(); } }',
    'window.__tutSumPend = performance.now(); window.__tutSumNow = true; try { S.tutDoneW = S.wave | 0; } catch (e) {} } }   /* V571: Urkunde gleich nach Lektion 10 */')
rep('const we = window.__waveEndT || 0; if (S.inWave || we < p || performance.now() - we < 2500) return;',
    'const we = window.__waveEndT || 0; if (!window.__tutSumNow && (S.inWave || we < p || performance.now() - we < 2500)) return;')
rep('window.__certNow = () => { window.__tutSumPend = 0;', 'window.__certNow = () => { window.__tutSumPend = 0; window.__tutSumNow = false;')
rep('''      setTimeout(() => { try { if (!S || !S.started || S.over) return; const ov = document.getElementById("ovAd"); if (ov && ov.hidden) window.__TT.ad.showDrop("tut"); else if (window.__dropAd) window.__dropAd("tut"); } catch (e) {} }, 700); } } catch (e) {}''',
    '''      const goAd = () => { try { if (!S || !S.started || S.over) return; if (window.__tutSumOpen || window.__tutSumPend) { setTimeout(goAd, 500); return; }   /* V571: Air Drop erst nach der Urkunde */
        setTimeout(() => { try { if (!S || !S.started || S.over) return; const ov = document.getElementById("ovAd"); if (ov && ov.hidden) window.__TT.ad.showDrop("tut"); else if (window.__dropAd) window.__dropAd("tut"); } catch (e) {} }, 900); } catch (e) {} }; setTimeout(goAd, 700); } } catch (e) {}''')
rep('    function open(force, resc) {\n',
    '    function open(force, resc) {\n      if (!resc && S && ((typeof TUT !== "undefined" && TUT.on) || window.__tutSumOpen || window.__tutSumPend || (S.tutDoneW != null && (S.wave | 0) < S.tutDoneW + 2))) return;   /* V571: Lucky Supply nicht im Kurs, erst 2 Wellen danach */\n')

CSS = '''<style id="v571tut">
#tutBar{background:#f3dfae url("img/tut_bamboo.webp?v=571") center/100% 100% no-repeat!important;padding:10px 16px 11px!important}
#tutBar .tbTrack{counter-reset:tb}
#tutBar .tbDot{counter-increment:tb;filter:none!important;opacity:1!important;transform:scale(.88)}
#tutBar .tbDot.cur{transform:scale(1.22)!important}
#tutBar .tbDot.ok{transform:scale(.95)}
#tutBar .tbDot:not(.ok)::before{content:counter(tb);position:absolute;left:-4px;top:-5px;min-width:13px;height:13px;padding:0 2px;box-sizing:border-box;border-radius:7px;background:#3a2414;color:#fff6dc;font:400 10px/13px Bangers,system-ui,sans-serif;text-align:center}
#tutPraise{display:none!important}
#bTut b{font-size:5.6px!important;letter-spacing:0!important;white-space:nowrap;max-width:35px;overflow:hidden}
body.tutBarOn #toast,body.tutBarOn #alert{display:none!important}
</style>
'''
rep("</body>", CSS + "</body>")

# Toasts und Ansager-Stimmen im Kurs aus
rep('/* V571-HOOK */', '', 0)
s = s.replace('window.__tutKeys = new Set(TUT_PRAISE);', '''window.__tutKeys = new Set(TUT_PRAISE);
setTimeout(() => { try { const _toK = toast; toast = function () { try { if (TUT.on) return; } catch (e) {} return _toK.apply(this, arguments); };
  if (typeof SFX !== "undefined" && SFX.say) { const _ssK = SFX.say; SFX.say = function (k) { try { if (TUT.on && !window.__tutKeys.has(k)) return; } catch (e) {} return _ssK.apply(this, arguments); }; } } catch (e) {} }, 0);   /* V571: im Kurs keine anderen Meldungen */''', 1)
open(dst, "w", encoding="utf-8").write(s)
print("ok")
