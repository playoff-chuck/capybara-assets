s=open('v183.html',encoding='utf-8').read()
def rep(a,b,cnt=1):
    global s
    n=s.count(a); assert n==cnt,(n,a[:70]); s=s.replace(a,b)
rep('ver: "V183", wave: S.wave','ver: "V184", wave: S.wave')
js=r'''
/* V184: Bass-Klänge nach Martins Wahl (04.11.) – tief, kurz, ohne Höhen, für den Handylautsprecher */
(() => {
  let bus = null, nb = null, lastAc = null; const last = {};
  const GAP = { move: 0.03, soft: 0.03, mg: 0.06, hitTick: 0.07, rotate: 0.04, lock: 0.05, drop: 0.05, die: 0.04, dieS: 0.04, spawn: 0.15, kan: 0.1, frost: 0.08, lines: 0.1, uiTap: 0.04 };
  function setup(ac) { if (bus && lastAc === ac) return true; const out = SFX._out && SFX._out(); if (!out) return false; lastAc = ac;
    bus = ac.createGain(); bus.gain.value = 1.1; const lp = ac.createBiquadFilter(); lp.type = "lowpass"; lp.frequency.value = 2200; lp.Q.value = 0.5;
    const comp = ac.createDynamicsCompressor(); comp.threshold.value = -14; comp.ratio.value = 4; comp.attack.value = 0.003; comp.release.value = 0.15;
    bus.connect(lp); lp.connect(comp); comp.connect(out);
    nb = ac.createBuffer(1, ac.sampleRate, ac.sampleRate); { const d = nb.getChannelData(0); let l = 0; for (let i = 0; i < d.length; i++) { l = 0.97 * l + 0.03 * (Math.random() * 2 - 1); d[i] = l * 6; } } return true; }
  function bassPlay(ac, fn) {
    const T = t => ac.currentTime + 0.005 + (t || 0);
    const env = (t, a, v, d) => { const g = ac.createGain(); g.gain.setValueAtTime(0.0001, t); g.gain.linearRampToValueAtTime(v, t + a); g.gain.exponentialRampToValueAtTime(0.0001, t + a + d); g.connect(bus); return g; };
    const thump = (f0, f1, d, v, type, t) => { t = T(t); const o = ac.createOscillator(); o.type = type || "sine"; o.frequency.setValueAtTime(f0, t); o.frequency.exponentialRampToValueAtTime(Math.max(20, f1), t + d); o.connect(env(t, 0.003, v, d)); o.start(t); o.stop(t + d + 0.05); };
    const noise = (f, d, v, t) => { t = T(t); const s = ac.createBufferSource(); s.buffer = nb; const bp = ac.createBiquadFilter(); bp.type = "lowpass"; bp.frequency.value = f; bp.Q.value = 0.7; s.connect(bp); bp.connect(env(t, 0.002, v, d)); s.start(t, Math.random() * 0.5); s.stop(t + d + 0.05); };
    const tock = (f, d, v, t) => { thump(f, f * 0.8, d, v, "triangle", t); noise(f * 3, d * 0.5, v * 0.5, t); };
    const note = (f, d, v, t) => { thump(f, f, d, v, "triangle", t); thump(f / 2, f / 2, d * 0.8, v * 0.5, "sine", t); };
    const M = n => 440 * Math.pow(2, (n - 69) / 12);
    fn({ thump, noise, tock, note, M });
  }
  const PICK = {   /* Name im Spiel → Klang (Variante laut Martins Wahl) */
    move: k => k.thump(170, 140, 0.04, 0.26),                                                    // B
    mg: k => { k.thump(150, 85, 0.045, 0.32); k.noise(700, 0.03, 0.12); },                         // A
    hitTick: k => k.tock(260, 0.025, 0.14),                                                       // A
    rotate: k => { k.tock(190, 0.025, 0.18); k.tock(250, 0.025, 0.16, 0.04); },                    // B
    soft: k => k.thump(120, 100, 0.03, 0.2),                                                      // B
    lock: k => k.thump(95, 50, 0.15, 0.6, "triangle"),                                            // B
    drop: k => { k.noise(380, 0.07, 0.18); k.thump(95, 45, 0.17, 0.7, "sine", 0.05); },           // A
    die: k => { k.thump(220, 90, 0.1, 0.3); k.noise(350, 0.06, 0.15); },                          // B (Grunt)
    dieS: k => k.thump(380, 180, 0.07, 0.24, "triangle"),                                         // A (Scout)
    spawn: k => k.thump(140, 160, 0.09, 0.22, "triangle"),                                        // B
    kan: k => k.thump(65, 34, 0.26, 0.85, "triangle"),                                            // B
    frost: k => k.thump(250, 200, 0.1, 0.22),                                                     // B
    lines1: k => { [60, 64, 67].forEach((n, i) => k.note(k.M(n), 0.16, 0.24, i * 0.07)); k.thump(80, 50, 0.2, 0.4); },          // A
    lines2: k => { [60, 64, 67, 72].forEach((n, i) => k.note(k.M(n), 0.18, 0.24, i * 0.07)); k.thump(70, 40, 0.3, 0.5); },      // A
    uiTap: k => k.tock(240, 0.025, 0.16),                                                         // A
  };
  function pickFor(n, a) {
    if (n === "squeak" || n === "die") { const kind = a[0] || "norm"; return kind === "norm" ? "die" : kind === "fast" ? "dieS" : null; }
    if (n === "lines") return a[0] === 1 ? "lines1" : a[0] === 2 ? "lines2" : null;
    return PICK[n] ? n : null;
  }
  const orig = SFX.play;
  SFX.play = (n, ...a) => { try {
    const k = pickFor(n, a), ac = SFX._ac && SFX._ac();
    if (k && ac && !SFX.muted && setup(ac)) { const t = ac.currentTime, g = GAP[k] || GAP[n] || 0.03; if (last[k] && t - last[k] < g) return; last[k] = t; bassPlay(ac, PICK[k]); return; }
  } catch (e) {} return orig(n, ...a); };
})();
'''
k=s.rfind('})();\n</script>'); assert k>0; s=s[:k]+js+s[k:]
open('v184.html','w',encoding='utf-8').write(s); print('ok')
