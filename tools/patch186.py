s=open('v185.html',encoding='utf-8').read()
def rep(a,b,cnt=1):
    global s
    n=s.count(a); assert n==cnt,(n,a[:70]); s=s.replace(a,b)
rep('ver: "V185", wave: S.wave','ver: "V186", wave: S.wave')
# Handylautsprecher geben unter ~250 Hz fast nichts wieder: Filter höher, Bus lauter
rep('bus = ac.createGain(); bus.gain.value = 1.1; const lp = ac.createBiquadFilter(); lp.type = "lowpass"; lp.frequency.value = 2200;',
    'bus = ac.createGain(); bus.gain.value = 1.6; const lp = ac.createBiquadFilter(); lp.type = "lowpass"; lp.frequency.value = 4200;')
# Block-Klänge: Grundton bleibt tief, dazu ein hörbarer «Körper» eine/zwei Oktaven höher + kurzer Klick
rep('move: k => k.thump(170, 140, 0.04, 0.26),', 'move: k => { k.thump(170, 140, 0.05, 0.3); k.thump(520, 420, 0.035, 0.22, "triangle"); k.noise(1800, 0.012, 0.12); },')
rep('rotate: k => { k.tock(190, 0.025, 0.18); k.tock(250, 0.025, 0.16, 0.04); },', 'rotate: k => { k.tock(190, 0.03, 0.22); k.thump(600, 560, 0.03, 0.2, "triangle"); k.tock(250, 0.03, 0.2, 0.045); k.thump(780, 740, 0.03, 0.18, "triangle", 0.045); },')
rep('soft: k => k.thump(120, 100, 0.03, 0.2),', 'soft: k => { k.thump(130, 110, 0.035, 0.24); k.thump(440, 380, 0.025, 0.16, "triangle"); },')
rep('lock: k => k.thump(95, 50, 0.15, 0.6, "triangle"),', 'lock: k => { k.thump(95, 50, 0.15, 0.6, "triangle"); k.thump(330, 220, 0.06, 0.32, "triangle"); k.noise(1500, 0.02, 0.18); },')
rep('drop: k => { k.noise(380, 0.07, 0.18); k.thump(95, 45, 0.17, 0.7, "sine", 0.05); },', 'drop: k => { k.noise(900, 0.07, 0.22); k.thump(95, 45, 0.17, 0.7, "sine", 0.05); k.thump(300, 160, 0.08, 0.35, "triangle", 0.05); },')
rep('mg: k => { k.thump(150, 85, 0.045, 0.32); k.noise(700, 0.03, 0.12); },', 'mg: k => { k.thump(150, 85, 0.045, 0.32); k.noise(1400, 0.03, 0.14); },')
rep('hitTick: k => k.tock(260, 0.025, 0.14),', 'hitTick: k => { k.tock(260, 0.025, 0.14); k.thump(700, 600, 0.02, 0.1, "triangle"); },')
open('v186.html','w',encoding='utf-8').write(s); print('ok')
