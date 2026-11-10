#!/usr/bin/env python3
# V579 (Martin 11.11. 00:53–00:55): Musik leicht wieder einschalten + Flugzeug wie früher
# - Flugzeug auf der Karte: genau wie vor V571 (Film und Ton starten zusammen, kein Vorlauf) – V571/V572/V576-Änderungen zurück
# - Ist die Musik stumm (Musik aus, Ton aus, Lautstärke 0 oder Musik-Regler 0), trägt der DJ oben rechts
#   ein rotes 🔇-Schild, das kurz wippt
# - Ein Tipp auf den DJ schaltet dann alles Nötige wieder ein (Musik, Ton, Lautstärke, Musik-Regler) und startet die Musik
#   (im Menü schaltet der DJ dann nicht mehr versehentlich aus)
import sys
src, dst = sys.argv[1], sys.argv[2]
s = open(src, encoding="utf-8").read()
def rep(a, b, n=1):
    global s
    c = s.count(a); assert c == n, (c, a[:90]); s = s.replace(a, b)
rep('const GAME_VER = "V578";', 'const GAME_VER = "V579";')

rep('/* V322: sichtbarer CANCEL-Knopf beim Platzieren eines Turms */\n',
'''/* V579: Musik stumm → 🔇 am DJ, Tipp schaltet alles wieder ein */
try { (() => { const dj = document.getElementById("dj"), box = dj && dj.closest(".djBox"); if (!dj || !box) return;
  const st = document.createElement("style"); st.textContent = `.djBox{position:relative}#musOff{position:absolute;right:8px;top:4px;z-index:5;width:28px;height:28px;border-radius:50%;background:#d9483b;border:2px solid #3a2414;box-shadow:0 2px 0 #3a2414;display:flex;align-items:center;justify-content:center;font-size:15px;line-height:1;pointer-events:none;animation:musOffWob 2.4s ease-in-out infinite}#musOff[hidden]{display:none}@keyframes musOffWob{0%,80%,100%{transform:rotate(0) scale(1)}86%{transform:rotate(-14deg) scale(1.15)}93%{transform:rotate(12deg) scale(1.15)}}`; document.head.appendChild(st);
  const b = document.createElement("div"); b.id = "musOff"; b.textContent = "🔇"; b.hidden = true; box.appendChild(b);
  const silent = () => { try { return !SFX.music.on || SFX.muted || SFX.vol === 0 || SFX.ch("m") < 0.05; } catch (e) { return false; } };
  setInterval(() => { const on = silent(); if (b.hidden === on) b.hidden = !on; }, 500);
  dj.addEventListener("click", ev => { if (!silent()) return; ev.stopImmediatePropagation(); ev.stopPropagation();
    try { SFX.init(); if (SFX.muted) SFX.toggle(); if (!(SFX.vol > 0)) SFX.setVol(0.3); if (SFX.ch("m") < 0.05) SFX.setCh("m", 0.8); if (!SFX.music.on) SFX.music.toggle(); try { musicLabel(); } catch (e) {} try { muteLabel(); } catch (e) {}
      const inGame = S && S.started && !S.over && ["ovStart", "ovCamp", "ovOver", "ovInfo", "ovHs"].every(id => $(id).hidden);
      if (inGame) { TP.key = null; SFX.music.start(S.wave); } else SFX.music.menu();
      b.hidden = true; snd("uiTap"); toast("MUSIC ON", "SOUND"); } catch (e) {} }, true);
})(); } catch (e) { console.error("v579 musoff", e); }
/* V322: sichtbarer CANCEL-Knopf beim Platzieren eines Turms */
''')

# Flugzeug: Stand vor V571 wiederherstellen
rep('function flyPlane(a, b, ms, nod) { const PL = (() => { const off = a[0] > 1 || a[0] < 0; if (!off || b[0] === a[0]) return { off, pre: 0, dl: 0 }; const bx = a[0] > 1 ? 1 : 0, ee = Math.max(0, Math.min(1, (bx - a[0]) / (b[0] - a[0]))), dl = Math.acos(1 - 2 * ee) / Math.PI * ms; return { off, dl, pre: 1500 }; })();   /* V572: Motor 1,5 s vor dem Flugzeug */\n      const arc = Math.min(a[1], b[1]) < 0.3 ? -.05 : .12, t0 = performance.now() + PL.pre,',
    'function flyPlane(a, b, ms, nod) { const arc = Math.min(a[1], b[1]) < 0.3 ? -.05 : .12, t0 = performance.now(),')
rep('const step = now => { if (mode !== "auto") return; const t = Math.max(0, Math.min(1, (now - t0) / ms)),', 'const step = now => { if (mode !== "auto") return; const t = Math.min(1, (now - t0) / ms),')
rep("""      step(performance.now()); try { const sAt = 0;
        setTimeout(() => { try { window.__planeSnd && window.__planeSnd(ms + PL.pre - sAt, PL.off); } catch (e) {} }, sAt); } catch (e) {} }""",
    "      step(t0); try { window.__planeSnd && window.__planeSnd(ms, a[0] > 1 || a[0] < 0); } catch (e) {} }")

open(dst, "w", encoding="utf-8").write(s)
print("ok V579")
