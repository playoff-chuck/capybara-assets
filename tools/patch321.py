"""V321 (Martin 06.11. 21:14, erstes Paket):
1. Kein doppeltes «Let's …»: zweiter «Let's»-Spruch innerhalb 8 s entfällt (z. B. «Let's make this wave count!» + «Let's roll!»).
2. Stürme je Kontinent: Asien nur Schneesturm (Sandsturm-Wellen 65/77/87 werden Blizzard), Afrika nur Sandsturm (Blizzard-Wellen 35/51 werden Sandsturm).
3. Weiterspielen nach dem Tod ab der letzten runden Welle davor (gestorben in 125 → weiter ab 121, Checkpoint 120).
   Checkpoint wird beim Game over gesichert (vorher nur am Ende von Welle 10/20/…, was beim Ortswechsel ausfallen konnte).
   Hauptmenü: PLAY = «CONTINUE · wave N» mit Ort; darunter klein «Start over · wave 1». Game over: «CONTINUE · WAVE N» oben.
4. Vibration deutlich spürbarer (vorher 14–22 ms, das spüren viele Handys nicht).
5. Karte: Ortsnamen, die unter die Titelkarte rutschen, stehen jetzt unter dem Punkt (Fund: «Redwoods»).
   Bei langen Flügen zeigt ein Pfeil am Rand mit Ortsnamen, wohin das Flugzeug fliegt (z. B. Asien → Nordamerika); Kamera schaut voraus."""
import sys
src, dst = sys.argv[1], sys.argv[2]
s = open(src, encoding='utf-8').read()
def rep(a, b, cnt=1):
    global s
    n = s.count(a); assert n == cnt, (n, a[:70]); s = s.replace(a, b)

rep('const GAME_VER = "V320";', 'const GAME_VER = "V321";')
# 2) Stürme je Kontinent
rep('function snowOn() { return S && S.started && !S.over && SNOW_BASES.includes(specBase()) && S.inWave && !S.paused && inPlay(); }',
    'const stormCont = () => { try { return S && !S.nuts ? wherePos(S.wave).cont[0] : ""; } catch (e) { return ""; } };   /* V321 */\n'
    'function snowOn() { if (!(S && S.started && !S.over && S.inWave && !S.paused && inPlay())) return false; const b = specBase(), c = stormCont(); return (SNOW_BASES.includes(b) && c !== "africa") || (DESERT_BASES.includes(b) && c === "asia"); }')
rep('function desertOn() { return S && S.started && !S.over && DESERT_BASES.includes(specBase()) && S.inWave && !S.paused && inPlay(); }',
    'function desertOn() { if (!(S && S.started && !S.over && S.inWave && !S.paused && inPlay())) return false; const b = specBase(), c = stormCont(); return (DESERT_BASES.includes(b) && c !== "asia") || (SNOW_BASES.includes(b) && c === "africa"); }   /* V321 */')
# 3) Hauptmenü PLAY = weiter ab Checkpoint
rep('$("modeList").innerHTML = `<button class="modeBtn playBtn" data-mode="pro"><span class="mName">PLAY ▶</span><span class="mSub">${b ? `Best · wave ${b}` : "South America · River Bank"}</span></button>`; return; }',
    '{ const cp = window.__cpGet ? window.__cpGet() : 0; if (cp >= 10) { const P = wherePos(cp + 1), nm = t => t.toLowerCase().replace(/\\b\\w/g, m => m.toUpperCase());   /* V321 */\n'
    '      $("modeList").innerHTML = `<button class="modeBtn playBtn" data-mode="pro" data-cont="1"><span class="mName">CONTINUE ▶</span><span class="mSub">Wave ${cp + 1} · ${nm(P.cont[1])} · ${nm(P.place)}</span></button><button class="newRun" data-mode="pro" data-new="1">Start over · wave 1</button>`; return; } }\n'
    '    $("modeList").innerHTML = `<button class="modeBtn playBtn" data-mode="pro"><span class="mName">PLAY ▶</span><span class="mSub">${b ? `Best · wave ${b}` : "South America · River Bank"}</span></button>`; return; }')
