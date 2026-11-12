#!/usr/bin/env python3
# V650 (Martin 12.11. 10:37 / 10:40):
# 1) Jede Sitzung: Betriebssystem, System-Version, Handy-Modell, Browser/App, Zeitzone, UTC-Abstand, Sprache
#    gehen mit jedem Ereignis-Paket (dv) an den Server; Server führt Tabelle «plays» (Start, Ende, Spielzeit, höchste Welle).
#    Admin: je Spieler die letzten 40 Sitzungen mit Ortszeit; Analyse: Modelle, Systeme, Spielzeiten nach Stunde/Wochentag.
# 2) Einstellungen: Fenster so breit wie der Bildschirm (kein Verkleinern mehr, notfalls scrollen),
#    Trainer-Banner ganz oben, Sterne größer, Nachricht als großes Feld, Figurenwahl ganz unten.
import sys, os
site = sys.argv[1]; p = os.path.join(site, "index.html"); s = open(p, encoding="utf-8").read()
def rep(a, b, n=1):
    global s
    c = s.count(a); assert c == n, (c, a[:90]); s = s.replace(a, b)
rep('const GAME_VER = "V649";', 'const GAME_VER = "V650";')

# 1) Geräte-Daten
rep('navigator.userAgentData.getHighEntropyValues(["model", "platformVersion"]).then(v => { DEVX.model = v.model || ""; DEVX.osv = v.platformVersion || ""; supportFill(); })',
    'navigator.userAgentData.getHighEntropyValues(["model", "platformVersion", "platform"]).then(v => { DEVX.model = v.model || ""; DEVX.osv = v.platformVersion || ""; DEVX.plat = v.platform || ""; supportFill(); })')
rep('    function body() { return JSON.stringify({ ver: GAME_VER, sess, dev: dev(), plat, br, sw: screen.width | 0, sh: screen.height | 0, mem: navigator.deviceMemory || null, uid: uidV(), ch, team: teamV(), ev: q.splice(0, 12) }); }',
    '''    const dvI = () => { const o = {}; try { let m;   /* V650: System, Version, Modell, Zeitzone */
        if ((m = /Android ([\\d.]+)/.exec(ua))) { o.os = "Android"; o.osv = m[1]; } else if ((m = /(?:iPhone|iPad|iPod).*? OS (\\d+[_\\d]*)/.exec(ua))) { o.os = /iPad/.test(ua) ? "iPadOS" : "iOS"; o.osv = m[1].replace(/_/g, "."); o.model = (/(iPhone|iPad|iPod)/.exec(ua) || [])[1] || ""; }
        else if ((m = /Mac OS X (\\d+[_\\d]*)/.exec(ua))) { o.os = navigator.maxTouchPoints > 1 ? "iPadOS" : "macOS"; o.osv = m[1].replace(/_/g, "."); } else if ((m = /Windows NT ([\\d.]+)/.exec(ua))) { o.os = "Windows"; o.osv = m[1]; } else if (/CrOS/.test(ua)) o.os = "ChromeOS"; else if (/Linux/.test(ua)) o.os = "Linux"; else o.os = "?";
        if (DEVX.osv) { o.osv = String(DEVX.osv); if (o.os === "Windows") o.osv = (+o.osv.split(".")[0] >= 13 ? "11" : "10") + " (" + DEVX.osv + ")"; }
        if (DEVX.model) o.model = DEVX.model;
        o.tz = Intl.DateTimeFormat().resolvedOptions().timeZone || ""; o.off = -new Date().getTimezoneOffset(); o.lang = (navigator.language || "").slice(0, 8); } catch (e) {} return o; };
    function body() { return JSON.stringify({ ver: GAME_VER, sess, dev: dev(), plat, br, sw: screen.width | 0, sh: screen.height | 0, mem: navigator.deviceMemory || null, uid: uidV(), ch, team: teamV(), dv: dvI(), ev: q.splice(0, 12) }); }''')
# Profil: Modell + Version zusätzlich als eigene Felder
rep('      os: dv[0] || "", app: dv[1] || "", scr: dv[2] || "", loc: dv[3] || "", tz,',
    '      os: dv[0] || "", app: dv[1] || "", scr: dv[2] || "", loc: dv[3] || "", tz, off: -new Date().getTimezoneOffset(), mdl: DEVX.model || "", osv: DEVX.osv || "",   /* V650 */')
# Admin: Sitzungen je Spieler
rep('    h += sec("GERÄT", [kv("System", esc(d.os || "–")),',
    '''    { const P = p.plays || [], two = n => String(n).padStart(2, "0"), WD = ["So", "Mo", "Di", "Mi", "Do", "Fr", "Sa"];   /* V650 */
      const lt = (t, off) => { if (off == null) return new Date(t).toLocaleString("de-AT"); const x = new Date(t + off * 60000); return `${WD[x.getUTCDay()]} ${two(x.getUTCDate())}.${two(x.getUTCMonth() + 1)}. ${two(x.getUTCHours())}:${two(x.getUTCMinutes())}`; };
      const tot = P.reduce((a, y) => a + (y.secs || 0), 0);
      h += sec(`SITZUNGEN (ORTSZEIT DES SPIELERS) · ${P.length}${P.length >= 40 ? "+" : ""} · ${Math.round(tot / 60)} min`, P.length ? P.map(y => kv(esc(lt(y.first, y.off)), esc(`${Math.max(1, Math.round(((y.secs || 0) || (y.last - y.first) / 1000) / 60))} min · bis W${y.maxw || 0} · ${y.os || ""} ${y.osv || ""}${y.model ? " · " + y.model : ""} · ${y.br || ""} · ${y.ver || ""}`))) : ['<div class="aMsg" style="font-size:12px">Noch keine Sitzungen (zählt ab V650).</div>']); }
    h += sec("GERÄT", [kv("System", esc(d.os || "–")), kv("System-Version", esc(d.osv || "–")), kv("Handy-Modell", esc(d.mdl || "–")), kv("UTC-Abstand", d.off != null ? (d.off >= 0 ? "+" : "−") + Math.abs(d.off / 60) + " h" : "–"),''')
