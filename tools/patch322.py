"""V322 (Martin 06.11. 21:14, zweites Paket):
1. Pause-Menü passt auf einen Screen: «World map» raus, Nuts-Umwege als kleine Kacheln (2 Spalten, gleiche Schrift für Name und Zeile),
   Abstände kleiner; Sound-Regler passen ohne Zoomen mit drauf (auch 360×640).
2. Basisturm platzieren: sichtbarer «✕ CANCEL»-Knopf über dem Spielfeld, solange man den Block wählt.
3. Betonmischer füllt nur bis zum höchsten Punkt des angeklickten Blocks (Spalte ±1), nicht bis zu höheren Blöcken weiter weg."""
import sys
src, dst = sys.argv[1], sys.argv[2]
s = open(src, encoding='utf-8').read()
def rep(a, b, cnt=1):
    global s
    n = s.count(a); assert n == cnt, (n, a[:70]); s = s.replace(a, b)

rep('const GAME_VER = "V321";', 'const GAME_VER = "V322";')
rep('let top = GH; for (let c = 0; c < NN; c++) if (S.grid[c]) { top = (c / GW) | 0; break; }',
    'let top = GH; for (let cx = Math.max(0, x - 1); cx <= Math.min(GW - 1, x + 1); cx++) for (let r = 0; r < GH; r++) if (S.grid[r * GW + cx]) { top = Math.min(top, r); break; }   /* V322: nur bis zum Block, auf den man tippt */')
rep('<em>${nzFirstOpen(c) ? "first try · +1 % main score per level" : "replay · best L" + nzBest(c) + " · board & medals only"}</em>',
    '<em>${nzFirstOpen(c) ? "+1 % per level" : "best L" + nzBest(c)}</em>')
CSS = '''
/* V322: Pause-Menü auf einen Screen */
#ovPause #btnPMap,#btnPMap{display:none!important}
#ovPause .pNuts{display:grid!important;grid-template-columns:1fr 1fr;gap:5px!important}
#ovPause .pNuts small,#ovPause .pNuts .nBonus{grid-column:1/-1}
#ovPause .pNuts button{padding:5px 6px 4px!important;min-height:0!important;font:400 13px/1.05 var(--f-display,"Bangers",sans-serif)!important;letter-spacing:.04em;border-width:2px!important;border-radius:12px!important}
#ovPause .pNuts button em{font:400 11px/1.1 var(--f-display,"Bangers",sans-serif)!important;letter-spacing:.05em;opacity:.8;margin-top:2px}
#ovPause .pNuts .nBonus{font-size:11px}
#ovPause .pVol .pvRow{padding:1px 0!important;min-height:0!important}
#ovPause .pVol{padding:6px 10px!important;gap:2px!important}
@media (max-height:780px){#ovPause .pauseBtns{gap:5px!important}#ovPause .pauseBtns>button{padding-top:7px!important;padding-bottom:6px!important}#ovPause h2{margin:0!important;font-size:28px!important}#ovPause .btn-big{padding-top:8px!important;padding-bottom:7px!important}#ovPause .pSpeed{margin-top:4px!important}#ovPause .pCapy{height:54px!important;width:auto!important;margin-top:-34px!important}.pauseOv:not([hidden]){padding-top:calc(env(safe-area-inset-top,0px) + 44px)!important}#ovPause .pVol .pvRow{height:26px!important}}
/* V322: CANCEL beim Platzieren */
#buildCancel{position:fixed;left:50%;transform:translateX(-50%);z-index:60;font:400 18px/1 var(--f-display,"Bangers",sans-serif);letter-spacing:.05em;color:#fff;background:#d9483b;border:3px solid #3a2414;border-radius:14px;box-shadow:0 4px 0 #3a2414;padding:8px 16px 6px}
'''
i = s.index('</style>'); s = s[:i] + CSS + s[i:]
JS = r'''
/* V322: sichtbarer CANCEL-Knopf beim Platzieren eines Turms */
try { (() => { const b = document.createElement("button"); b.id = "buildCancel"; b.type = "button"; b.textContent = "✕ CANCEL"; b.hidden = true; document.body.appendChild(b);
  b.addEventListener("click", e => { e.stopPropagation(); try { if (S && S.mode === "build") { S.mode = null; S.aim = null; snd("uiTap"); } } catch (er) {} b.hidden = true; });
  setInterval(() => { const on = !!(S && S.started && !S.over && S.mode === "build" && !S.paused); if (on) { const bd = document.getElementById("board"); if (bd) { const r = bd.getBoundingClientRect(); b.style.top = Math.max(8, r.top + 8) + "px"; } } if (b.hidden === on) b.hidden = !on; }, 150); })(); } catch (e) { console.error("v322 cancel", e); }
/* V322: Pause-Menü – Sound-Bereich scrollt nie aus dem Bild */
try { (() => { const ov = document.getElementById("ovPause"); if (!ov) return; new MutationObserver(() => { if (!ov.hidden) setTimeout(() => { try { ov.scrollTop = 0; } catch (e) {} }, 0); }).observe(ov, { attributes: true, attributeFilter: ["hidden"] }); })(); } catch (e) {}
'''
anchor = '})();\n</script>'
p = s.rindex(anchor); s = s[:p] + JS + s[p:]
open(dst, 'w', encoding='utf-8').write(s)
print("ok")
