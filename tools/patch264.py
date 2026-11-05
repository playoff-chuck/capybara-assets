"""V264 (Martin 05.11. 14:57): Dev «Intros: on/off» entfernt – man spielt immer wie ein normaler Spieler.
Neu: Dev-Knopf «Check news» zeigt alle Neuheiten-Fenster nacheinander (alle Monster, alle Waffen/Gadgets – wo es eine
Anzeige gibt, im Sale-Stil –, Elite-Upgrades und zum Schluss Lucky Supply), ohne hinzuspielen. Spielstand bleibt
unverändert (Kaufen in der Vorschau kauft nicht, Gold/Pocket/«schon gesehen» werden zurückgesetzt).
Nochmal tippen bricht ab."""
import sys
src, dst = sys.argv[1], sys.argv[2]
s = open(src, encoding='utf-8').read()
def rep(a, b, cnt=1):
    global s
    n = s.count(a); assert n == cnt, (n, a[:70]); s = s.replace(a, b)
rep('const GAME_VER = "V263";', 'const GAME_VER = "V264";')
rep('<button id="devIntro">Intros: on</button>', '<button id="devNews">Check news</button>')
rep('function buy() { const k = cur; if (!k || why(k)) { paint(); return; }', 'function buy() { const k = cur; if (window.__newsPrev) { close(false); return; } if (!k || why(k)) { paint(); return; }')
rep('const keep = ["tarnturm-dev", "tarnturm-devnointro"];', 'const keep = ["tarnturm-dev"];')
js = r'''
  /* V264: Dev – Check news (alle Neuheiten-Fenster nacheinander, ohne Spielstand zu ändern) */
  try { (() => { try { LS.set("tarnturm-devnointro", "0"); } catch (e) {}
    const btn = document.getElementById("devNews"); if (!btn) return; let run = null;
    const vis = id => { const el = document.getElementById(id); return el && !el.hidden && getComputedStyle(el).display !== "none"; };
    function list() { const L = []; Object.keys(INTRO_MON).forEach(k => L.push({ t: "mon", k }));
      const AD = ["kan", "ton", "mix", "frost", "snipe"]; Object.keys(INTRO_GEAR).forEach(k => L.push({ t: AD.includes(k) ? "ad" : "gear", k })); L.push({ t: "bandit" }); return L; }
    function snap() { return { seen: JSON.stringify(S.seen || {}), gold: S.gold, tons: S.tons, tg: S.tonIntroGift, due: JSON.stringify(S.adDue || {}), iw: S.introWave, bd: S.banditDone, pk: ["snipes", "mixers", "teslas", "locks", "chomps"].map(k => S[k]) }; }
    function restore(z) { S.seen = JSON.parse(z.seen); S.gold = z.gold; S.tons = z.tons; S.tonIntroGift = z.tg; S.adDue = JSON.parse(z.due); S.introWave = z.iw; S.banditDone = z.bd; ["snipes", "mixers", "teslas", "locks", "chomps"].forEach((k, i) => { S[k] = z.pk[i]; }); }
    function stop(msg) { if (!run) return; clearInterval(run.iv); restore(run.z); window.__newsPrev = false; run = null; btn.textContent = "Check news"; btn.classList.remove("armed"); try { toast(msg || "NEWS · done", "DEV", 1500); } catch (e) {} }
    function open(q) { if (q.t === "ad") { S.intro = true; S.adOpen = true; window.__adLast = 0; window.__TT.ad.show(q.k, q.k !== "ton"); }
      else if (q.t === "bandit") { const b = document.getElementById("devBandit"); if (b) b.click(); }
      else showIntro({ t: q.t, k: q.k }); }
    const busy = () => vis("ovIntro") || document.body.classList.contains("introWin") || vis("ovAd") || vis("ovBandit");
    btn.addEventListener("click", e => { e.stopPropagation(); try { snd("uiTap"); } catch (er) {}
      if (run) { stop("NEWS · stopped"); return; }
      if (!S || !S.started || S.over) { try { toast("Start a game first", "DEV", 1500); } catch (er) {} return; }
      try { const db = document.getElementById("devBar"); if (db && db.classList.contains("open")) db.classList.remove("open"); } catch (er) {}
      const L = list(); run = { L, i: 0, z: snap(), wait: 0, iv: null }; window.__newsPrev = true; btn.textContent = "Stop news"; btn.classList.add("armed");
      const next = () => { if (!run) return; if (run.i >= run.L.length) { stop(); return; } restore(run.z); const q = run.L[run.i++]; try { btn.textContent = `Stop news ${run.i}/${run.L.length}`; } catch (er) {} open(q); run.wait = 0; };
      next();
      run.iv = setInterval(() => { if (!run) return; if (busy()) { run.wait = 0; return; } if (++run.wait >= 2) { S.intro = false; S.adOpen = false; next(); } }, 250);
    });
  })(); } catch (e) { console.error("devNews", e); }
'''
i = s.rfind('})();\n</script>'); s = s[:i] + js + s[i:]
open(dst, 'w', encoding='utf-8').write(s); print('ok')