rep('if (window.ONE_MODE) { startGame(k); return; }',
    'if (window.ONE_MODE) { const cp = window.__cpGet ? window.__cpGet() : 0; if (b.dataset.cont && cp >= 10) { startGame(k, cp); return; } startGame(k); return; }   /* V321 */')
# 4) Vibration spürbarer
rep('buzz(d >= 3 ? [20, 40, 20] : [d === 2 ? 22 : 14], false);', 'buzz(d >= 3 ? [60, 50, 60] : [d === 2 ? 55 : 40], false);   /* V321: spürbar */')
# 5) Karte: Zielpfeil am Rand + Ortsnamen unter den Punkt, wenn sie unter die Titelkarte rutschen
rep('<div class="mapSkip">tap to skip</div>`;', '<div class="mapSkip">tap to skip</div><div class="mapDest" hidden><b></b></div>`;')
rep('if (t < 1) requestAnimationFrame(step); else plane.classList.remove("on"); };',
    'destPtr(b, t < 1 ? x : -1, y); if (t < 1) requestAnimationFrame(step); else plane.classList.remove("on"); };')
rep('    function flyPlane(a, b, ms) {',
    '''    function destPtr(b, px, py) {   /* V321: Pfeil am Rand zeigt das Flugziel mit Namen */
      const el = ov.querySelector(".mapDest"); if (!el) return; if (px < 0) { el.hidden = true; return; }
      let nm = ""; MAP_PTS.forEach((pts, c) => pts.forEach((p, i) => { if (Math.abs(p[0] - b[0]) < 1e-6 && Math.abs(p[1] - b[1]) < 1e-6) nm = nice(CONTS[c][2][i]); }));
      const r = world.getBoundingClientRect(), W = vp.clientWidth, H = vp.clientHeight, bx = r.left + b[0] * r.width, by = r.top + b[1] * r.height;
      const top = 110, bot = H - 70, inside = bx > 20 && bx < W - 20 && by > top && by < bot; if (inside) { el.hidden = true; return; }
      const cx = W / 2, cy = (top + bot) / 2, dx = bx - cx, dy = by - cy, f = Math.min((W / 2 - 70) / Math.max(1e-6, Math.abs(dx)), ((bot - top) / 2 - 24) / Math.max(1e-6, Math.abs(dy)));
      el.hidden = false; el.style.left = (cx + dx * f) + "px"; el.style.top = (cy + dy * f) + "px";
      const ang = Math.atan2(dy, dx) * 180 / Math.PI; el.style.setProperty("--ang", ang + "deg"); el.querySelector("b").textContent = (dx < 0 ? "◀ " : "") + nm + (dx >= 0 ? " ▶" : ""); }
    function flyPlane(a, b, ms) {''')
rep('cam = { ...cam, x: cam.x + (x - cam.x) * f, y: cam.y + (y - cam.y) * f }; apply(0); }   /* V317: Kamera folgt dem Flugzeug */',
    'const lx = x + (b[0] - x) * 0.25, ly = y + (b[1] - y) * 0.25; cam = { ...cam, x: cam.x + (lx - cam.x) * f, y: cam.y + (ly - cam.y) * f }; apply(0); }   /* V317/V321: Kamera folgt dem Flugzeug und schaut voraus */')
