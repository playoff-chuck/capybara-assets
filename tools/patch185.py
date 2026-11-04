s=open('v184.html',encoding='utf-8').read()
def rep(a,b,cnt=1):
    global s
    n=s.count(a); assert n==cnt,(n,a[:70]); s=s.replace(a,b)
rep('ver: "V184", wave: S.wave','ver: "V185", wave: S.wave')
js=r'''
/* V185: immer nur EIN Musikstück – Hintergrund-Tabs/-Fenster schweigen, andere offene Spiel-Fenster werden stumm */
(() => {
  const ID = Math.random().toString(36).slice(2); let hiddenMute = false, otherMute = false;
  const allAudio = () => [TP.el].filter(Boolean);
  const hush = on => { try { allAudio().forEach(a => { if (on) { a.dataset.wasPlaying = a.paused ? "0" : "1"; a.pause(); } else if (a.dataset.wasPlaying === "1" && TP.key && !TP.paused) { const p = a.play(); if (p && p.catch) p.catch(() => {}); } }); } catch (e) {}
    try { const ac = SFX._ac && SFX._ac(); if (ac) { if (on && ac.state === "running") ac.suspend(); else if (!on && ac.state === "suspended") ac.resume(); } } catch (e) {} };
  const apply = () => hush(hiddenMute || otherMute);
  document.addEventListener("visibilitychange", () => { hiddenMute = document.hidden; apply(); if (!document.hidden) announce(); });
  addEventListener("pagehide", () => { hiddenMute = true; apply(); });
  let bc = null; try { bc = new BroadcastChannel("capy-music"); } catch (e) {}
  const announce = () => { try { bc && bc.postMessage({ id: ID, t: Date.now() }); } catch (e) {} otherMute = false; apply(); };
  if (bc) bc.onmessage = e => { if (e.data && e.data.id !== ID) { otherMute = true; apply(); } };
  addEventListener("pointerdown", () => { if (otherMute) announce(); }, { capture: true, passive: true });
  announce();
})();
'''
k=s.rfind('})();\n</script>'); assert k>0; s=s[:k]+js+s[k:]
open('v185.html','w',encoding='utf-8').write(s); print('ok')
