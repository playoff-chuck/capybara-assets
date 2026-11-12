#!/usr/bin/env python3
# V658 (Martin 12.11. 12:27): Leicht-Modus für ältere Handys.
# Baut auf dem Effekte-Schalter (V494) auf: Effekte aus (automatisch bei Ruckeln/schwacher Hardware oder von Hand) = Leicht-Modus:
#  - Spielfeld-Canvas mit max. 2-facher Pixeldichte (schwache Hardware 1,5) statt bis 3 – größter Gewinn auf Handys mit 3–3,5x
#  - keine Weichzeichner (backdrop-filter), DJ-/Deko-Dauerbewegungen aus, Partikel auf 36 begrenzt
#  - Knopf in den Einstellungen heißt jetzt «GRAPHICS: FULL / LITE (AUTO) / LITE»
import sys, os, json
site = sys.argv[1]; p = os.path.join(site, "index.html"); s = open(p, encoding="utf-8").read()
def rep(a, b, n=1):
    global s
    c = s.count(a); assert c == n, (c, a[:90]); s = s.replace(a, b)
rep('const GAME_VER = "V657";', 'const GAME_VER = "V658";')
rep('function fxOn() { const p = fxPref(); return p !== "off" && p !== "auto-off"; }',
    'function fxOn() { const p = fxPref(); return p !== "off" && p !== "auto-off"; }\n'
    'function liteOn() { return !fxOn(); }   /* V658: Leicht-Modus = Effekte aus */\n'
    'function liteApply() { try { document.body.classList.toggle("lite", liteOn()); } catch (e) {} try { resize(); } catch (e) {} }')
rep('function fxLabel() { const b = $("setFx"); if (b) b.textContent = "EFFECTS: " + (fxOn() ? "ON" : fxPref() === "auto-off" ? "OFF (AUTO)" : "OFF"); }',
    'function fxLabel() { const b = $("setFx"); if (b) b.textContent = "GRAPHICS: " + (fxOn() ? "FULL" : fxPref() === "auto-off" ? "LITE (AUTO)" : "LITE"); }   /* V658 */')
rep('function fxAutoOff(why) { if (fxPref() != null || FX_FORCE != null) return; try { localStorage.setItem("capy-fx", "auto-off"); } catch (e) {} fxLabel();',
    'function fxAutoOff(why) { if (fxPref() != null || FX_FORCE != null) return; try { localStorage.setItem("capy-fx", "auto-off"); } catch (e) {} fxLabel(); liteApply(); try { window.__evLog && window.__evLog.push("perf", { d: { lite: 1, why: String(why || "") } }); } catch (e) {}')
rep('toast("EFFECTS OFF · smoother play on this phone", "HQ", 2400);', 'toast("LITE GRAPHICS · smoother play on this phone", "HQ", 2400);')
rep('setTimeout(() => { fxLabel(); if (FX_WEAK) fxAutoOff("hw"); }, 1500);',
    'setTimeout(() => { fxLabel(); liteApply(); if (FX_WEAK) fxAutoOff("hw"); }, 1500);\n'
    'setInterval(() => { try { if (liteOn() && S && S.fx && S.fx.length > 36) S.fx.splice(0, S.fx.length - 36); } catch (e) {} }, 300);   /* V658: Partikel begrenzen */')
rep('''if (e.target.closest("#setFx")) { const on = fxOn(); try { localStorage.setItem("capy-fx", on ? "off" : "on"); } catch (er) {} if (on) { try { if (S && S.fx) S.fx = S.fx.filter(f => f.type !== "ofx"); } catch (er) {} } fxLabel();''',
    '''if (e.target.closest("#setFx")) { const on = fxOn(); try { localStorage.setItem("capy-fx", on ? "off" : "on"); } catch (er) {} if (on) { try { if (S && S.fx) S.fx = S.fx.filter(f => f.type !== "ofx"); } catch (er) {} } fxLabel(); liteApply();''')
rep('DPR = Math.min(3, window.devicePixelRatio || 1);\n  cv.width = Math.round(r.width * DPR);',
    'DPR = Math.min((typeof liteOn === "function" && liteOn()) ? (FX_WEAK ? 1.5 : 2) : 3, window.devicePixelRatio || 1);   /* V658 */\n  cv.width = Math.round(r.width * DPR);')
rep('#ovSettings .joinBox{transform-origin:50% 0!important}',
    '#ovSettings .joinBox{transform-origin:50% 0!important}\n'
    '/* V658: Leicht-Modus */\n'
    'body.lite *,body.lite *::before,body.lite *::after{-webkit-backdrop-filter:none!important;backdrop-filter:none!important}'
    'body.lite .dj .disc,body.lite .dj .djhead,body.lite .dj .djarm,body.lite .dj .djLedger,body.lite .modeBtn svg.sold,body.lite .board.wounded,body.lite .board.wounded canvas#cv,body.lite .hkConf i,body.lite .allIn.prem::after{animation:none!important}')
open(p, "w", encoding="utf-8").write(s)
TR = {"GRAPHICS:": {"ru": "ГРАФИКА:", "es": "GRÁFICOS:", "pt": "GRÁFICOS:"}, "FULL": {"ru": "ПОЛНАЯ", "es": "COMPLETOS", "pt": "COMPLETOS"},
      "LITE": {"ru": "ЛЁГКАЯ", "es": "LIGEROS", "pt": "LEVES"}, "LITE (AUTO)": {"ru": "ЛЁГКАЯ (АВТО)", "es": "LIGEROS (AUTO)", "pt": "LEVES (AUTO)"},
      "GRAPHICS: FULL": {"ru": "ГРАФИКА: ПОЛНАЯ", "es": "GRÁFICOS: COMPLETOS", "pt": "GRÁFICOS: COMPLETOS"},
      "GRAPHICS: LITE": {"ru": "ГРАФИКА: ЛЁГКАЯ", "es": "GRÁFICOS: LIGEROS", "pt": "GRÁFICOS: LEVES"},
      "GRAPHICS: LITE (AUTO)": {"ru": "ГРАФИКА: ЛЁГКАЯ (АВТО)", "es": "GRÁFICOS: LIGEROS (AUTO)", "pt": "GRÁFICOS: LEVES (AUTO)"},
      "LITE GRAPHICS · smoother play on this phone": {"ru": "ЛЁГКАЯ ГРАФИКА · так игра идёт плавнее", "es": "GRÁFICOS LIGEROS · juego más fluido en este móvil", "pt": "GRÁFICOS LEVES · jogo mais fluido neste celular"}}
for l in ("en", "ru", "es", "pt"):
    q = os.path.join(site, "lang", f"{l}.json"); d = json.load(open(q, encoding="utf-8"))
    for k, v in TR.items():
        if k not in d: d[k] = k if l == "en" else v[l]
    with open(q, "w", encoding="utf-8") as f: json.dump(d, f, ensure_ascii=False, indent=0)
print("ok V658")
