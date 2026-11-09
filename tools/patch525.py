#!/usr/bin/env python3
"""V525 (Martin 09.11. 17:49): Support-Infos.
- Eindeutige Spieler-Nummer (capy-uid, z. B. K7Q2-M9XD, zufällig, 32^8 Möglichkeiten; reist mit dem Cloud-Save mit).
  Nicht der Cloud-Code (der ist geheim und öffnet den Spielstand).
- Rechts oben: Versionsnummer, darunter in gleicher Größe die Spieler-Nummer.
- Zahnrad-Menü: Kasten «SUPPORT INFO» mit Version, Spieler-Nummer und Gerät (System, Modell wenn verfügbar, Browser/App, Bildschirm,
  Kerne, Speicher, Sprache) + Knopf COPY (kopiert alles als eine Zeile).
Aufruf: python3 tools/patch525.py site/index.html"""
import sys
p = sys.argv[1]; s = open(p, encoding="utf-8").read()
def rep(a, b, n=1):
    global s
    c = s.count(a); assert c == n, (c, a[:80]); s = s.replace(a, b)
rep('const GAME_VER = "V524";', 'const GAME_VER = "V525";')
rep('const t = document.createElement("div"); t.className = "verTag"; t.textContent = GAME_VER; o.appendChild(t); } }); } catch (e) {}',
    'const t = document.createElement("div"); t.className = "verTag"; t.textContent = GAME_VER + "\\n" + capyUid(); o.appendChild(t); } }); } catch (e) {}')
