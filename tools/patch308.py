"""V308: Flugzeug-Knopf legt auf Android das App-Icon auf den Handy-Startbildschirm (Martin 06.11. 07:07:
«im Menü soll bei Flugzeugmodus icon am Handydesktop für Android erstellt werden»).
Bisher wurde die Installations-Abfrage nur genutzt, wenn Chrome sie beim Tippen schon geliefert hatte, und danach
verworfen. Jetzt:
- Tippen auf ✈ speichert offline UND fragt «Zum Startbildschirm hinzufügen» (Android-Chrome-Abfrage).
- Kam die Abfrage erst später, bekommt der fertige Knopf ein rosa 📲-Zeichen; nächstes Tippen legt das Icon an.
- Gibt der Browser keine Abfrage her (z. B. Samsung-Browser, Firefox): Hinweis «Browser-Menü ⋮ → Add to Home screen».
- Schon installiert (App-Fenster oder appinstalled) → keine Abfrage, kein Hinweis mehr."""
import sys
src, dst = sys.argv[1], sys.argv[2]
s = open(src, encoding='utf-8').read()
def rep(a, b, cnt=1):
    global s
    n = s.count(a); assert n == cnt, (n, a[:70]); s = s.replace(a, b)

rep('const GAME_VER = "V307";', 'const GAME_VER = "V308";')

# Zustand «installiert» + Knopf-Zeichnung mit 📲-Zeichen, solange das Icon noch fehlt und Chrome es anbietet
rep('''    const draw = (pct) => { b.classList.toggle("ok", state === "ready"); b.innerHTML = state === "busy" ? `<b>${pct || 0}%</b>` + PLANE.replace('class="pl"', 'class="pl fly"') : PLANE + (state === "ready" ? '<i class="okDot"></i>' : ''); };''',
    '''    const andr = /Android/i.test(navigator.userAgent), isInst = () => LS.get("capy-installed") === "1" || matchMedia("(display-mode: standalone)").matches || !!navigator.standalone;
    const draw = (pct) => { b.classList.toggle("ok", state === "ready"); const ic = state === "ready" && prompt && !isInst();
      b.innerHTML = state === "busy" ? `<b>${pct || 0}%</b>` + PLANE.replace('class="pl"', 'class="pl fly"') : PLANE + (state === "ready" ? (ic ? '<i class="icDot">📲</i>' : '<i class="okDot"></i>') : ''); };''')

rep('''    addEventListener("beforeinstallprompt", e => { e.preventDefault(); prompt = e; });''',
    '''    addEventListener("beforeinstallprompt", e => { e.preventDefault(); prompt = e; if (state !== "busy") draw(); });
    addEventListener("appinstalled", () => { LS.set("capy-installed", "1"); prompt = null; if (state !== "busy") draw(); toast("Icon added to your home screen!", "OFFLINE", 2600); });
    const askIcon = () => { if (isInst()) return false;
      if (prompt) { const p = prompt; prompt = null; try { p.prompt(); p.userChoice.then(c => { if (c && c.outcome === "accepted") LS.set("capy-installed", "1"); draw(); }).catch(() => {}); } catch (e) {} return true; }
      if (andr) { toast("Home-screen icon: browser menu ⋮ → Add to Home screen", "OFFLINE", 3600); return true; }
      return false; };''')

# Fertig geladen: Hinweis aufs Icon, falls noch nicht da
rep('''        toast(ios && !standalone ? "Saved! Tip: Share → Add to Home Screen" : "Saved! Works in flight mode now.", "OFFLINE", 3200); } });''',
    '''        toast(ios && !standalone ? "Saved! Tip: Share → Add to Home Screen" : prompt && !isInst() ? "Saved! Tap ✈ again for the home-screen icon" : "Saved! Works in flight mode now.", "OFFLINE", 3200); } });''')

# Tippen im fertigen Zustand: Icon anlegen (oder Hinweis), sonst wie bisher
rep('''      if (state === "ready") { toast(navigator.onLine ? "All saved · plays in flight mode" : "Offline mode · leaderboard waits for signal", "OFFLINE", 2400); if (prompt) { prompt.prompt(); prompt = null; } return; }''',
    '''      if (state === "ready") { if (!askIcon()) toast(navigator.onLine ? "All saved · plays in flight mode" : "Offline mode · leaderboard waits for signal", "OFFLINE", 2400); return; }''')

# Erstes Tippen: Abfrage sofort (Fingertipp nötig), Laden läuft parallel
rep('''      if (prompt) { try { prompt.prompt(); } catch (e) {} prompt = null; }
      const r = await navigator.serviceWorker.ready;''',
    '''      if (prompt && !isInst()) askIcon();
      const r = await navigator.serviceWorker.ready;''')

# CSS für das 📲-Zeichen
rep('#btnOffline .okDot{position:absolute;',
    '#btnOffline .icDot{position:absolute;right:-4px;bottom:-4px;width:24px;height:24px;border-radius:50%;background:#ff6fb5;border:2px solid #3a2414;box-sizing:border-box;font:normal 13px/20px sans-serif;text-align:center;font-style:normal;animation:icPulse 1.6s ease-in-out infinite}\n@keyframes icPulse{0%,100%{transform:scale(1)}50%{transform:scale(1.12)}}\n#btnOffline .okDot{position:absolute;')

open(dst, 'w', encoding='utf-8').write(s)
print("ok")
