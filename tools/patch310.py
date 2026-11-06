"""V310: Spiel auf Android installierbar machen (Icon auf dem Startbildschirm).
Martin 06.11. 09:09: Chrome bietet nur «Verknüpfung erstellen», nicht «Installieren»; ✈ zeigt keine Abfrage.
Ursache (Chrome: Page.getInstallabilityErrors → «no-manifest»): <link rel="manifest"> stand nach </head> im <body>
und wird dort von Chrome ignoriert. Jetzt: Manifest-Link und theme-color im <head>, die Kopie im Body entfällt."""
import sys
src, dst = sys.argv[1], sys.argv[2]
s = open(src, encoding='utf-8').read()
def rep(a, b, cnt=1):
    global s
    n = s.count(a); assert n == cnt, (n, a[:70]); s = s.replace(a, b)

rep('const GAME_VER = "V309";', 'const GAME_VER = "V310";')
rep('<title>Capybara Squad</title><link rel="manifest" href="manifest.webmanifest"><meta name="theme-color" content="#2b3a22">',
    '<title>Capybara Squad</title>')
head_end = s.index('</head>')
s = s[:head_end] + '<link rel="manifest" href="manifest.webmanifest"><meta name="theme-color" content="#2b3a22">' + s[head_end:]
assert s.index('rel="manifest"') < s.index('</head>') < s.index('<body')
open(dst, 'w', encoding='utf-8').write(s)
print("ok")
