"""V332 (Martin 06.11. 23:15: «Es kommen die Punkte, keine Versionsnummer» – Spiel startet im Browser nicht):
1) Selbstreparatur direkt nach dem Startbild: ist das Spiel nach 12 s nicht fertig geladen (keine Versionsnummer), steht dort
   «Tap to reload» – Antippen löscht Offline-Speicher + Service Worker und lädt neu. Meldet den Hänger an /api/events (boot-stall).
2) drawImage überspringt kaputte Bilder (Fehler «HTMLImageElement … broken state» aus der Hauptschleife, Android Chrome 138)."""
import sys
src, dst = sys.argv[1], sys.argv[2]
s = open(src, encoding='utf-8').read()
def rep(a, b, cnt=1):
    global s
    n = s.count(a); assert n == cnt, (n, a[:70]); s = s.replace(a, b)
rep('const GAME_VER = "V331";', 'const GAME_VER = "V332";')
rep('<div class="spDots" aria-hidden="true"><i></i><i></i><i></i></div></div>',
'''<div class="spDots" aria-hidden="true"><i></i><i></i><i></i></div></div>
<script>(function(){try{var c=CanvasRenderingContext2D.prototype,d=c.drawImage;c.drawImage=function(im){if(im&&im.tagName==="IMG"&&(!im.complete||!im.naturalWidth))return;return d.apply(this,arguments);};}catch(e){}
setTimeout(function(){try{var sp=document.getElementById("splash");if(!sp||!document.body.contains(sp)||sp.querySelector(".verTag"))return;
var st=window.__TT?"tt":"none";try{fetch("/api/events",{method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify({ver:"boot",sess:"boot"+Date.now()%1e6,dev:0,plat:navigator.userAgent.slice(0,120),br:"",sw:screen.width|0,sh:screen.height|0,ev:[{k:"error",msg:"boot-stall "+st+" rs="+document.readyState,src:"splash"}]}),keepalive:true});}catch(e){}
var f=document.createElement("div");f.className="spGo";f.style.display="block";f.textContent="TAP TO RELOAD";var g=sp.querySelector(".spDots");if(g)g.style.display="none";sp.appendChild(f);
sp.addEventListener("click",function(ev){ev.stopImmediatePropagation();var go=function(){location.replace(location.pathname+"?r="+Date.now());};
try{var p=[];if(navigator.serviceWorker)p.push(navigator.serviceWorker.getRegistrations().then(function(rs){return Promise.all(rs.map(function(r){return r.unregister();}));}));
if(window.caches)p.push(caches.keys().then(function(ks){return Promise.all(ks.map(function(k){return caches.delete(k);}));}));Promise.all(p).then(go,go);setTimeout(go,2500);}catch(e){go();}},true);}catch(e){}},12000);})();</script>''')
open(dst, 'w', encoding='utf-8').write(s)
print("ok")
