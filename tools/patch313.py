"""V313: Zahnrad-Menü im Hauptmenü (Martin 06.11. 10:06: «Cloud Save … macht das Hauptmenü überfrachtet.
Mach im Hauptmenü ein schönes Zahnradsymbol und dort legen wir das rein. Dort … auch die Wahl des Avatars und den Namen.»).
- Fußleiste: «☁ Cloud save» raus, dafür gemaltes Zahnrad (Nano Banana Pro, Stil wie Pokal/Medaille).
- Guide-Knopf «i» unten links (lag halb unter dem Flugzeug-Knopf) raus aus der Fußleiste, ebenfalls ins Zahnrad-Menü.
- Zahnrad öffnet die Einstellungen: Held (Blue/Rosie), Spielername, dazu «☁ Cloud save» und «Guide» (Guide nur im Hauptmenü).
Aufruf: python3 tools/patch313.py src dst   (kopiert review/v313/gear.webp als site/img/<hash>.webp)"""
import sys, hashlib, shutil, os
src, dst = sys.argv[1], sys.argv[2]
s = open(src, encoding='utf-8').read()
def rep(a, b, cnt=1):
    global s
    n = s.count(a); assert n == cnt, (n, a[:70]); s = s.replace(a, b)

root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
g = open(os.path.join(root, 'review/v313/gear.webp'), 'rb').read()
gname = 'img/' + hashlib.sha256(g).hexdigest()[:10] + '.webp'
site = os.path.dirname(os.path.abspath(dst)) if os.path.basename(os.path.dirname(os.path.abspath(dst))) == 'site' else os.path.join(root, 'site')
shutil.copyfile(os.path.join(root, 'review/v313/gear.webp'), os.path.join(root, 'site', gname))

rep('const GAME_VER = "V312";', 'const GAME_VER = "V313";')
rep('<button id="btnCloud" class="btn-small">☁ Cloud save</button>',
    '<button id="btnSetM" class="btn-small">Settings</button><button id="btnCloud" class="btn-small">☁ Cloud save</button>')
rep('<input id="setNick" type="text" maxlength="14" autocomplete="off" spellcheck="false" placeholder="e.g. CapyKing">',
    '<input id="setNick" type="text" maxlength="14" autocomplete="off" spellcheck="false" placeholder="e.g. CapyKing">'
    '<div class="setRow"><button id="setCloud" class="btn-small" type="button">☁ Cloud save</button><button id="setGuide" class="btn-small" type="button">Guide</button></div>')

JS = r'''
/* V313: Zahnrad-Menü im Hauptmenü (Cloud save, Held, Name, Guide) */
try { (() => {
  const b = document.getElementById("btnSetM"); if (!b) return;
  b.innerHTML = `<img src="__GEAR__" alt="">`; b.classList.add("icoBtn"); b.setAttribute("aria-label", "Settings"); b.title = "Settings";
  b.addEventListener("click", e => { e.stopPropagation(); try { SFX.init(); snd("uiTap"); } catch (er) {} document.getElementById("btnGear").click(); });
  const ov = document.getElementById("ovSettings"), gd = document.getElementById("setGuide");
  new MutationObserver(() => { if (!ov.hidden) gd.hidden = !!document.getElementById("ovStart").hidden; }).observe(ov, { attributes: true, attributeFilter: ["hidden"] });
  document.getElementById("setCloud").addEventListener("click", e => { e.stopPropagation(); try { window.__cloud && window.__cloud.open(); } catch (er) { console.error("setCloud", er); } });
  gd.addEventListener("click", e => { e.stopPropagation(); document.getElementById("setX").click(); const t0 = Date.now();
    const iv = setInterval(() => { if (ov.hidden || Date.now() - t0 > 3500) { clearInterval(iv); if (ov.hidden) document.getElementById("btnInfo").click(); } }, 100); });
})(); } catch (e) { console.error("v313", e); }
'''.replace('__GEAR__', gname)
anchor = '})();\n</script>'
p = s.rindex(anchor); s = s[:p] + JS + s[p:]
CSS = ('#btnCloud,#btnInfo{display:none!important}\n'
       '#ovSettings .setRow{display:flex;gap:8px;margin-top:6px}\n#ovSettings .setRow button{flex:1;min-height:40px}\n#ovSettings .setRow button[hidden]{display:none}\n')
q = s.rindex('</body>'); s = s[:q] + '<style>\n' + CSS + '</style>\n' + s[q:]
open(dst, 'w', encoding='utf-8').write(s)
print("ok", gname)
