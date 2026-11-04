"""V195: Rufzeichen-Filter im Spiel (Server prüft /api/callsign: Beleidigungen, echte Namen, Kontaktdaten)."""
import sys
src, dst = sys.argv[1], sys.argv[2]
s = open(src, encoding='utf-8').read()
def rep(a, b, cnt=1):
    global s
    n = s.count(a); assert n == cnt, (n, a[:70]); s = s.replace(a, b)

rep('const GAME_VER = "V194";', 'const GAME_VER = "V195";')
helper = '''const NICK_WHY = { realname: "Please pick a made-up call sign \\u2013 no real names.", rude: "That call sign isn't allowed. Try another one.", contact: "No phone numbers, e-mails or links, please." };
async function nickCheck(n) { try { const ac = new AbortController(); const tm = setTimeout(() => ac.abort(), 2500); const r = await fetch(API_BASE + "/callsign?name=" + encodeURIComponent(n), { cache: "no-store", signal: ac.signal }); clearTimeout(tm); if (!r.ok) return null; const d = await r.json(); return d && d.ok === false ? (d.why || "rude") : null; } catch (e) { return null; } }
function nickErr(input, why) { const host = input.closest(".joinNickRow") || input; let el = host.nextElementSibling && host.nextElementSibling.classList.contains("nickErr") ? host.nextElementSibling : null; if (!el) { el = document.createElement("div"); el.className = "nickErr"; host.insertAdjacentElement("afterend", el); }
  el.textContent = why ? (NICK_WHY[why] || NICK_WHY.rude) : ""; el.hidden = !why; if (why) { input.focus(); try { input.select(); } catch (e) {} snd("nope"); } }
'''
rep('async function finishJoin(useName) {', helper + 'async function finishJoin(useName) {')
rep('  let n = useName ? cleanNick($("joinNick").value) : "";',
    '  let n = useName ? cleanNick($("joinNick").value) : "";\n  if (n.length >= 2) { const why = await nickCheck(n); nickErr($("joinNick"), why); if (why) return; }')
rep('$("setX").addEventListener("click", () => { const n = cleanNick($("setNick").value); if (n.length >= 2) LS.set("tarnturm-nick", n);',
    '$("setX").addEventListener("click", async () => { const n = cleanNick($("setNick").value); if (n.length >= 2) { const why = await nickCheck(n); nickErr($("setNick"), why); if (why) return; LS.set("tarnturm-nick", n); }')
css = '''<style id="v195">
.nickErr{margin:6px 0 0;padding:5px 8px;border-radius:8px;background:#ffe1e1;border:2px solid #b8402c;color:#7a1f12;font:700 12.5px/1.25 "Baloo 2",sans-serif;text-align:left}
</style>
'''
i = s.rfind('</body>'); s = s[:i] + css + s[i:]
open(dst, 'w', encoding='utf-8').write(s); print('ok')
