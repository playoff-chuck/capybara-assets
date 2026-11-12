#!/usr/bin/env python3
# V653 (Martin 12.11. 11:06/11:07): Admin-Knopf gut sichtbar rechts oben (unter dem Ton-Knopf, orange, «ADMIN»);
# in der Admin-Liste oben Kasten «SPIELER-TABELLE»: Stand, «Jetzt aktualisieren», «Auf Google Drive», «Herunterladen (CSV)».
# Server baut die Tabelle stündlich je Kalenderwoche neu (reports/JJJJ-KWnn/spieler.csv + sitzungen.csv), alte Wochen bleiben.
import sys, os
site = sys.argv[1]; p = os.path.join(site, "index.html"); s = open(p, encoding="utf-8").read()
def rep(a, b, n=1):
    global s
    c = s.count(a); assert c == n, (c, a[:90]); s = s.replace(a, b)
rep('const GAME_VER = "V652";', 'const GAME_VER = "V653";')
rep('#stAdm svg{width:24px;height:24px}',
    '#stAdm svg{width:24px;height:24px}\n'
    '#stAdm{top:calc(env(safe-area-inset-top,0px) + 72px)!important;right:calc(env(safe-area-inset-right,0px) + 12px)!important;width:52px!important;height:52px!important;background:#ff8a2b!important;color:#fff!important;z-index:61!important;flex-direction:column;gap:0}'
    '#stAdm svg{width:22px;height:22px}#stAdm svg circle,#stAdm svg path{fill:#fff}#stAdm em{font:800 9px/1 system-ui,sans-serif;font-style:normal;letter-spacing:.06em;margin-top:1px}   /* V653 */\n'
    '#ovAdm .aRep{background:#fffaf0;border:2px solid #3a2414;border-radius:14px;padding:10px 12px;margin:0 0 10px;box-shadow:0 2px 0 #3a2414}'
    '#ovAdm .aRep b{display:block;font:400 17px/1 Bangers,Oswald,system-ui;letter-spacing:.05em;color:#8a5a2b}#ovAdm .aRep small{display:block;margin:4px 0 8px;font:500 13px/1.35 "Baloo 2",system-ui;color:#6b4a2b}'
    '#ovAdm .aRepB{display:grid;grid-template-columns:1fr 1fr 1fr;gap:6px}#ovAdm .aRepB button{min-height:44px;padding:4px 6px;border:2px solid #3a2414;border-radius:10px;background:#fff6e3;color:#3a2414;font:700 13px/1.15 "Baloo 2",system-ui}'
    '#ovAdm .aRepB button[data-act=drive]{background:#d9ecff}#ovAdm .aRepB button:disabled{opacity:.5}')
rep('<path d="M14.6 13.4c.7-.3 1.5-.4 2.4-.4 2.9 0 4.9 2 4.9 5h-5.2c0-1.8-.8-3.4-2.1-4.6z" fill="#8a5a2b"/></svg>\';',
    '<path d="M14.6 13.4c.7-.3 1.5-.4 2.4-.4 2.9 0 4.9 2 4.9 5h-5.2c0-1.8-.8-3.4-2.1-4.6z" fill="#8a5a2b"/></svg><em>ADMIN</em>\';')
rep('    let h = `<button type="button" class="aStat"',
    '    let h = `<div class="aRep"><b>SPIELER-TABELLE</b><small id="aRepSt">Stand wird geladen …</small><div class="aRepB"><button type="button" data-act="refresh">↻ Jetzt aktualisieren</button><button type="button" data-act="drive">Auf Google Drive</button><button type="button" data-act="get">Herunter&shy;laden (CSV)</button></div></div>`;   /* V653 */\n'
    '    setTimeout(() => repCall("status"), 0);\n'
    '    h += `<button type="button" class="aStat"')
rep('  function renderList() { back.hidden = true;',
    '''  function repShow(st, note) { const el = document.getElementById("aRepSt"); if (!el) return; const L = st && st.last, D = st && st.drive;   /* V653 */
    el.innerHTML = (note ? `<span style="color:#1f7a3a;font-weight:700">${esc(note)}</span><br>` : "") + (L ? `Woche ${esc(L.week)} · Stand ${esc(L.msk)} MSK · ${L.players} Spieler · ${L.plays} Sitzungen. Wird stündlich neu gebaut, jede Woche eine neue Tabelle.` : "Noch keine Tabelle gebaut.")
      + (D ? `<br>Google Drive: ${D.done ? "zuletzt hochgeladen " + esc(D.doneMsk || "") : "Auftrag vom " + esc(D.msk) + " MSK – Claude lädt innerhalb einer Stunde hoch."}` : "")
      + (st && st.weeks && st.weeks.length > 1 ? `<br>Frühere Wochen: ${st.weeks.slice(1).map(esc).join(", ")}` : ""); }
  async function repCall(act) { const tok = tokenGet(); if (!tok) return; const bs = body.querySelectorAll(".aRepB button"); bs.forEach(b => b.disabled = true);
    try { const r = await fetch(API_BASE + "/admin/report", { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify({ token: tok, act }), cache: "no-store" }); const j = await r.json();
      if (act === "get") { if (j.csv) { const a = document.createElement("a"); a.href = URL.createObjectURL(new Blob(["\\ufeff" + j.csv], { type: "text/csv;charset=utf-8" })); a.download = `Capybara_Spieler_${j.week}.csv`; document.body.appendChild(a); a.click(); setTimeout(() => { URL.revokeObjectURL(a.href); a.remove(); }, 2000); repShow(null, "Datei geladen: Capybara_Spieler_" + j.week + ".csv"); repCall("status"); return; } repShow(null, "Noch keine Tabelle – erst «Jetzt aktualisieren»."); }
      else repShow(j.st, act === "refresh" ? "Aktualisiert." : act === "drive" ? "Auftrag an Claude: Tabelle kommt in deinen Google-Drive-Ordner «Capybara»." : ""); }
    catch (e) { repShow(null, "Keine Verbindung zum Server."); } finally { bs.forEach(b => b.disabled = false); } }
  function renderList() { back.hidden = true;''')
rep('  body.addEventListener("click", e => { const st = e.target.closest(".aStat");',
    '  body.addEventListener("click", e => { const rb = e.target.closest(".aRepB button"); if (rb) { try { snd("uiTap"); } catch (er) {} repCall(rb.dataset.act); return; }   /* V653 */\n    const st = e.target.closest(".aStat");')
open(p, "w", encoding="utf-8").write(s)
print("ok V653")
