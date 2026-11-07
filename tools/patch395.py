"""V395: Ein Auszeichnungs-Icon (Martin, 07.11.): Das Pokal-Icon im Hauptmenü öffnet jetzt die Medaillen;
oben in der Karte drei Reiter MEDALS · HALL OF FAME · SQUAD, damit kommt man zu den anderen beiden.
Die Knöpfe «Medals» und «Squad» sind im Hauptmenü ausgeblendet.
Aufruf: python3 tools/patch395.py site/index.html site/index.html"""
import re, sys
src, dst = sys.argv[1], sys.argv[2]
s = open(src, encoding='utf-8').read()
def rep(a, b, cnt=1):
    global s
    n = s.count(a); assert n == cnt, (n, a[:70]); s = s.replace(a, b)
m = re.search(r'const GAME_VER = "V(\d+)";', s); old = int(m.group(1)); NEW = old + 1
rep(f'const GAME_VER = "V{old}";', f'const GAME_VER = "V{NEW}";')
rep('''#ovSquad{position:fixed;''', '''#btnAlbum,#btnSquad{display:none!important}
.awTabs{display:flex;gap:4px;margin:0 34px 8px 0}
.awTabs button{flex:1;min-width:0;padding:6px 2px;border-radius:10px;border:2px solid #3a2a1a;background:#ece0c8;color:#3a2a1a;font:400 15px/1 Bangers,system-ui;letter-spacing:.5px;box-shadow:0 2px 0 #3a2a1a}
.awTabs button.on{background:#ffd84d}
#ovHs .awTabs{margin:0 30px 8px 0}
body:has(#ovAlbum:not([hidden])):has(#albBody):has(#albX) #btnOffline,body:has(#ovAlbum:not([hidden])):has(#albBody):has(#albX) #btnMap,body:has(#ovHs:not([hidden])):has(#hsList):has(#btnHsClose) #btnOffline,body:has(#ovHs:not([hidden])):has(#hsList):has(#btnHsClose) #btnMap{display:none!important}
#ovSquad{position:fixed;''')
rep('''$("btnSquad").addEventListener("click", () => { SFX.init(); openSquad(); });''', '''$("btnSquad").addEventListener("click", () => { SFX.init(); openSquad(); });
/* V%d: ein Auszeichnungs-Icon – Pokal öffnet Medaillen, Reiter zu Hall of fame und Squad */
{ let hsOk = false; const OV = { medals: "ovAlbum", hof: "ovHs", squad: "ovSquad" }, BOX = { medals: "#ovAlbum .albBox", hof: "#ovHs .hsBox", squad: "#ovSquad .albBox" };
  const tabs = act => { for (const k in BOX) { const box = document.querySelector(BOX[k]); if (!box) continue; let t = box.querySelector(".awTabs");
      if (!t) { t = document.createElement("div"); t.className = "awTabs"; t.innerHTML = `<button data-aw="medals">MEDALS</button><button data-aw="hof">HALL OF FAME</button><button data-aw="squad">SQUAD</button>`; box.insertBefore(t, box.firstChild); }
      t.querySelectorAll("button").forEach(b => b.classList.toggle("on", b.dataset.aw === act)); } };
  const go = k => { for (const o of Object.values(OV)) { const e = $(o); if (e) e.hidden = true; } tabs(k);
    if (k === "medals") openAlbum(); else if (k === "squad") openSquad(); else { hsOk = true; $("btnHs").click(); } };
  $("btnHs").addEventListener("click", e => { if (hsOk) { hsOk = false; return; } e.stopImmediatePropagation(); SFX.init(); go("medals"); }, true);
  document.addEventListener("click", e => { const b = e.target.closest && e.target.closest(".awTabs button"); if (!b) return; e.stopPropagation(); try { snd("uiTap"); } catch (er) {} go(b.dataset.aw); }, true);
  try { $("btnHs").setAttribute("aria-label", "Awards"); $("btnHs").title = "Awards"; } catch (e) {} }''' % NEW)
open(dst, 'w', encoding='utf-8').write(s); print("ok V%d" % NEW)
