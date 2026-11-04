"""V214: Anzeige oben steht fest (Herzen/Gold/Vorschau verschieben sich nicht mehr), Durchtipp-Schutz nach dem
Schließen von Turm-/Shop-Fenster, Startscreen: Zahnrad und weißer Sound-Knopf weg, rosa Mute-Knopf rechts oben."""
import sys
src, dst = sys.argv[1], sys.argv[2]
s = open(src, encoding='utf-8').read()
def rep(a, b, cnt=1):
    global s
    n = s.count(a); assert n == cnt, (n, a[:70]); s = s.replace(a, b)
rep('const GAME_VER = "V213";', 'const GAME_VER = "V214";')
# Durchtipp-Schutz: nach dem Schließen 450 ms keine Feld-Tipps
rep('function closeSheet() {', 'function closeSheet() { window.__tapGuard = performance.now() + 450;')
rep('cv.addEventListener("pointerdown", e => {\n  if (!S.started || S.over) return;', 'cv.addEventListener("pointerdown", e => {\n  if (!S.started || S.over) return;\n  if (performance.now() < (window.__tapGuard || 0)) return;')
# Fall-Sperre länger (Martin: 300 ms reicht nicht)
rep('function spawnPiece() { S.dropLockUntil = performance.now() + 300;', 'function spawnPiece() { S.dropLockUntil = performance.now() + 650;')
# Geschenk-Link: playcapybarasquad.com/?gift=ton → beim CONTINUE +1 Ten-ton drop (einmalig je Link-Aufruf)
rep('  S.dirty = true; S.started = true; S.paused = false; closeSheet(); drawNext();',
    '  S.dirty = true; S.started = true; S.paused = false; closeSheet(); drawNext();\n  try { const q = new URLSearchParams(location.search); if (q.get("gift") === "ton" && !window.__giftDone) { window.__giftDone = true; S.tons = (S.tons || 0) + 1; history.replaceState(null, "", location.pathname); setTimeout(() => toast("GIFT FROM HQ · +1 Ten-ton drop", "SQUAD", 2600), 2900); saveGame(); } } catch (e) {}')
js = '''
  /* V214: Mute-Knopf rechts oben auf dem Startscreen */
  try { const st = document.getElementById("ovStart"); if (st && !document.getElementById("stMute")) { const b = document.createElement("button"); b.id = "stMute"; b.type = "button"; b.setAttribute("aria-label", "Mute");
      const paint = () => { const m = !!(SFX && SFX.muted); b.classList.toggle("off", m); b.innerHTML = m ? '<svg viewBox="0 0 24 24" width="22" height="22"><path d="M4 9h4l5-4v14l-5-4H4z" fill="currentColor"/><path d="M16 9l5 6M21 9l-5 6" stroke="currentColor" stroke-width="2.4" stroke-linecap="round"/></svg>' : '<svg viewBox="0 0 24 24" width="22" height="22"><path d="M4 9h4l5-4v14l-5-4H4z" fill="currentColor"/><path d="M16 8.5a5 5 0 0 1 0 7M18.5 6a8.5 8.5 0 0 1 0 12" stroke="currentColor" stroke-width="2" fill="none" stroke-linecap="round"/></svg>'; };
      b.addEventListener("click", e => { e.stopPropagation(); try { SFX.init(); SFX.toggle(); muteLabel(); } catch (er) {} paint(); }); st.appendChild(b); paint(); setInterval(paint, 1000); } } catch (e) {}
'''
i = s.rfind('})();\n</script>'); s = s[:i] + js + s[i:]
css = '''<style id="v214">
/* Anzeige oben: feste Breiten */
.barCanopy .grp{justify-content:flex-start!important;padding-left:18px!important}
.barCanopy .grp .stat{flex:0 0 auto!important}
#sLives{display:inline-block!important;width:30px!important;min-width:30px!important;text-align:left!important;font-variant-numeric:tabular-nums}
#sGold{display:inline-block!important;width:62px!important;min-width:62px!important;text-align:left!important;overflow:visible;font-variant-numeric:tabular-nums}
.barCanopy .score b,#sScore{font-variant-numeric:tabular-nums}
/* Startscreen: Zahnrad + weißer Sound weg, rosa Mute rechts oben */
body:has(#ovStart:not([hidden])) #btnGear,body:has(#ovStart:not([hidden])) .gearTR,body:has(#ovStart:not([hidden])) .hdrSound,body:has(#ovStart:not([hidden])) #bSound{display:none!important}
#stMute{position:fixed!important;top:calc(env(safe-area-inset-top,0px) + 12px)!important;right:calc(env(safe-area-inset-right,0px) + 12px)!important;width:44px!important;height:44px!important;min-width:0!important;min-height:0!important;padding:0!important;border-radius:50%!important;border:2px solid #3a2414!important;background:#ff8fc4!important;color:#3a2414!important;display:grid!important;place-items:center;box-shadow:0 3px 0 #3a2414!important;z-index:80!important}
#stMute.off{background:#e9dccb!important;color:#7a6650!important}
#ovStart[hidden] #stMute{display:none!important}
</style>
'''
i = s.rfind('</body>'); s = s[:i] + css + s[i:]
open(dst, 'w', encoding='utf-8').write(s); print('ok')