# Admin: Analyse
rep('      h += sec("TIPP-KARTEN", obj(x.tips));',
    '''      h += sec("TIPP-KARTEN", obj(x.tips));
      { const pp = x.plays || {}, hr = pp.hours || [], wd = pp.wd || [], mx = Math.max(1, ...hr), mw = Math.max(1, ...wd), WD = ["Mo", "Di", "Mi", "Do", "Fr", "Sa", "So"];   /* V650 */
        const bar = (v, m) => `<i style="display:inline-block;height:9px;width:${Math.round(90 * v / m)}px;background:#e98a2b;border-radius:3px;vertical-align:middle;margin-right:6px"></i>${v}`;
        h += sec("SITZUNGEN · GERÄTE", [kv("Sitzungen", num(pp.n || 0) + " · " + num(pp.mins || 0) + " min gesamt")].concat(obj(pp.models).map(r => r.replace("<span>", "<span>Modell "))).concat(obj(pp.os).map(r => r.replace("<span>", "<span>System "))));
        h += sec("SPIELZEIT NACH ORTSZEIT (STUNDE)", hr.some(Boolean) ? hr.map((v, i) => v ? kv(String(i).padStart(2, "0") + ":00", bar(v, mx)) : "").filter(Boolean) : []);
        h += sec("SPIELZEIT NACH WOCHENTAG", wd.some(Boolean) ? wd.map((v, i) => kv(WD[i], bar(v, mw))) : []); }''')

# 2) Einstellungen
rep('''box.style.transform = ""; const avail = innerHeight - 24, h = box.getBoundingClientRect().height; const r = box.getBoundingClientRect(), k = Math.min(1.2, (innerWidth - 16) / Math.max(1, r.width), Math.max(0.6, avail / Math.max(1, h)));''',
    '''box.style.transform = ""; const avail = innerHeight - 24, h = box.getBoundingClientRect().height; const r = box.getBoundingClientRect(), k = Math.min(1.2, (innerWidth - 16) / Math.max(1, r.width), Math.max(1, avail / Math.max(1, h)));   /* V650: nie kleiner, lieber scrollen */''')
rep('<button id="setMsg" class="btn-small" type="button">✉ MESSAGE</button>',
    '<button id="setMsg" class="btn-small" type="button">✉ MESSAGE</button><span class="setMsgHint">Write us · ideas, bugs, wishes …</span>')
rep('#ovSettings .joinBox{transform-origin:50% 50%!important}',
    '''#ovSettings .joinBox{transform-origin:50% 0!important}
/* V650: Einstellungen breit, Trainer oben, Figuren unten, Bewertung groß */
#ovSettings{z-index:88!important;overflow-y:auto!important;align-items:center!important;justify-content:flex-start!important;padding:calc(env(safe-area-inset-top,0px) + 8px) 8px calc(env(safe-area-inset-bottom,0px) + 110px)!important;-webkit-overflow-scrolling:touch}
#ovSettings .joinBox{box-sizing:border-box!important;width:min(520px,calc(100vw - 16px))!important;margin:0 auto!important;padding:14px 14px 16px!important}
#ovSettings .joinBox>.xBtn{order:-9}#ovSettings .joinBox>.alHead{order:-8}#ovSettings .joinBox>.setTut{order:-7;margin-top:12px}#ovSettings .joinBox>.heroPick{order:20;margin-top:6px}
#ovSettings .tutBanner{max-width:none!important}
#ovSettings .setRate{width:100%;gap:8px;margin-top:8px;padding:10px 8px 12px;border:2.5px solid #3a2414;border-radius:16px;background:#fffdf6;box-sizing:border-box}
#ovSettings .setRate .rateRow{flex-direction:column;gap:10px;width:100%}
#ovSettings .setRate .rateStars{gap:4px}#ovSettings .setRate button.rStar{width:min(54px,13vw)!important;height:min(54px,13vw)!important}
#ovSettings .setRate #setMsg{width:100%;min-height:64px;display:flex;align-items:center;justify-content:center;gap:6px;font-size:17px!important}
#ovSettings .setRate .setMsgHint{display:block;font:600 12px/1.3 var(--f-body,"Baloo 2",sans-serif);color:#7a5a3e;text-align:center;margin-top:-4px}
body:has(#ovSettings:not([hidden])) #btnOffline,body:has(#ovSettings:not([hidden])) #btnMap{visibility:hidden!important}
#ovRate .rBox{width:min(520px,100%)!important}#ovRate textarea{min-height:150px!important;font-size:16px!important}''')
open(p, "w", encoding="utf-8").write(s)
import json
TR = {"en": {"Write us · ideas, bugs, wishes …": "Write us · ideas, bugs, wishes …"},
      "ru": {"Write us · ideas, bugs, wishes …": "Напиши нам · идеи, ошибки, пожелания …"},
      "es": {"Write us · ideas, bugs, wishes …": "Escríbenos · ideas, errores, deseos …"},
      "pt": {"Write us · ideas, bugs, wishes …": "Escreve-nos · ideias, erros, desejos …"}}
for l, add in TR.items():
    q = os.path.join(site, "lang", f"{l}.json"); d = json.load(open(q, encoding="utf-8"))
    for k, v in add.items():
        if k not in d: d[k] = v
    with open(q, "w", encoding="utf-8") as f: json.dump(d, f, ensure_ascii=False, indent=0)
print("ok V650")
