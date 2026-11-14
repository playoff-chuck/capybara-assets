import sys
# V707: Neue Besucher im Browser sehen zuerst die Trailer-Seite (/trailer/, Sprache automatisch). Martin 14.11.2026 13:31 («3»).
# Nicht umgeleitet: Apps (TWA-Referrer, WebView, installierte PWA), Links mit Parametern, Testläufe (webdriver), alle, die schon gespielt haben.
src, dst = sys.argv[1], sys.argv[2]
s = open(src, encoding="utf-8").read()
def rep(a, b, n=1):
    global s
    c = s.count(a); assert c == n, (a[:60], c); s = s.replace(a, b)
rep('const GAME_VER = "V706";', 'const GAME_VER = "V707";')
rep('<!doctype html><html><head>', '<!doctype html><html><head><script>/* V707: Startseite = Trailer für neue Browser-Besucher */(function(){try{var p=location.pathname,ua=navigator.userAgent||"";if(p!=="/"&&p!=="/index.html")return;if(location.search||location.hash)return;if(navigator.webdriver)return;if(/; wv\\)|CapyWebTest/.test(ua))return;if((document.referrer||"").indexOf("android-app://")===0)return;if(window.matchMedia&&(matchMedia("(display-mode: standalone)").matches||matchMedia("(display-mode: fullscreen)").matches||matchMedia("(display-mode: minimal-ui)").matches))return;if(navigator.standalone)return;for(var i=0;i<localStorage.length;i++){if(/^(capy|tarnturm)/.test(localStorage.key(i)||""))return;}location.replace("/trailer/");}catch(e){}})();</script>')
open(dst, "w", encoding="utf-8").write(s)
print("ok")
