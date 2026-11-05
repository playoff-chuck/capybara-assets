"""V302 (To-do 19): Cloud-Speicherstand mit Wiederherstellungscode.
Sichert alle Spieldaten (localStorage tarnturm-*/capy-*) nach dem Speichern (höchstens 1× je 60 s) und beim Verlassen
auf /api/save unter einem zufälligen Code CAPY-XXXXX-XXXXX. Server behält die letzten 5 Stände je Code.
Fenster «☁ CLOUD SAVE» (Startbildschirm + Pause): Code zeigen/kopieren, Stand per Code wiederherstellen.
Reset-Skript lässt den Code (capy-cloud) stehen; Speicher wird als dauerhaft angefragt (storage.persist)."""
import sys
src, dst = sys.argv[1], sys.argv[2]
s = open(src, encoding='utf-8').read()
def rep(a, b, cnt=1):
    global s
    n = s.count(a); assert n == cnt, (n, a[:70]); s = s.replace(a, b)
rep('const GAME_VER = "V301";', 'const GAME_VER = "V302";')
rep('if(rkk&&/^(tarnturm|capy)/.test(rkk)&&rkk!=="tarnturm-dev")rk.push(rkk);',
    'if(rkk&&/^(tarnturm|capy)/.test(rkk)&&rkk!=="tarnturm-dev"&&rkk!=="capy-cloud")rk.push(rkk);')
rep('<button id="btnAlbum" class="btn-small">Medals', '<button id="btnCloud" class="btn-small">☁ Cloud save</button><button id="btnAlbum" class="btn-small">Medals')
rep('<button id="btnPFb">Send feedback</button>', '<button id="btnPCloud">☁ Cloud save</button><button id="btnPFb">Send feedback</button>')
rep('<li><b>No personal data.</b> Your progress stays on this device.</li>', '<li><b>No personal data.</b> Your progress is backed up under a random code – no name, no e-mail.</li>')
rep('<button class="btn-accent btn-big" id="btnAccept">Let\'s go!</button>', '<button class="btn-accent btn-big" id="btnAccept">Let\'s go!</button><button class="btn-small cloudT" id="btnCloudT">☁ I already play – restore my progress</button>')
rep('Your game progress stays on this device. We collect no other personal data.',
    'Your progress is backed up under a random code (☁ Cloud save) – no name, no e-mail. We collect no other personal data.')

