"""V208: Neuheiten-Bilder sofort da – alle Vorstellungs-Bilder des gewählten Helden werden nach Spielstart
im Hintergrund vorgeladen und dekodiert; falls eins doch noch fehlt, erscheint das Fenster erst mit dem Bild."""
import sys
src, dst = sys.argv[1], sys.argv[2]
s = open(src, encoding='utf-8').read()
def rep(a, b, cnt=1):
    global s
    n = s.count(a); assert n == cnt, (n, a[:70]); s = s.replace(a, b)
rep('const GAME_VER = "V207";', 'const GAME_VER = "V208";')
# Fenster erst zeigen, wenn das Szenenbild bereit ist (max. 1,5 s)
rep('{ const im = w.querySelector("img"); if (im.getAttribute("src") !== fs) { im.classList.add("ldg"); im.onload = im.onerror = () => im.classList.remove("ldg"); im.src = fs; if (im.complete && im.naturalWidth) im.classList.remove("ldg"); } }',
    '{ const im = w.querySelector("img"); if (im.getAttribute("src") !== fs) { const ovI = $("ovIntro"); im.classList.add("ldg"); ovI.style.visibility = "hidden"; const done = () => { im.classList.remove("ldg"); ovI.style.visibility = ""; }; im.onload = im.onerror = done; setTimeout(done, 1500); im.src = fs; if (im.complete && im.naturalWidth) done(); } }')
js = '''
  /* V208: Vorstellungs-Bilder vorladen (gewählter Held), damit sie beim Einblenden sofort da sind */
  try { window.__PRE = window.__PRE || {}; let preHero = null;
    const preload = () => { try { const h = heroKey(); if (preHero === h) return; preHero = h;
        const list = Object.entries(INTRO_SC).filter(([k]) => k.startsWith(h + "_")).map(([, v]) => v)
          .concat(["jaguar", "mummy", "tiger", "bear", "elite"].map(k => `intro/in_${h}_${k}.webp`));
        let i = 0; const next = () => { if (i >= list.length) return; const u = list[i++]; if (window.__PRE[u]) return next(); const im = new Image(); im.decoding = "async"; im.src = u; window.__PRE[u] = im;
          const go = () => (window.requestIdleCallback ? requestIdleCallback(next, { timeout: 400 }) : setTimeout(next, 60)); (im.decode ? im.decode() : Promise.resolve()).then(go, go); };
        next(); } catch (e) {} };
    setInterval(() => { if (typeof S !== "undefined" && S && S.started) preload(); }, 1500); } catch (e) {}
'''
i = s.rfind('})();\n</script>'); s = s[:i] + js + s[i:]
open(dst, 'w', encoding='utf-8').write(s); print('ok')