rep('.verTag{position:absolute;', '.verTag{white-space:pre;text-align:right;line-height:1.25!important;position:absolute;')
rep('function fxLabel() {', '''/* V525: Spieler-Nummer + Geräte-Info für Support */
function capyUid() { let u = ""; try { u = localStorage.getItem("capy-uid") || ""; } catch (e) {}
  if (!/^[A-Z0-9]{4}-[A-Z0-9]{4}$/.test(u)) { const A = "ABCDEFGHJKLMNPQRSTUVWXYZ23456789"; let r; try { r = crypto.getRandomValues(new Uint8Array(8)); } catch (e) { r = Array.from({ length: 8 }, () => Math.random() * 256 | 0); }
    u = Array.from(r, x => A[x % 32]).join(""); u = u.slice(0, 4) + "-" + u.slice(4); try { localStorage.setItem("capy-uid", u); } catch (e) {} }
  return u; }
const DEVX = { model: "", osv: "" };
try { navigator.userAgentData && navigator.userAgentData.getHighEntropyValues && navigator.userAgentData.getHighEntropyValues(["model", "platformVersion"]).then(v => { DEVX.model = v.model || ""; DEVX.osv = v.platformVersion || ""; supportFill(); }).catch(() => {}); } catch (e) {}
function devInfo() { const ua = navigator.userAgent || ""; let os = "Other", m;
  if ((m = /Android ([\\d.]+)/.exec(ua))) os = "Android " + m[1]; else if ((m = /(iPhone|iPad|iPod).*OS (\\d+[_\\d]*)/.exec(ua))) os = m[1] + " iOS " + m[2].replace(/_/g, "."); else if (/Macintosh/.test(ua)) os = navigator.maxTouchPoints > 1 ? "iPad (desktop mode)" : "macOS"; else if (/Windows/.test(ua)) os = "Windows"; else if (/CrOS/.test(ua)) os = "ChromeOS"; else if (/Linux/.test(ua)) os = "Linux";
  const br = (m = /SamsungBrowser\\/([\\d]+)/.exec(ua)) ? "Samsung Internet " + m[1] : (m = /Edg\\w*\\/([\\d]+)/.exec(ua)) ? "Edge " + m[1] : (m = /OPR\\/([\\d]+)/.exec(ua)) ? "Opera " + m[1] : (m = /YaBrowser\\/([\\d]+)/.exec(ua)) ? "Yandex " + m[1] : (m = /Firefox\\/([\\d]+)/.exec(ua)) ? "Firefox " + m[1] : (m = /CriOS\\/([\\d]+)/.exec(ua)) ? "Chrome iOS " + m[1] : (m = /Chrome\\/([\\d]+)/.exec(ua)) ? "Chrome " + m[1] : (m = /Version\\/([\\d.]+).*Safari/.exec(ua)) ? "Safari " + m[1] : "Browser";
  let app = "Web"; try { if (/^android-app:/.test(document.referrer || "") || sessionStorage.getItem("capy-twa")) { app = "Android app"; sessionStorage.setItem("capy-twa", "1"); } else if (matchMedia("(display-mode: standalone)").matches || navigator.standalone) app = "Home screen"; } catch (e) {}
  const scr = `${screen.width}×${screen.height} @${Math.round((devicePixelRatio || 1) * 100) / 100}x`, hw = [navigator.hardwareConcurrency ? navigator.hardwareConcurrency + " cores" : "", navigator.deviceMemory ? navigator.deviceMemory + " GB" : ""].filter(Boolean).join(" · ");
  return [os + (DEVX.model ? " · " + DEVX.model : ""), app + " · " + br, scr + (hw ? " · " + hw : ""), "lang " + (I18N.lang || "en") + " · " + (navigator.language || "")].join(" | "); }
function supportText() { return `Capybara Squad ${GAME_VER} · player ${capyUid()} · ${devInfo()}`; }
function supportFill() { try { const b = document.getElementById("supBox"); if (!b) return; b.querySelector(".supV").textContent = GAME_VER; b.querySelector(".supU").textContent = capyUid(); b.querySelector(".supD").textContent = devInfo().split(" | ").join("\\n"); } catch (e) {} }
function supportBox() { try { const box = document.querySelector("#ovSettings .joinBox"); if (!box || document.getElementById("supBox")) { supportFill(); return; }
    const d = document.createElement("div"); d.id = "supBox"; d.innerHTML = `<div class="hpHead">SUPPORT INFO</div><div class="supGrid"><span>Version</span><b class="supV" translate="no"></b><span>Player no.</span><b class="supU" translate="no"></b><span>Device</span><b class="supD" translate="no"></b></div><button id="supCopy" class="btn-small" type="button">COPY</button>`;
    box.appendChild(d); supportFill();
    d.querySelector("#supCopy").addEventListener("click", () => { const t = supportText(), ok = () => { try { snd("uiTap"); toast("COPIED · paste it into your message to us", "HQ", 2200); } catch (e) {} };
      try { navigator.clipboard.writeText(t).then(ok, () => { fallback(); }); } catch (e) { fallback(); }
      function fallback() { try { const ta = document.createElement("textarea"); ta.value = t; ta.style.position = "fixed"; ta.style.opacity = "0"; document.body.appendChild(ta); ta.select(); document.execCommand("copy"); ta.remove(); ok(); } catch (e) {} } }); } catch (e) {} }
new MutationObserver(() => { const o = document.getElementById("ovSettings"); if (o && !o.hidden) supportBox(); }).observe(document.getElementById("ovSettings") || document.body, { attributes: true, attributeFilter: ["hidden"] });
function fxLabel() {''')
rep('#ovSettings .setRow{flex-wrap:wrap}', '#ovSettings .setRow{flex-wrap:wrap}\n#supBox{margin-top:12px;padding:10px 12px;border:2px dashed rgba(58,36,20,.35);border-radius:12px;text-align:left}#supBox .supGrid{display:grid;grid-template-columns:auto 1fr;gap:3px 10px;font:500 12px/1.3 ui-monospace,Menlo,monospace;margin:6px 0 8px}#supBox .supGrid span{opacity:.65;font-family:inherit}#supBox .supGrid b{font-weight:700;white-space:pre-wrap;word-break:break-word}#supBox #supCopy{width:100%}')
open(p, "w", encoding="utf-8").write(s); print("ok V525")
