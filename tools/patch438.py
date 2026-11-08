#!/usr/bin/env python3
"""V438 (Martin 08.11. 09:25/09:26):
1. Unkraut wächst bis in die oberste Zeile (Ring) → Game over «WEEDS TOOK THE RING». Vorher zwei Warnungen (einmal je Unkrautfeld):
   General «WEED ALERT» bei 4 freien Zeilen bis zum Ring (Clip weed_warn), Blue-Sprechblase bei 2 freien Zeilen (rb_weedlast). HeyGen 9,8 s, 0,0033 $.
2. Nach dem Sieg (W150): keine «CONTINUE · WAVE 146»- und keine «Start over»-Knöpfe; stattdessen großer Knopf «TELL YOUR FRIENDS» (Einladungslink per Messenger, wie INVITE FRIENDS) + Main menu.
3. t119: W65 Blizzard + Bildausfall bleibt (Martin: gemeinsam ok)."""
import sys, json, base64, os
src, dst = sys.argv[1], sys.argv[2]
s = open(src, encoding="utf-8").read()
def rep(a, b, n=1):
    global s
    assert s.count(a) == n, (s.count(a), a[:80])
    s = s.replace(a, b)
rep('const GAME_VER = "V437";', 'const GAME_VER = "V438";')
VD = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'voice')
L = json.load(open(os.path.join(VD, 'lines12.json'), encoding='utf-8'))
vt = ''.join(f'{json.dumps(k)}: {json.dumps(t)}, ' for k, t in L.items())
vb = ''.join(f'"{k}":"' + base64.b64encode(open(os.path.join(VD, k + '.mp3'), 'rb').read()).decode() + '",' for k in L)
rep('const VOICE_TEXT = {', 'const VOICE_TEXT = {' + vt)
rep('const VOICE = {', 'const VOICE = {' + vb)
# 1. Unkraut bis zum Ring + Warnungen
rep('''        if (S.inWave) w.growT += dt; if (w.growT >= 6.8 && w.h < 12) { const ny = w.root - w.h; if (ny >= 1 && weedPush(w.x, ny, p)) { w.h++; w.growT = 0; } else w.growT = 6.8; } } }''',
'''        if (S.inWave) w.growT += dt; if (w.growT >= 6.8) { const ny = w.root - w.h; if (ny <= 0 && !S.over) { w.growT = 0; try { fxText(w.x, 1, "WEEDS TOOK THE RING", "#ff6fb5"); } catch (e) {} gameOver("Weeds reached the ring."); } else if (ny >= 1 && weedPush(w.x, ny, p)) { w.h++; w.growT = 0; } else w.growT = 6.8; }   /* V438: Spitze im Ring = Game over */
        { const left = w.root - w.h + 1;   /* freie Zeilen zwischen Spitze und Ring (Zeile 0) */
          if (left <= 2 && !D.weedW2) { D.weedW2 = true; try { window.__rbSay && window.__rbSay("rb_weedlast", true); } catch (e) {} }
          else if (left <= 4 && !D.weedW1) { D.weedW1 = true; try { snd("siren"); announce("WEED ALERT", "If it reaches the ring, it's over · Tesla or Sniper", "ALERT", 3000); setTimeout(() => SFX.say("weed_warn"), 500); } catch (e) {} } } } }''')
rep('(/ceiling/.test(why) ? "STACK TOPPED OUT" : "OVERRUN")', '(/ceiling/.test(why) ? "STACK TOPPED OUT" : /Weeds/.test(why) ? "WEEDS TOOK THE RING" : "OVERRUN")')
rep('.replace("STACK TOPPED OUT", "TOWER FULL").replace("OVERRUN", "THEY GOT THROUGH"); } catch (e) {}',
    '.replace("STACK TOPPED OUT", "TOWER FULL").replace("OVERRUN", "THEY GOT THROUGH"); } catch (e) {}\n    try { if (S && S.won) { const bc = $("btnCp"), rs = $("btnRestart"); if (bc) bc.hidden = true; if (rs) { rs.classList.add("btn-big"); rs.textContent = "TELL YOUR FRIENDS"; rs.dataset.won = "1"; } } else { const rs = $("btnRestart"); if (rs) delete rs.dataset.won; } } catch (e) {}   /* V438: nach dem Sieg nur Empfehlen + Menü */')
rep('$("btnRestart").addEventListener("click", () => showCamp(() => startGame(MODE), `${MODES[MODE].label.toUpperCase()} · GET READY`));',
    '$("btnRestart").addEventListener("click", () => { if ($("btnRestart").dataset.won) { try { SFX.init(); snd("uiTap"); sqInviteFrom($("btnRestart")); } catch (e) {} return; } showCamp(() => startGame(MODE), `${MODES[MODE].label.toUpperCase()} · GET READY`); });')
rep('''async function sqInvite() { if (sqBusy) return; sqBusy = true; sqNote("…");''',
'''async function sqInviteFrom(btn) {   /* V438: Einladung von der Siegkarte – Rückmeldung im Knopf */
  const t0 = btn.textContent; const note = t => { btn.textContent = t; setTimeout(() => { btn.textContent = t0; }, 3500); };
  if (sqBusy) return; sqBusy = true;
  try { const c = await sqMyCode(); const url = SHARE_URL + (c ? "/?squad=" + c : "/"), text = "I beat all 150 waves of Capybara Squad! Try it – you get a free Ten-ton drop.";
    if (navigator.share) { try { await navigator.share({ title: "Capybara Squad", text, url }); note("SENT!"); } catch (e) { if (!(e && e.name === "AbortError")) note("LINK: " + url.replace("https://", "")); } return; }
    try { await navigator.clipboard.writeText(text + " " + url); note("LINK COPIED!"); } catch (e) { note("LINK: " + url.replace("https://", "")); }
  } finally { sqBusy = false; } }
async function sqInvite() { if (sqBusy) return; sqBusy = true; sqNote("…");''')
rep('try { const cp = window.__cpGet(), bc = $("btnCp"); if (bc && cp >= 5 && !(S && S.nuts)) {', 'try { const cp = window.__cpGet(), bc = $("btnCp"); if (bc && cp >= 5 && !(S && S.nuts) && !(S && S.won)) {   /* V438: nicht nach dem Sieg */')
open(dst, "w", encoding="utf-8").write(s)
print("ok")
