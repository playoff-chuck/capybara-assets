"""V201: Pausemenü kompakt – deckt Anzeige und Steuerung ab, Capybara-Bild, großes RESUME, Restart/Menü klein
nebeneinander, Sound nur als kleiner rosa Knopf (Regler erst nach Antippen), Spieltempo als schmale Chips.
«Hero & name» und Hinweise raus (Held/Name gibt es im Hauptmenü)."""
import sys
src, dst = sys.argv[1], sys.argv[2]
s = open(src, encoding='utf-8').read()
def rep(a, b, cnt=1):
    global s
    n = s.count(a); assert n == cnt, (n, a[:70]); s = s.replace(a, b)
rep('const GAME_VER = "V200";', 'const GAME_VER = "V201";')
js = '''
  /* V201: Pausemenü kompakt */
  try { const ov = document.getElementById("ovPause");
    if (ov && !ov.querySelector(".pCard")) {
      const card = document.createElement("div"); card.className = "pCard";
      const img = document.createElement("img"); img.className = "pCapy"; img.alt = "";
      const sb = document.createElement("button"); sb.type = "button"; sb.className = "pSndBtn"; sb.setAttribute("aria-label", "Sound settings");
      sb.innerHTML = '<svg viewBox="0 0 24 24" width="20" height="20" aria-hidden="true"><path d="M4 9h4l5-4v14l-5-4H4z" fill="currentColor"/><path d="M16 8.5a5 5 0 0 1 0 7M18.5 6a8.5 8.5 0 0 1 0 12" stroke="currentColor" stroke-width="2" fill="none" stroke-linecap="round"/></svg>';
      card.append(sb, img);
      [...ov.children].forEach(c => card.appendChild(c));
      ov.appendChild(card);
      const row = document.createElement("div"); row.className = "pRow"; const r = document.getElementById("btnPRestart"), m = document.getElementById("btnPMenu");
      if (r && m) { r.parentNode.insertBefore(row, r); row.append(r, m); }
      const vol = document.getElementById("pVol"); if (vol) card.appendChild(vol);
      sb.addEventListener("click", e => { e.stopPropagation(); card.classList.toggle("sndOpen"); try { snd("uiTap"); } catch (er) {} });
      new MutationObserver(() => { if (!ov.hidden) { card.classList.remove("sndOpen"); try { img.src = HERO_IMG[heroKey()]; } catch (er) {} } }).observe(ov, { attributes: true, attributeFilter: ["hidden"] });
      try { img.src = HERO_IMG[heroKey()]; } catch (er) {}
    } } catch (e) {}
'''
i = s.rfind('})();\n</script>'); assert i > 0
s = s[:i] + js + s[i:]
css = '''<style id="v201">
/* V201 Pausemenü: eigene Ebene über Anzeige und Steuerung */
#ovPause.pauseOv:not([hidden]){position:fixed!important;inset:0!important;z-index:95!important;display:flex!important;align-items:center!important;justify-content:center!important;
  padding:calc(env(safe-area-inset-top,0px) + 12px) 14px calc(env(safe-area-inset-bottom,0px) + 12px)!important;margin:0!important;width:auto!important;height:auto!important;max-height:none!important;
  background:rgba(20,28,16,.62)!important;backdrop-filter:blur(3px);-webkit-backdrop-filter:blur(3px);border:0!important;box-shadow:none!important;border-radius:0!important;transform:none!important}
#ovPause .pCard{position:relative;width:min(340px,100%);background:#fff7e8;border:3px solid #3a2414;border-radius:22px;box-shadow:0 5px 0 #3a2414;padding:62px 16px 14px;display:flex;flex-direction:column;align-items:stretch;gap:10px}
#ovPause .pCapy{position:absolute;left:50%;top:-58px;width:110px;height:110px;margin-left:-55px;object-fit:contain;filter:drop-shadow(0 4px 4px rgba(0,0,0,.35));pointer-events:none}
#ovPause .pCard h2{margin:0!important;text-align:center;font-size:30px!important;line-height:1!important;color:#3a2414!important;text-shadow:none!important}
#ovPause .pauseBtns{display:flex!important;flex-direction:column!important;gap:8px!important;margin:0!important;width:100%!important;max-width:none!important;align-self:stretch!important}
#ovPause .pRow,#ovPause .pauseBtns>button{max-width:none!important}
body:has(#ovPause:not([hidden])) #alert,body:has(#ovPause:not([hidden])) #toast{display:none!important}
#ovPause .pauseBtns>button,#ovPause .pRow button{width:100%!important;min-height:0!important;margin:0!important}
#ovPause #btnPResume{height:52px!important;font-size:24px!important}
#ovPause .pRow{display:grid;grid-template-columns:1fr 1fr;gap:8px}
#ovPause .pRow button{height:40px!important;font-size:15px!important;padding:0 8px!important}
#ovPause #btnPSquad,#ovPause #btnPFb,#ovPause #btnPSound,#ovPause .pauseHint{display:none!important}
#ovPause #btnPNutsQuit:not([hidden]){height:38px!important;font-size:14px!important}
#ovPause .pSpeed{margin:0!important;padding:0!important;display:grid;gap:4px;justify-items:center}
#ovPause .pSpeed small{font-size:10px!important;letter-spacing:.12em;color:#9b7a5c!important}
#ovPause .pSpeedRow{display:flex!important;gap:5px!important;flex-wrap:nowrap!important;justify-content:center}
#ovPause .pSpeedRow button{min-width:0!important;width:auto!important;height:30px!important;padding:0 9px!important;font-size:13px!important;border-radius:999px!important;box-shadow:0 2px 0 #3a2414!important}
#ovPause .pSpeed em{font-size:11px!important}
#ovPause .pSndBtn{position:absolute!important;top:10px!important;right:10px!important;width:38px!important;height:38px!important;min-width:0!important;min-height:0!important;border-radius:50%!important;border:2px solid #3a2414!important;background:#ff8fc4!important;color:#3a2414!important;display:grid!important;place-items:center;padding:0!important;cursor:pointer;box-shadow:0 2px 0 #3a2414!important;z-index:2}
#ovPause .pCard.sndOpen .pSndBtn{background:#d94c8c!important;color:#fff!important}
#ovPause .pVol{display:none!important}
#ovPause .pCard.sndOpen .pVol{display:block!important;margin:0!important;padding:8px 10px!important;border-radius:14px!important;border:2px solid #e1c9a6!important;background:#fff!important;box-shadow:none!important}
#ovPause .pVol .pvHead{margin-bottom:2px!important}
#ovPause .pVol .pvRow{padding:2px 0!important;font-size:13px!important}
#ovPause .pVol #pvMute{height:28px!important;font-size:12px!important;padding:0 10px!important}
@media (max-height:640px){#ovPause .pCapy{width:86px;height:86px;top:-44px;margin-left:-43px}#ovPause .pCard{padding-top:46px}}
</style>
'''
i = s.rfind('</body>'); s = s[:i] + css + s[i:]
open(dst, 'w', encoding='utf-8').write(s); print('ok')