# Flugbogen nach unten, wenn er sonst oben aus dem Bild (unter die Titelkarte) liefe (Asien → Nordamerika)
rep('function flyPlane(a, b, ms) { const t0 = performance.now(),', 'function flyPlane(a, b, ms) { const arc = Math.min(a[1], b[1]) < 0.3 ? -.05 : .12, t0 = performance.now(),')
rep('Math.sin(Math.PI * e) * .12', 'Math.sin(Math.PI * e) * arc')
rep('Math.cos(Math.PI * e) * 0.12', 'Math.cos(Math.PI * e) * arc')
CSS = '''
/* V321 */
#ovMap .mapDest{position:absolute;z-index:6;transform:translate(-50%,-50%);pointer-events:none}
#ovMap .mapDest b{display:block;white-space:nowrap;font:400 17px/1 var(--f-display,"Bangers",sans-serif);letter-spacing:.04em;color:#3a2414;background:#ffd84d;border:3px solid #3a2414;border-radius:12px;padding:6px 10px 4px;box-shadow:0 3px 0 #3a2414;animation:mdPulse 1s ease-in-out infinite}
@keyframes mdPulse{50%{transform:scale(1.08)}}
.mPin.lblDown em{top:16px!important;transform:translate(-50%,0)!important}
.mPin.cur.lblDown em{top:30px!important}
.newRun{display:block;margin:10px auto 0;background:none;border:0;color:#fff7e8;font:700 14px/1.2 var(--f-body,"Baloo 2",sans-serif);text-decoration:underline;text-underline-offset:3px;opacity:.85;text-shadow:0 1px 2px rgba(0,0,0,.6);padding:6px 10px}
'''
i = s.index('</style>'); s = s[:i] + CSS + s[i:]
JS = r'''
/* V321: doppeltes «Let's» vermeiden */
try { (() => { const sy = SFX.say; let letT = -1e9; SFX.say = function (k) { try { const t = String((typeof VOICE_TEXT !== "undefined" && VOICE_TEXT[k]) || k || ""); if (/^let'?s\b/i.test(t)) { const now = performance.now(); if (now - letT < 8000) return; letT = now; } } catch (e) {} return sy.apply(SFX, arguments); }; })(); } catch (e) { console.error("v321 lets", e); }
/* V321: Checkpoint = letzte runde Welle vor dem Tod (125 → 120), Game over zeigt CONTINUE */
try { (() => { const key = () => "tarnturm-cp-" + (window.ONE_MODE ? "pro" : MODE);
  window.__cpGet = () => +LS.get(key()) || 0;
  const bump = w => { const c = Math.floor(((w | 0) - 1) / 10) * 10; if (c >= 10 && c > window.__cpGet()) LS.set(key(), c); };
  window.__cpBump = bump;
  const _go = gameOver; gameOver = function () { try { if (S && !S.nuts && !S.testRun) bump(S.wave); } catch (e) {} const r = _go.apply(this, arguments);
    try { const cp = window.__cpGet(), bc = $("btnCp"); if (bc && cp >= 10 && !(S && S.nuts)) { bc.hidden = false; bc.innerHTML = `CONTINUE · WAVE ${cp + 1}`; bc.classList.add("btn-big"); const p = bc.parentNode; if (p && p.firstElementChild !== bc) p.insertBefore(bc, p.firstElementChild); const rs = $("btnRestart"); if (rs) { rs.classList.remove("btn-big"); rs.textContent = "Start over · wave 1"; } } } catch (e) {}
    return r; };
  try { if (typeof renderModes === "function") renderModes(); } catch (e) {}
})(); } catch (e) { console.error("v321 cp", e); }
/* V321: Ortsnamen auf der Karte nie unter der Titelkarte */
try { (() => { setInterval(() => { const ov = document.getElementById("ovMap"); if (!ov || ov.hidden) return; const top = ov.querySelector(".mapTop"); if (!top) return; const tb = top.getBoundingClientRect().bottom + 6;
    ov.querySelectorAll(".mPin").forEach(p => { const em = p.querySelector("em"); if (!em) { p.classList.remove("lblDown"); return; } const pr = p.getBoundingClientRect(); const down = p.classList.contains("lblDown");
      const need = down ? pr.top - (p.classList.contains("cur") ? 70 : 14) - em.offsetHeight < tb : em.getBoundingClientRect().top < tb; if (need !== down) p.classList.toggle("lblDown", need); }); }, 200); })(); } catch (e) { console.error("v321 lbl", e); }
'''
anchor = '})();\n</script>'
p = s.rindex(anchor); s = s[:p] + JS + s[p:]
open(dst, 'w', encoding='utf-8').write(s)
print("ok")