JS = r'''
  /* V302: Cloud-Speicherstand mit Wiederherstellungscode (To-do 19) */
  try { (() => {
    const AL = "0123456789ABCDEFGHJKMNPQRSTVWXYZ";
    const SKIP = new Set(["tarnturm-dev", "tarnturm-devnointro", "capy-offline", "capy-cloud", "capy-cloudT"]);
    const norm = c => { c = String(c || "").toUpperCase().replace(/[\s-]/g, "").replace(/O/g, "0").replace(/[IL]/g, "1"); if (c.startsWith("CAPY")) c = c.slice(4); return /^[0-9A-HJKMNP-TV-Z]{10}$/.test(c) ? c : null; };
    const show = c => c ? `CAPY-${c.slice(0, 5)}-${c.slice(5)}` : "";
    const get = k => { try { return localStorage.getItem(k); } catch (e) { return null; } };
    const set = (k, v) => { try { localStorage.setItem(k, v); } catch (e) {} };
    function code(make) { let c = norm(get("capy-cloud")); if (!c && make) { c = Array.from(crypto.getRandomValues(new Uint8Array(10)), b => AL[b & 31]).join(""); set("capy-cloud", c); } return c; }
    function snap() { const d = {}; try { for (let i = 0; i < localStorage.length; i++) { const k = localStorage.key(i); if (k && /^(tarnturm|capy)-[a-z0-9_-]{1,40}$/.test(k) && !SKIP.has(k)) d[k] = localStorage.getItem(k); } } catch (e) {} return d; }
    const worth = d => Object.keys(d).some(k => k === "tarnturm-save" || /^tarnturm-(best|hs|cp|nuts-best)-/.test(k) || k === "tarnturm-album");
    try { navigator.storage && navigator.storage.persist && navigator.storage.persist().catch(() => {}); } catch (e) {}
    let lastUp = 0, pend = null, busy = false, lastErr = "";
    function body() { const d = snap(); if (!worth(d)) return null; let w = 0; try { w = (S && S.wave) | 0; } catch (e) {} return JSON.stringify({ code: code(true), ver: GAME_VER, wave: w, data: d }); }
    async function upload(beacon) { const b = body(); if (!b) return false;
      if (beacon && navigator.sendBeacon) { try { if (navigator.sendBeacon(API_BASE + "/save", b)) { lastUp = Date.now(); set("capy-cloudT", String(lastUp)); return true; } } catch (e) {} }
      if (busy) return false; busy = true;
      try { const r = await fetch(API_BASE + "/save", { method: "POST", headers: { "Content-Type": "application/json" }, body: b, keepalive: b.length < 60000 });
        busy = false; if (r.ok) { lastUp = Date.now(); set("capy-cloudT", String(lastUp)); lastErr = ""; paint(); return true; } lastErr = "Server busy – will retry"; }
      catch (e) { busy = false; lastErr = "Offline – will retry"; }
      paint(); return false; }
    function soon() { if (pend) return; const wait = Math.max(3000, 60000 - (Date.now() - lastUp)); pend = setTimeout(() => { pend = null; upload(false); }, wait); }
    const _sg = saveGame; saveGame = function () { const r = _sg.apply(this, arguments); try { soon(); } catch (e) {} return r; };
    document.addEventListener("visibilitychange", () => { if (document.hidden && Date.now() - lastUp > 5000) upload(true); });
    setInterval(() => { if (Date.now() - lastUp > 10 * 60000) upload(false); }, 5 * 60000);

    const ov = document.createElement("div"); ov.className = "overlay joinOv"; ov.id = "ovCloud"; ov.hidden = true;
    ov.innerHTML = `<div class="joinBox cloudBox"><button class="xBtn" id="cloudX" aria-label="Close"><svg viewBox="0 0 24 24"><path d="M6 6l12 12M18 6L6 18" stroke="currentColor" stroke-width="3" stroke-linecap="round"/></svg></button>
      <div class="alHead"><span class="alTag">☁ CLOUD SAVE</span></div>
      <p class="cloudTxt">Your progress is backed up on our server. Write down your code – with it you get your progress back on any phone.</p>
      <div class="cloudCode" id="cloudCode"></div>
      <div class="cloudRow"><button class="btn-small" id="cloudCopy">Copy code</button><button class="btn-small" id="cloudNow">Back up now</button></div>
      <p class="cloudStat" id="cloudStat"></p>
      <div class="cloudSep">RESTORE ON THIS DEVICE</div>
      <div class="cloudRow"><input id="cloudIn" type="text" maxlength="20" autocomplete="off" spellcheck="false" autocapitalize="characters" placeholder="CAPY-XXXXX-XXXXX"><button class="btn-small" id="cloudGet">Find</button></div>
      <p class="cloudStat" id="cloudMsg"></p>
      <div class="cloudRow" id="cloudAsk" hidden><button class="btn-accent" id="cloudYes">Yes, restore</button><button class="btn-small" id="cloudNo">Cancel</button></div></div>`;
    document.body.appendChild(ov);
    const $c = id => document.getElementById(id); let found = null;
    const ago = t => { const m = Math.round((Date.now() - t) / 60000); return m < 1 ? "just now" : m < 60 ? `${m} min ago` : m < 1440 ? `${Math.round(m / 60)} h ago` : new Date(t).toLocaleDateString("en-GB", { day: "numeric", month: "short" }); };
    function paint() { if (ov.hidden) return; const c = code(false), t = +get("capy-cloudT") || 0;
      $c("cloudCode").textContent = c ? show(c) : "–"; $c("cloudCopy").disabled = !c;
      $c("cloudStat").textContent = lastErr ? lastErr : !c ? "Your code appears after your first wave." : t ? `Last backup: ${ago(t)}` : "Not backed up yet."; }
    let wasPaused = null;
    function open() { try { SFX.init(); snd("uiTap"); } catch (e) {} found = null; $c("cloudAsk").hidden = true; $c("cloudMsg").textContent = ""; $c("cloudIn").value = "";
      ov.hidden = false; paint(); if (!code(false) && worth(snap())) upload(false); }
    function close() { ov.hidden = true; try { snd("uiTap"); } catch (e) {} }
    async function find() { const c = norm($c("cloudIn").value); found = null; $c("cloudAsk").hidden = true;
      if (!c) { $c("cloudMsg").textContent = "That code doesn't look right. It has 10 letters/digits after CAPY."; return; }
      $c("cloudMsg").textContent = "Looking…";
      try { const r = await fetch(API_BASE + "/save?code=" + c, { cache: "no-store" });
        if (r.status === 404) { $c("cloudMsg").textContent = "No backup found for this code."; return; }
        if (!r.ok) { $c("cloudMsg").textContent = "Server busy – please try again in a minute."; return; }
        const d = await r.json(); found = { c, d };
        $c("cloudMsg").textContent = `Found: wave ${d.wave || "?"}, saved ${ago(d.t)}. This replaces the progress on this device.`; $c("cloudAsk").hidden = false; }
      catch (e) { $c("cloudMsg").textContent = "No connection – please try again online."; } }
    async function restore() { if (!found) return; const { c, d } = found;
      try { const mine = code(false); if (mine && mine !== c) await upload(false); } catch (e) {}
      try { const keep = new Set(["tarnturm-dev"]); const rm = []; for (let i = 0; i < localStorage.length; i++) { const k = localStorage.key(i); if (k && /^(tarnturm|capy)-/.test(k) && !keep.has(k)) rm.push(k); }
        rm.forEach(k => localStorage.removeItem(k)); Object.entries(d.data || {}).forEach(([k, v]) => { if (/^(tarnturm|capy)-/.test(k) && typeof v === "string") localStorage.setItem(k, v); });
        localStorage.setItem("capy-cloud", c); localStorage.setItem("capy-cloudT", String(Date.now())); localStorage.setItem("capy-reset", "276"); } catch (e) { $c("cloudMsg").textContent = "Could not write the save on this device."; return; }
      $c("cloudMsg").textContent = "Restored! Restarting…"; setTimeout(() => location.reload(), 600); }
    ov.addEventListener("click", e => { e.stopPropagation(); const b = e.target.closest("button"); if (!b) { if (e.target === ov) close(); return; }
      if (b.id === "cloudX") close(); else if (b.id === "cloudCopy") { const t = show(code(false)); try { navigator.clipboard.writeText(t).then(() => { $c("cloudStat").textContent = "Copied!"; }, () => {}); } catch (er) {} try { snd("uiTap"); } catch (er) {} }
      else if (b.id === "cloudNow") { $c("cloudStat").textContent = "Backing up…"; upload(false).then(ok => { if (!ok && !lastErr) $c("cloudStat").textContent = "Nothing to back up yet – play a wave first."; }); }
      else if (b.id === "cloudGet") find(); else if (b.id === "cloudYes") restore(); else if (b.id === "cloudNo") { found = null; $c("cloudAsk").hidden = true; $c("cloudMsg").textContent = ""; } });
    $c("cloudIn").addEventListener("keydown", e => { if (e.key === "Enter") find(); });
    ["btnCloud", "btnPCloud", "btnCloudT"].forEach(id => { const b = $c(id); b && b.addEventListener("click", e => { e.stopPropagation(); open(); }); });
    window.__cloud = { code, snap, upload, open, norm, show };
  })(); } catch (e) { console.error("cloud", e); }
'''
CSS = '''<style id="v302cloud">
#ovCloud{z-index:990}
.cloudBox{text-align:center}
.cloudTxt{margin:8px 0 10px;font-weight:700;font-size:14px;line-height:1.35}
.cloudCode{font:800 26px/1.2 "Baloo 2",system-ui,sans-serif;letter-spacing:1.5px;background:#fff6e6;border:3px dashed #3a2a1a;border-radius:14px;padding:10px 8px;margin:4px 0 10px;user-select:all;-webkit-user-select:all;color:#3a2a1a}
.cloudRow{display:flex;gap:8px;justify-content:center;align-items:center;margin:6px 0}
.cloudRow input{flex:1;min-width:0;font:800 17px/1.2 "Baloo 2",system-ui,sans-serif;letter-spacing:1px;text-transform:uppercase;padding:9px 10px;border-radius:10px;border:2px solid #3a2a1a;background:#fff!important;color:#3a2a1a!important}
.cloudRow input::placeholder{color:#b9a88c}
.cloudT{display:block;margin:10px auto 0}
.cloudStat{min-height:18px;margin:4px 0;font-size:13px;font-weight:700;opacity:.85}
.cloudSep{margin:14px 0 4px;font:900 11px/1 system-ui;letter-spacing:1px;opacity:.7}
</style>
</body>'''
rep('</body>', CSS)
end = '})();\n</script>'
i = s.rindex(end)
s = s[:i] + JS + s[i:]
open(dst, 'w', encoding='utf-8').write(s)
print("ok")
