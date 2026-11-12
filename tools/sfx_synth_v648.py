#!/usr/bin/env python3
"""V648: erzeugt die gewählten Effekt-Samples (Martin 12.11., Klangvergleich) → <out>/fx_*.mp3
Vorgabe: Handy + Kopfhörer – nicht schrill, nicht bassig, reduziert (Band 180–4500 Hz, weiche Anschläge).
Stein = lock B (Filz-Tupf) · Reihe = lines A (3 Marimba-Töne) · Splat B (Blopp) · MG B (ein gedämpfter Plopp) · Münze B (2 Marimba-Töne) · Kanone = Runde 1.
Aufruf: python3 tools/sfx_synth_v648.py site/sfx   (braucht numpy + ffmpeg)"""
import numpy as np, wave, sys, os, subprocess, tempfile
SR = 44100; OUT = sys.argv[1]
def t_(n): return np.arange(n) / SR
def env(n, a, d): t = t_(n); return np.minimum(1, t / max(a, 1e-4)) * np.exp(-t / d)
def noise(n, seed=0): return np.random.default_rng(seed).standard_normal(n)
def band(x, lo, hi, soft=0.25):
    X = np.fft.rfft(x); f = np.fft.rfftfreq(len(x), 1 / SR)
    g = 1 / (1 + (lo / np.maximum(f, 1)) ** (2 / soft)) / (1 + (f / hi) ** (2 / soft)); return np.fft.irfft(X * g, len(x))
def bp(x, lo, hi):
    X = np.fft.rfft(x); f = np.fft.rfftfreq(len(x), 1 / SR); X[(f < lo) | (f > hi)] = 0; return np.fft.irfft(X, len(x))
def tone(f, dur, a=.004, d=.08, h=()):
    n = int(dur * SR); t = t_(n); y = np.sin(2 * np.pi * f * t)
    for m, amp in h: y += amp * np.sin(2 * np.pi * f * m * t)
    return y * env(n, a, d)
def glide(f0, f1, dur, a=.004, d=.06):
    n = int(dur * SR); t = t_(n); f = f1 + (f0 - f1) * np.exp(-t * 5 / dur); return np.sin(2 * np.pi * np.cumsum(f) / SR) * env(n, a, d)
def sweep(f0, f1, dur, shape=3):
    n = int(dur * SR); t = t_(n); f = f1 + (f0 - f1) * np.exp(-t * shape / dur); return np.sin(2 * np.pi * np.cumsum(f) / SR)
def at(total, parts):
    o = np.zeros(int(total * SR))
    for t0, x in parts: s = int(t0 * SR); o[s:s + len(x)] += x[:len(o) - s]
    return o
def soft(x):   # Runde-2-Nachbearbeitung
    x = band(x, 180, 4500, 0.4); fo = int(.008 * SR); x[-fo:] *= np.linspace(1, 0, fo); x[:int(.002 * SR)] *= np.linspace(0, 1, int(.002 * SR))
    i = np.where(np.abs(x) > 1e-4)[0]; return x[:i[-1] + int(.03 * SR)] if len(i) else x
def trim(x, thr=.005):
    i = np.where(np.abs(x) > thr * np.max(np.abs(x)))[0]; return x[max(0, i[0] - 50):i[-1] + 200]
def save(name, x):
    x = x / np.max(np.abs(x)) * 10 ** (-6 / 20); fo = int(.006 * SR); x[-fo:] *= np.linspace(1, 0, fo)
    w = tempfile.NamedTemporaryFile(suffix=".wav", delete=False).name
    ww = wave.open(w, "wb"); ww.setnchannels(1); ww.setsampwidth(2); ww.setframerate(SR); ww.writeframes((x * 32767).astype(np.int16).tobytes()); ww.close()
    subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-i", w, "-ac", "1", "-ar", "44100", "-b:a", "80k", os.path.join(OUT, f"fx_{name}.mp3")], check=True); os.remove(w)
save("lock", trim(soft(tone(330, .14, .004, .035, ((2, .15),)))))
save("lines", trim(soft(at(.7, [(0, tone(523, .4, .004, .09, ((4, .08),))), (.07, tone(659, .4, .004, .09, ((4, .08),))), (.14, tone(784, .45, .004, .12, ((4, .08),)))]))))
save("splat", trim(soft(glide(420, 170, .14, .004, .04))))
mg = soft(at(.35, [(i * .085, tone(300, .06, .003, .014)) for i in range(3)])); i = np.where(np.abs(mg) > .02 * np.max(np.abs(mg)))[0]; save("mg", mg[i[0]:i[0] + int(.075 * SR)])
save("coin", trim(soft(at(.4, [(0, tone(784, .2, .004, .05)), (.07, tone(1046.5, .3, .004, .07))]))))
n = int(1.0 * SR)
kan = (sweep(90, 38, .6, 3) * env(int(.6 * SR), .002, .18))[:n]
kan = np.concatenate([kan, np.zeros(n - len(kan))]) + bp(noise(n, 20), 60, 600) * env(n, .003, .25) * .7 + bp(noise(n, 21), 2000, 8000) * env(n, .0003, .01) * .6
k1 = np.where(np.abs(kan) > .01 * np.max(np.abs(kan)))[0]; save("kan", trim(kan[max(0, k1[0] - 200):k1[-1] + 2000]))
print("ok fx")
