#!/usr/bin/env python3
# V419 (t14 Teil 2, Martin 07.11. 18:20): Freunde einladen.
# Settings → «INVITE FRIENDS»: eigener Squad-Code vom Server (capy-api /squad, nur Zähler), Link playcapybarasquad.com/?squad=CODE
# über System-Teilen (sonst kopieren). Zeile darunter: «SQUAD +n · friends joined with your link».
# Wer über den Link kommt: einmal je Gerät Zähler +1, ab Welle 2 blaue Air-Drop-Karte «A GIFT FROM A FRIEND» + 1 Ten-ton.
import sys
src, dst = sys.argv[1], sys.argv[2]
s = open(src, encoding="utf-8").read()
def rep(a, b, n=1):
    global s
    assert s.count(a) == n, (s.count(a), a[:80])
    s = s.replace(a, b)

rep('const GAME_VER = "V418";', 'const GAME_VER = "V419";')

rep('''<button id="setCloud" class="btn-small" type="button">☁ Cloud save</button><button id="setGuide" class="btn-small" type="button">Guide</button></div>''',
    '''<button id="setCloud" class="btn-small" type="button">☁ Cloud save</button><button id="setGuide" class="btn-small" type="button">Guide</button></div><div class="setInv"><button id="setInvite" class="shareBtn" type="button">INVITE FRIENDS</button><small id="setInvN">Friends get a free Ten-ton drop</small></div>''')

rep('''ton: { img: "img/ad_drop_free.webp", name: "TEN-TON DROP", line: "HQ sent you a Ten-ton drop. It's already in your Pocket.", met: ["+1 Ten-ton", "In your Pocket"], btn: "THANKS! ▶" },''',
    '''ton: { img: "img/ad_drop_free.webp", name: "TEN-TON DROP", line: "HQ sent you a Ten-ton drop. It's already in your Pocket.", met: ["+1 Ten-ton", "In your Pocket"], btn: "THANKS! ▶" },
                 friend: { img: "img/ad_drop_free.webp", name: "A GIFT FROM A FRIEND", line: "A friend invited you to the squad and sent a Ten-ton drop. It's already in your Pocket.", met: ["+1 Ten-ton", "In your Pocket"], btn: "THANKS! ▶" },   /* V419 */''')
rep('''const vl = { ton: "ad_drop", sweep: "ad_sweep", med: "ad_med", rot: "ad_upright" }[kind];''',
    '''const vl = { ton: "ad_drop", friend: "ad_drop", sweep: "ad_sweep", med: "ad_med", rot: "ad_upright" }[kind];''')
rep('''if (kind === "sweep" || kind === "ton") [0.5, 0.8]''', '''if (kind === "sweep" || kind === "ton" || kind === "friend") [0.5, 0.8]''')

rep('''window.__shareCard = o => shareCard(o); window.__shareInfo = o => shInfo(o);''',
    '''window.__shareCard = o => shareCard(o); window.__shareInfo = o => shInfo(o);
/* V419 (t14): Freunde einladen – Squad-Code, Zähler auf unserem Server, Geschenk für Eingeladene */
const SQ_RE = /^[ABCDEFGHJKMNPQRSTUVWXYZ2-9]{6}$/;
function sqPost(path, body) { return fetch(API_BASE + path, { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify(body || {}) }); }
async function sqMyCode() { const c = LS.get("capy-squad-code"); if (c && SQ_RE.test(c)) return c;
  try { const r = await sqPost("/squad"); if (!r.ok) return null; const d = await r.json(); if (d && SQ_RE.test(d.code || "")) { LS.set("capy-squad-code", d.code); return d.code; } } catch (e) {} return null; }
function sqNote(t) { const el = $("setInvN"); if (el) el.textContent = t; }
let sqBusy = false, sqCntT = -1e9;
async function sqInvite() { if (sqBusy) return; sqBusy = true; sqNote("…");
  try { const c = await sqMyCode(); if (!c) { sqNote("No connection · please try again later"); return; }
    const url = SHARE_URL + "/?squad=" + c, text = "Join my squad in Capybara Squad! You get a free Ten-ton drop.";
    if (navigator.share) { try { await navigator.share({ title: "Capybara Squad", text, url }); sqNote(`Your squad code: ${c}`); } catch (e) { sqNote(e && e.name === "AbortError" ? `Your squad code: ${c}` : `Your link: ${url.replace("https://", "")}`); } return; }
    try { await navigator.clipboard.writeText(text + " " + url); sqNote("Link copied! Send it to your friends."); } catch (e) { sqNote(`Your link: ${url.replace("https://", "")}`); }
  } finally { sqBusy = false; } }
async function sqCount() { const c = LS.get("capy-squad-code"); if (!c || !SQ_RE.test(c) || performance.now() - sqCntT < 30000) return; sqCntT = performance.now();
  try { const r = await fetch(API_BASE + "/squad?code=" + c, { cache: "no-store" }); if (!r.ok) return; const d = await r.json(); const n = d && d.n | 0; if (!sqBusy) sqNote(n > 0 ? `SQUAD +${n} · ${n === 1 ? "friend" : "friends"} joined with your link` : "Friends get a free Ten-ton drop"); } catch (e) {} }
document.addEventListener("click", e => { if (e.target.closest("#setInvite")) { try { SFX.init(); snd("uiTap"); } catch (er) {} sqInvite(); return; }
  setTimeout(() => { const o = $("ovSettings"); if (o && !o.hidden) sqCount(); }, 80); });
(() => { try { const q = new URLSearchParams(location.search), c = (q.get("squad") || "").toUpperCase();
  if (!c) return; q.delete("squad"); try { history.replaceState(null, "", location.pathname + (q.toString() ? "?" + q : "") + location.hash); } catch (e) {}
  if (!SQ_RE.test(c) || LS.get("capy-squad-from") || c === LS.get("capy-squad-code")) return;
  LS.set("capy-squad-from", c);
  sqPost("/squad/join", { code: c }).then(r => { if (r.ok) LS.set("capy-squad-gift", "1"); }).catch(() => {}); } catch (e) {} })();
setInterval(() => { try { if (LS.get("capy-squad-gift") !== "1" || !S || !S.started || S.over || S.nuts || S.replay || S.testRun || (S.wave || 0) < 2 || !window.__dropAd) return;
  LS.del("capy-squad-gift"); S.tons = (S.tons || 0) + 1; window.__dropAd("friend"); } catch (e) {} }, 2000);''')

rep('''#rpRes .rpShare{margin:6px auto 0!important;height:40px!important;font-size:20px!important;padding:0 20px!important}
</style>''', '''#rpRes .rpShare{margin:6px auto 0!important;height:40px!important;font-size:20px!important;padding:0 20px!important}
/* V419: Einladen */
#ovSettings .setInv{display:flex;flex-direction:column;align-items:center;gap:6px;margin-top:10px}
#ovSettings .setInv .shareBtn{margin:0!important;height:38px!important;font-size:18px!important;padding:0 18px!important}
#ovSettings .setInv small{font-size:12px;font-weight:700;color:#9b7a5c;text-align:center;line-height:1.25}
</style>''')

open(dst, "w", encoding="utf-8").write(s)
print("ok")
