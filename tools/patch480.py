#!/usr/bin/env python3
"""V480 – Outfits neu (t139, Martin 08.11. 22:38–22:42):
- Shades gratis ab Welle 20 (beste Welle), Explorer/Winter/Champion weiter 60/90/120 ★
- 5 neue lustige Outfits nur über geworbene Freunde (1/2/3/5/8): Pop Star, Rock King, Big Boss, Pirate, Astronaut (img/outfit_<held>_5…9.webp)
- Freund zählt erst, wenn er Welle 5 erreicht (vorher: beim Öffnen des Links); Zähler lokal gespeichert (capy-squad-n), Squad File zeigt «SQUAD FRIENDS»
Nutzung: python3 tools/patch480.py src dst"""
import sys, re
src, dst = sys.argv[1], sys.argv[2]
s = open(src, encoding="utf-8").read()

def rep(a, b, n=1):
    global s
    c = s.count(a)
    assert c == n, (c, a[:80])
    s = s.replace(a, b)

m = re.search(r'const GAME_VER = "V(\d+)";', s); v = int(m.group(1))
rep(m.group(0), f'const GAME_VER = "V{v + 1}";')

rep('const OUTFIT = [["Standard", 0], ["Shades", 30], ["Explorer", 60], ["Winter", 90], ["Champion", 120]];   /* V413: Name, Sterne */',
    'const OUTFIT = [["Standard", 0], ["Shades", { w: 20 }], ["Explorer", 60], ["Winter", 90], ["Champion", 120], ["Pop Star", { f: 1 }], ["Rock King", { f: 2 }], ["Big Boss", { f: 3 }], ["Pirate", { f: 5 }], ["Astronaut", { f: 8 }]];   /* V413: Name, Sterne · V480: {w} = ab Welle, {f} = geworbene Freunde */\n'
    'function outfitNeed(o) { const r = o[1]; return typeof r === "number" ? { s: r } : r; }\n'
    'function sqFriends() { try { return +localStorage.getItem("capy-squad-n") || 0; } catch (e) { return 0; } }\n'
    'function outfitOn(o, stars) { const n = outfitNeed(o); if (n.s != null) return stars >= n.s; if (n.w != null) return getBest("pro") >= n.w; return sqFriends() >= n.f; }\n'
    'function outfitLabel(o) { const n = outfitNeed(o); if (n.s != null) return n.s + " ★"; if (n.w != null) return "wave " + n.w; return n.f === 1 ? "1 friend" : n.f + " friends"; }')
rep('function outfitSel(k) { try { const n = +localStorage.getItem("capy-outfit-" + k) || 0; return n >= 0 && n <= 4 ? n : 0; } catch (e) { return 0; } }',
    'function outfitSel(k) { try { const n = +localStorage.getItem("capy-outfit-" + k) || 0; return n >= 0 && n < OUTFIT.length ? n : 0; } catch (e) { return 0; } }')
rep('''h += `<div class="albSec">${k.toUpperCase()}'S OUTFITS<span>${OUTFIT.filter(o => stars >= o[1]).length} / 5</span></div><div class="ofRow">` + OUTFIT.map((o, n) => { const on = stars >= o[1];''',
    '''h += `<div class="albSec">${k.toUpperCase()}'S OUTFITS<span>${OUTFIT.filter(o => outfitOn(o, stars)).length} / ${OUTFIT.length}</span></div><div class="ofRow">` + OUTFIT.map((o, n) => { const on = outfitOn(o, stars);''')
rep('''<small>${on ? (n === sel ? "wearing" : "tap to wear") : o[1] + " ★"}</small></div>`; }).join("") + `</div>`; }
  return h; }''',
    '''<small>${on ? (n === sel ? "wearing" : "tap to wear") : outfitLabel(o)}</small></div>`; }).join("") + `</div>`; }
  { const fn = sqFriends(), nx = OUTFIT.map(outfitNeed).filter(n => n.f != null && n.f > fn).map(n => n.f).sort((a, b) => a - b)[0];   /* V480: Freunde-Zähler + nächstes Outfit */
    h += `<div class="albSec">SQUAD FRIENDS<span>${fn}</span></div><div class="sqNote">${nx ? `Friends who reach wave 5 with your link unlock outfits · next at ${nx}` : "All friend outfits unlocked!"}</div>`; setTimeout(sqRefresh, 0); }
  return h; }''')
# Zähler-Abfrage speichert n; Squad File neu zeichnen, wenn sich n ändert
rep('''const d = await r.json(); const n = d && d.n | 0; if (!sqBusy) sqNote(''',
    '''const d = await r.json(); const n = d && d.n | 0; sqStoreN(n); if (!sqBusy) sqNote(''')
rep('''let sqBusy = false, sqCntT = -1e9;''',
    '''let sqBusy = false, sqCntT = -1e9, sqRefT = -1e9;
function sqStoreN(n) { try { const old = +localStorage.getItem("capy-squad-n") || 0; if (n !== old) { localStorage.setItem("capy-squad-n", n); const o = $("ovSquad"); if (o && !o.hidden) openSquad(); } } catch (e) {} }   /* V480 */
async function sqRefresh() { const c = LS.get("capy-squad-code"); if (!c || !SQ_RE.test(c) || performance.now() - sqRefT < 20000) return; sqRefT = performance.now();
  try { const r = await fetch(API_BASE + "/squad?code=" + c, { cache: "no-store" }); if (!r.ok) return; const d = await r.json(); sqStoreN(d && d.n | 0); } catch (e) {} }   /* V480: Freunde-Zähler fürs Squad File */''')
# Freund zählt erst ab Welle 5 (nicht beim Öffnen des Links); Geschenk bleibt ab W2
rep('''  LS.set("capy-squad-from", c);
  sqPost("/squad/join", { code: c }).then(r => { if (r.ok) LS.set("capy-squad-gift", "1"); }).catch(() => {}); } catch (e) {} })();''',
    '''  LS.set("capy-squad-from", c); LS.set("capy-squad-gift", "1"); LS.set("capy-squad-pend", c); } catch (e) {} })();   /* V480: zählen erst ab Welle 5 (s. u.) */
setInterval(() => { try { const c = LS.get("capy-squad-pend"); if (!c || !SQ_RE.test(c) || !S || !S.started || S.over || S.nuts || S.replay || S.testRun || (S.wave || 0) < 5) return;
  LS.del("capy-squad-pend"); sqPost("/squad/join", { code: c }).catch(() => {}); } catch (e) {} }, 4000);   /* V480: der Freund zählt, sobald er Welle 5 erreicht */''')
rep('.albSec{margin:10px 0 4px;font-family:Bangers,system-ui;font-size:18px;letter-spacing:.5px;display:flex;justify-content:space-between}',
    '.albSec{margin:10px 0 4px;font-family:Bangers,system-ui;font-size:18px;letter-spacing:.5px;display:flex;justify-content:space-between}.sqNote{font-size:12px;opacity:.8;margin:0 0 6px}')
open(dst, "w", encoding="utf-8").write(s); print("ok", v + 1)
