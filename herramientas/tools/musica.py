"""Música propia (sintetizada): pad + arpegio + pulso suave. musica.py segundos salida.wav [semilla]"""
import numpy as np, sys, wave
SR = 44100; dur = float(sys.argv[1]); out = sys.argv[2]; rng = np.random.default_rng(int(sys.argv[3]) if len(sys.argv) > 3 else 1)
bpm = 96; beat = 60 / bpm; n = int(SR * dur); t = np.arange(n) / SR
def f(m): return 440 * 2 ** ((m - 69) / 12)
prog = [[60, 64, 67, 71], [57, 60, 64, 67], [53, 57, 60, 64], [55, 59, 62, 67]]   # Cmaj7 Am7 Fmaj7 G
L = np.zeros(n); R = np.zeros(n)
compas = 4 * beat
def env_adsr(m, a, r):
    e = np.ones(m); ka = int(a * SR); kr = int(r * SR)
    e[:ka] = np.linspace(0, 1, ka); e[-kr:] *= np.linspace(1, 0, kr); return e
k = 0; c = 0
while k * compas < dur:
    ch = prog[c % 4]; i0 = int(k * compas * SR); m = min(int(compas * SR) + int(.6 * SR), n - i0)
    if m <= 0: break
    tt = np.arange(m) / SR; e = env_adsr(m, .5, .7)
    for j, nota in enumerate(ch):
        fr = f(nota - 12); v = (np.sin(2 * np.pi * fr * tt) + .35 * np.sin(2 * np.pi * fr * 2.002 * tt) + .15 * np.sin(2 * np.pi * fr * 3.01 * tt)) * e * .045
        L[i0:i0 + m] += v * (1 - .15 * j); R[i0:i0 + m] += v * (.55 + .15 * j)
    bajo = f(ch[0] - 24); vb = np.sin(2 * np.pi * bajo * tt) * env_adsr(m, .05, .5) * .08; L[i0:i0+m] += vb; R[i0:i0+m] += vb
    for s in range(8):                      # arpegio en corcheas
        nota = ch[[0, 1, 2, 3, 2, 1, 2, 3][s]] + 12
        j0 = i0 + int(s * beat / 2 * SR); mm = min(int(.9 * SR), n - j0)
        if mm <= 0: continue
        ts = np.arange(mm) / SR; vv = np.sin(2 * np.pi * f(nota) * ts) * np.exp(-ts * 5.5) * .05
        pan = .5 + .3 * np.sin(s); L[j0:j0+mm] += vv * (1 - pan) * 1.4; R[j0:j0+mm] += vv * pan * 1.4
    for s in range(4):                      # pulso suave
        j0 = i0 + int(s * beat * SR); mm = min(int(.25 * SR), n - j0)
        if mm <= 0: continue
        ts = np.arange(mm) / SR; kk = np.sin(2 * np.pi * (55 + 60 * np.exp(-ts * 30)) * ts) * np.exp(-ts * 18) * .10
        L[j0:j0+mm] += kk; R[j0:j0+mm] += kk
    k += 1; c += 1
fade = int(2.5 * SR); L[-fade:] *= np.linspace(1, 0, fade); R[-fade:] *= np.linspace(1, 0, fade)
L[:int(SR)] *= np.linspace(0, 1, int(SR)); R[:int(SR)] *= np.linspace(0, 1, int(SR))
x = np.stack([L, R], 1); x = x / max(1e-6, np.abs(x).max()) * .8
w = wave.open(out, 'wb'); w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes((x * 32767).astype('<i2').tobytes()); w.close()
