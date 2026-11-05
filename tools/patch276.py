"""V276 (Martin 16:09): Flugzeug wird beim Flug stufenlos kleiner. Bisher sprang --ik bei jedem Kamera-Schritt sofort auf 1/k,
während die Karte 1,3–1,8 s weich zoomte → Größensprünge. Jetzt rechnet jeder Frame die echte aktuelle Kartenskala aus und setzt
die Flugzeuggröße auf dem Bildschirm selbst: erster Flug (von außen) groß 1,8× → 1,0× am Landepunkt, andere Flüge konstant.
Dazu einmalig alles auf «neuer Spieler» zurück (wie Street player), damit Tutorial/Welttour-Start auf Martins Handy wiederkommen."""
import sys
src, dst = sys.argv[1], sys.argv[2]
s = open(src, encoding='utf-8').read()
def rep(a, b, cnt=1):
    global s
    n = s.count(a); assert n == cnt, (n, a[:70]); s = s.replace(a, b)
rep('const GAME_VER = "V275";', 'const GAME_VER = "V276";')
rep('''plane.style.setProperty("--py", (y) * BW * MAP_AR + "px"); {''',
    '''plane.style.setProperty("--py", (y) * BW * MAP_AR + "px");
        { let kc = 1; try { const m = getComputedStyle(world).transform; if (m && m !== "none") kc = parseFloat(m.slice(m.indexOf("(") + 1)) || 1; } catch (er) {}
          const big = (a[0] > 1 || a[0] < 0) ? 0.8 : 0, sc = 1 + big * (1 - e) * (1 - e * 0.35); plane.style.setProperty("--ik", sc / kc); if (t >= 1) plane.style.removeProperty("--ik"); }
        {''')
rep('<script>try{["img/', '<script>try{if(localStorage.getItem("capy-reset")!=="276"){var rk=[];for(var ri=0;ri<localStorage.length;ri++){var rkk=localStorage.key(ri);if(rkk&&/^(tarnturm|capy)/.test(rkk)&&rkk!=="tarnturm-dev")rk.push(rkk);}rk.forEach(function(k){localStorage.removeItem(k);});localStorage.setItem("capy-reset","276");}}catch(e){}\ntry{["img/')
open(dst, 'w', encoding='utf-8').write(s)
