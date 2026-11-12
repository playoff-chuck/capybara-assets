#!/usr/bin/env python3
# V656 (Martin 12.11. 11:53/11:58): Admin – Kasten «GOOGLE PLAY» mit Knopf «Schlüssel hochladen (JSON)».
# Die Datei geht direkt an den Server (/admin/secret), nie über den Chat. Danach zeigt der Kasten die Dienstkonto-E-Mail,
# die Martin in der Play Console unter «Nutzer und Berechtigungen» einlädt. Claude lädt dann App-Versionen selbst hoch.
import sys, os
site = sys.argv[1]; p = os.path.join(site, "index.html"); s = open(p, encoding="utf-8").read()
def rep(a, b, n=1):
    global s
    c = s.count(a); assert c == n, (c, a[:90]); s = s.replace(a, b)
rep('const GAME_VER = "V655";', 'const GAME_VER = "V656";')
rep('<button type="button" data-act="get">Herunter&shy;laden (CSV)</button></div></div>`;   /* V653 */',
    '<button type="button" data-act="get">Herunter&shy;laden (CSV)</button></div></div>'
    '<div class="aRep"><b>GOOGLE PLAY · AUTOMATISCHE RELEASES</b><small id="aKeySt">Dienstkonto-Schlüssel (JSON-Datei aus Google Cloud) hier hochladen – er geht direkt an den Server, nicht in den Chat.</small>'
    '<div class="aRepB" style="grid-template-columns:1fr"><button type="button" data-act="key">🔑 Schlüssel hochladen (JSON)</button></div><input type="file" id="aKeyF" accept=".json,application/json" hidden></div>`;   /* V653 · V656 */')
rep('  body.addEventListener("click", e => { const rb = e.target.closest(".aRepB button"); if (rb) { try { snd("uiTap"); } catch (er) {} repCall(rb.dataset.act); return; }   /* V653 */',
    '''  body.addEventListener("change", async e => { if (e.target.id !== "aKeyF") return; const f = e.target.files && e.target.files[0]; const st = document.getElementById("aKeySt"); if (!f || !st) return;   /* V656 */
    st.textContent = "Lade hoch …"; try { const k = JSON.parse(await f.text()); const r = await fetch(API_BASE + "/admin/secret", { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify({ token: tokenGet(), key: k }), cache: "no-store" }); const j = await r.json();
      st.innerHTML = j.ok ? `<span style="color:#1f7a3a;font-weight:700">Gespeichert ✓</span><br>Jetzt in der Play Console unter «Nutzer und Berechtigungen» diese Adresse einladen:<br><b style="user-select:all;word-break:break-all">${esc(j.email)}</b>` : `<span style="color:#b3261e;font-weight:700">${esc(j.error || "Fehler")}</span>`; }
    catch (er) { st.innerHTML = '<span style="color:#b3261e;font-weight:700">Das ist keine gültige JSON-Datei.</span>'; } e.target.value = ""; });
  body.addEventListener("click", e => { const rb = e.target.closest(".aRepB button"); if (rb) { try { snd("uiTap"); } catch (er) {} if (rb.dataset.act === "key") { const fi = document.getElementById("aKeyF"); if (fi) fi.click(); return; } repCall(rb.dataset.act); return; }   /* V653 · V656 */''')
open(p, "w", encoding="utf-8").write(s)
print("ok V656")
