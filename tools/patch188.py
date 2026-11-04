s=open('v187.html',encoding='utf-8').read()
def rep(a,b,cnt=1):
    global s
    n=s.count(a); assert n==cnt,(n,a[:70]); s=s.replace(a,b)
rep('ver: "V187", wave: S.wave','ver: "V188", wave: S.wave')
js=r'''
/* V188: Vollbild-Fenster sauber halten (kein General, keine Wellen-Nummer, keine Pause-Knöpfe, kein DJ) und
   während des Boss-Hacks die Hauptmusik anhalten – nur die Hack-Musik läuft */
(() => {
  const FULL = ["ovHack", "ovOver", "ovPause", "ovStart", "ovCamp", "ovInfo", "ovHs", "ovSettings", "ovAlbum", "ovJoin", "ovOrders", "ovIntro", "ovGive", "ovSpec", "ovFb", "ovNutsRes", "ovSign"];
  let hackHeld = false;
  setInterval(() => {
    const up = FULL.some(id => { const e = document.getElementById(id); return e && !e.hidden && e.getClientRects().length; });
    document.body.classList.toggle("ovUp", up);
    const hackUp = (() => { const e = document.getElementById("ovHack"); return !!(e && !e.hidden) || !!(typeof S !== "undefined" && S && S.duel); })();
    try { if (hackUp && TP.el && !TP.el.paused) { TP.el.pause(); hackHeld = true; }
      else if (!hackUp && hackHeld) { hackHeld = false; if (TP.key && !TP.paused && !document.hidden) { const p = TP.el.play(); if (p && p.catch) p.catch(() => {}); tpFade(0.5, 0.8); } } } catch (e) {}
  }, 120);
})();
'''
k=s.rfind('})();\n</script>'); assert k>0; s=s[:k]+js+s[k:]
css='''<style id="v188">
body.ovUp #genAv,body.ovUp #waveNum,body.ovUp #bPauseTop,body.ovUp #bWave,body.ovUp #hkMiss,body.ovUp #hackPill,body.ovUp header .djBox,body.ovUp #djSong,body.ovUp #coach{visibility:hidden!important;pointer-events:none!important}
</style>
'''
i=s.rfind('</body>'); s=s[:i]+css+s[i:]
open('v188.html','w',encoding='utf-8').write(s); print('ok')
