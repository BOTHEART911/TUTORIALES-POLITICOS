"""Compositor de tutoriales PRIV.
python3 tut.py <guion.json> <h|v>  ->  out/<ID>_<16x9|9x16>.mp4

Lee rec/<ID>_<fmt>/rec.json (frames + marcas), voz/<ID>/ (mp3, vtt, dur.json).
Cada escena se acompasa a su voz (0,75x a 1,6x y congelado al final).
"""
import json, os, re, sys, subprocess, bisect, wave
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter

T = '/home/claude/tut'
G = json.load(open(sys.argv[1])); FMT = sys.argv[2]; ID = G['id']
REC = json.load(open(f'{T}/rec/{ID}_{FMT}/rec.json'))
VD = f'{T}/voz/{ID}'; DUR = json.load(open(f'{VD}/dur.json'))
W, H = (1920, 1080) if FMT == 'h' else (1080, 1920)
FPS = 30
TMP = f'{T}/build/tmp_{ID}_{FMT}'; os.makedirs(TMP, exist_ok=True)
OUT = f'{T}/out/{ID}'; os.makedirs(OUT, exist_ok=True)
NOCHE, AZUL, NAR = '#0A2540', '#0063D8', '#C2410C'
SORA = lambda w, s: ImageFont.truetype(f'{T}/fuente/ttf/Sora-{w}.ttf', s)
INTER = lambda n, s: ImageFont.truetype(f'/usr/share/fonts/opentype/inter/Inter-{n}.otf', s)
INTRO, OUTRO = 3.2, 4.2

# ---------------- línea de tiempo ----------------
frames = REC['frames']; fts = [f[0] for f in frames]
marcas = REC['marcas']
CORTES = REC.get('cortes', [])
def _corte_en(a, b):
    return sum(max(0, min(b, c1) - max(a, c0)) for c0, c1 in CORTES)
def real_de(a, x):
    """tiempo real tras 'x' segundos útiles desde 'a', saltando los cortes"""
    t = a
    for c0, c1 in sorted(CORTES):
        if c1 <= t: continue
        if c0 >= t + x: break
        x -= max(0, c0 - t); t = c1
    return t + x
OTRO = f"{T}/rec/{ID}_{'v' if FMT == 'h' else 'h'}/rec.json"
S_OTRO = {}
if os.path.exists(OTRO):   # mismo ritmo en video y Short (capítulos iguales)
    _R = json.load(open(OTRO)); _m = _R['marcas']; _c = _R.get('cortes', [])
    for _i, (_n, _a) in enumerate(_m[:-1]):
        _b = _m[_i + 1][1]; S_OTRO[_n] = _b - _a - sum(max(0, min(_b, c1) - max(_a, c0)) for c0, c1 in _c)
esc = []
t = INTRO
for i, (nom, a) in enumerate(marcas[:-1]):
    b = marcas[i + 1][1]; S = b - a - _corte_en(a, b); V = DUR[nom]
    Tn = max(V + 0.75, S / 1.6, S_OTRO.get(nom, 0) / 1.6)
    f = max(0.75, min(1.6, S / Tn))
    esc.append(dict(id=nom, a=a, S=S, T=Tn, f=f, t0=t, voz=t + 0.3)); t += Tn
TOTAL = t + OUTRO
print('duración', round(TOTAL, 1), [(e['id'], round(e['T'], 1), round(e['f'], 2)) for e in esc])


def src_en(tout):
    if tout < INTRO: return esc[0]['a']
    for e in esc:
        if tout < e['t0'] + e['T']:
            return real_de(e['a'], min((tout - e['t0']) * e['f'], e['S'] - 0.02))
    return real_de(esc[-1]['a'], esc[-1]['S'] - 0.02)


# ---------------- capas fijas ----------------
def fondo():
    im = Image.new('RGB', (W, H), NOCHE); d = ImageDraw.Draw(im)
    for y in range(H):
        k = y / H; d.line([(0, y), (W, y)], fill=(int(10 + 8 * k), int(37 + 20 * k), int(64 + 40 * k)))
    glow = Image.new('L', (W, H), 0); ImageDraw.Draw(glow).ellipse([W * .55, -H * .3, W * 1.3, H * .5], fill=70)
    glow = glow.filter(ImageFilter.GaussianBlur(160))
    im = Image.composite(Image.new('RGB', (W, H), '#1f6fe0'), im, glow)
    d = ImageDraw.Draw(im)
    for x in range(0, W, 36):
        for y in range(0, H, 36): d.point((x, y), fill=(40, 70, 105))
    return im


if FMT == 'h':
    BAR = 40; VW, VH = 1494, 840; VX, VY = (W - VW) // 2, 30 + BAR
    VENT = (VX, VY - BAR, VX + VW, VY + VH); RAD = 18
else:
    VW, VH = 638, 1380; VX, VY = (W - VW) // 2, 226; BEZ = 16; RAD = 64
    VENT = (VX - BEZ, VY - BEZ, VX + VW + BEZ, VY + VH + BEZ)


def chrome():
    bg = fondo().convert('RGBA'); d = ImageDraw.Draw(bg)
    sh = Image.new('L', (W, H), 0); ImageDraw.Draw(sh).rounded_rectangle([VENT[0] + 6, VENT[1] + 18, VENT[2] + 6, VENT[3] + 26], RAD + 6, fill=150)
    sh = sh.filter(ImageFilter.GaussianBlur(26)); bg = Image.composite(Image.new('RGBA', (W, H), (0, 0, 0, 255)), bg, sh); d = ImageDraw.Draw(bg)
    if FMT == 'h':
        d.rounded_rectangle(VENT, RAD, fill='#E9EEF5')
        for i, c in enumerate(['#FF5F57', '#FEBC2E', '#28C840']): d.ellipse([VX + 18 + i * 22, VY - BAR + 14, VX + 30 + i * 22, VY - BAR + 26], fill=c)
        d.rounded_rectangle([VX + 110, VY - BAR + 8, VX + 660, VY - BAR + 32], 12, fill='#FFFFFF')
        d.text((VX + 128, VY - BAR + 20), G.get('barra', 'Panel privado · app de la campaña'), font=INTER('Medium', 15), fill='#4B5B72', anchor='lm')
        et = f"Tutorial {G['num']} · {G['titulo']}"
        d.text((VX + VW - 18, VY - BAR + 20), et, font=INTER('SemiBold', 16), fill='#0A2540', anchor='rm')
        hueco = [VX, VY, VX + VW, VY + VH]; rr = 0
    else:
        d.rounded_rectangle(VENT, RAD, fill='#111827'); d.rounded_rectangle([VENT[0] + 3, VENT[1] + 3, VENT[2] - 3, VENT[3] - 3], RAD - 3, outline='#374151', width=2)
        d.text((W // 2, 92), f"TUTORIAL {G['num']}", font=INTER('Bold', 30), fill='#7FB2FF', anchor='mm')
        d.text((W // 2, 152), G['titulo'], font=SORA(800, 58), fill='#FFFFFF', anchor='mm')
        hueco = [VX, VY, VX + VW, VY + VH]; rr = RAD - BEZ
    hueco_m = Image.new('L', (W, H), 0); hd = ImageDraw.Draw(hueco_m)
    if FMT == 'h':
        hd.rounded_rectangle(VENT, RAD, fill=255); hd.rectangle([0, 0, W, VY - 1], fill=0)
    else:
        hd.rounded_rectangle(hueco, rr, fill=255)
    bg.putalpha(Image.fromarray((255 - np.array(hueco_m)).astype('uint8')))
    bg.save(f'{TMP}/chrome.png')


def tarjeta(tipo):
    im = fondo().convert('RGBA'); d = ImageDraw.Draw(im); cx = W // 2
    s = 1.0 if FMT == 'h' else 1.15
    if tipo == 'intro':
        ic = Image.open(f'{T}/assets/icono_tut.png').resize((int(170 * s),) * 2, Image.LANCZOS)
        y0 = H // 2 - int(230 * s)
        im.alpha_composite(ic, (cx - ic.width // 2, y0)); y = y0 + ic.height + int(46 * s)
        d.text((cx, y), f"{G.get('zona', 'PANEL PRIVADO')} · TUTORIAL {G['num']}", font=INTER('Bold', int(30 * s)), fill='#7FB2FF', anchor='mm'); y += int(78 * s)
        tf = SORA(800, int(92 * s) if FMT == 'h' else 96)
        for ln in partir(G['titulo'], tf, W - 160): d.text((cx, y), ln, font=tf, fill='#FFFFFF', anchor='mm'); y += int(104 * s)
        d.text((cx, y + 4), G['sub'], font=INTER('Medium', int(38 * s)), fill='#C9D6E8', anchor='mm')
    else:
        y = H // 2 - int(170 * s)
        d.text((cx, y), 'Oscar Polanía', font=SORA(800, int(104 * s)), fill='#FFFFFF', anchor='mm'); y += int(86 * s)
        d.text((cx, y), 'Experto en soluciones digitales', font=INTER('Medium', int(38 * s)), fill='#C9D6E8', anchor='mm'); y += int(60 * s)
        d.line([(cx - 160, y), (cx + 160, y)], fill='#2F6FD0', width=3); y += int(70 * s)
        if G.get('siguiente'):
            d.text((cx, y), 'SIGUIENTE', font=INTER('Bold', int(28 * s)), fill='#FDBA74', anchor='mm'); y += int(58 * s)
            tf = SORA(700, int(50 * s))
            for ln in partir(f"{G['num'] + 1}. {G['siguiente']}", tf, W - 160): d.text((cx, y), ln, font=tf, fill='#FFFFFF', anchor='mm'); y += int(64 * s)
    im.save(f'{TMP}/{tipo}.png')


def partir(txt, font, ancho):
    out, cur = [], ''
    for w in txt.split():
        p = (cur + ' ' + w).strip()
        if font.getlength(p) <= ancho or not cur: cur = p
        else: out.append(cur); cur = w
    return out + [cur] if cur else out


# ---------------- subtítulos ASS ----------------
def ts(x):
    x = max(0, x); h = int(x // 3600); m = int(x % 3600 // 60); s = x % 60
    return f'{h}:{m:02d}:{s:05.2f}'


def vtt(path):
    out = []
    for blk in open(path, encoding='utf-8').read().strip().split('\n\n'):
        ls = blk.strip().split('\n')
        for i, l in enumerate(ls):
            m = re.match(r'(\d+):(\d+):(\d+)[,.](\d+) --> (\d+):(\d+):(\d+)[,.](\d+)', l)
            if m:
                g = [int(v) for v in m.groups()]
                a = g[0] * 3600 + g[1] * 60 + g[2] + g[3] / 1000; b = g[4] * 3600 + g[5] * 60 + g[6] + g[7] / 1000
                out.append((a, b, ' '.join(ls[i + 1:]).strip()))
    return out


def subtitulos():
    fs = 44 if FMT == 'h' else 50
    maxc = 52 if FMT == 'h' else 30
    mv = 40 if FMT == 'h' else 70
    cab = f"""[Script Info]
ScriptType: v4.00+
PlayResX: {W}
PlayResY: {H}
WrapStyle: 2

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: S,Inter,{fs},&H00FFFFFF,&H00FFFFFF,&H00402A0A,&H96402A0A,-1,0,0,0,100,100,0,0,3,14,0,2,80,80,{mv},1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""
    ev = []
    for e in esc:
        for a, b, txt in vtt(f"{VD}/{e['id']}.vtt"):
            pals = txt.split(); import math
            kk = max(1, math.ceil(len(txt) / (maxc * 2 - 4))); meta = len(txt) / kk
            trozos = []; cur = []
            for w in pals:   # trozos parejos de máx. 2 renglones
                if cur and len(trozos) < kk - 1 and (len(' '.join(cur + [w])) > meta + 6 or len(' '.join(cur + [w])) > maxc * 2 - 4):
                    trozos.append(cur); cur = []
                cur.append(w)
            if cur: trozos.append(cur)
            n = sum(len(' '.join(c)) for c in trozos); t0 = a
            for c in trozos:
                s_ = ' '.join(c); dt = (b - a) * len(s_) / max(1, n)
                if len(s_) > maxc and len(c) > 1:
                    best = min(range(1, len(c)), key=lambda k: abs(len(' '.join(c[:k])) - len(' '.join(c[k:]))))
                    s_ = ' '.join(c[:best]) + r'\N' + ' '.join(c[best:])
                ev.append([e['voz'] + t0, min(e['voz'] + t0 + dt + 0.25, e['t0'] + e['T']), s_])
                t0 += dt
    ev.sort(key=lambda x: x[0])
    for i in range(len(ev) - 1): ev[i][1] = min(ev[i][1], ev[i + 1][0] - 0.02)
    ev = [f"Dialogue: 0,{ts(a)},{ts(b)},S,,0,0,0,,{x}" for a, b, x in ev]
    open(f'{TMP}/subs.ass', 'w', encoding='utf-8').write(cab + '\n'.join(ev) + '\n')


# ---------------- audio ----------------
def leer(path):
    r = subprocess.run(['ffmpeg', '-v', 'error', '-i', path, '-f', 's16le', '-ac', '2', '-ar', '44100', '-'], capture_output=True)
    return np.frombuffer(r.stdout, '<i2').reshape(-1, 2).astype(np.float32) / 32768


def audio():
    SR = 44100; n = int(TOTAL * SR) + SR
    subprocess.run(['python3', f'{T}/tools/musica.py', str(TOTAL + 0.5), f'{TMP}/musica.wav', str(G['num'])], check=True)
    mus = leer(f'{TMP}/musica.wav'); mus = np.pad(mus, ((0, max(0, n - len(mus))), (0, 0)))[:n]
    voz = np.zeros((n, 2), np.float32); act = np.zeros(n, np.float32)
    for e in esc:
        v = leer(f"{VD}/{e['id']}.mp3"); i = int(e['voz'] * SR); voz[i:i + len(v)] += v[:n - i]; act[i:i + len(v)] = 1
    k = int(.35 * SR); ker = np.ones(k) / k; act = np.convolve(act, ker, 'same')
    gan = 0.30 - 0.20 * np.clip(act, 0, 1)
    mez = voz * 1.05 + mus * gan[:, None]
    mez = mez / max(1, np.abs(mez).max() / 0.95)
    w = wave.open(f'{TMP}/audio.wav', 'wb'); w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR)
    w.writeframes((mez * 32767).astype('<i2').tobytes()); w.close()
    subprocess.run(['ffmpeg', '-y', '-v', 'error', '-i', f'{TMP}/audio.wav', '-af', 'loudnorm=I=-15:TP=-1.5:LRA=11', '-ar', '44100', f'{TMP}/audio_n.wav'], check=True)
    os.replace(f'{TMP}/audio_n.wav', f'{TMP}/audio.wav')


# ---------------- cámara (solo horizontal) ----------------
CUR = REC.get('cur', []); VPW = REC.get('vp', {}).get('width', 1280); VPH = REC.get('vp', {}).get('height', 720)
ZOOM = {e['id']: e.get('zoom', 1.0) for e in G['escenas']}
def cur_en(st):
    if not CUR: return (VPW / 2, VPH / 2)
    k = bisect.bisect_right([c[0] for c in CUR], st) - 1
    if k < 0: return (CUR[0][1], CUR[0][2])
    t0, x0, y0 = CUR[k]
    if k + 1 < len(CUR):
        t1, x1, y1 = CUR[k + 1]
        if st > t1 - 0.65:   # el cursor ya va en camino al siguiente
            q = min(1, (st - (t1 - 0.65)) / 0.65); return (x0 + (x1 - x0) * q, y0 + (y1 - y0) * q)
    return (x0, y0)
def zoom_obj(tout):
    if tout < INTRO or tout >= TOTAL - OUTRO: return 1.0
    for e in esc:
        if tout < e['t0'] + e['T']: return ZOOM.get(e['id'], 1.0)
    return 1.0
CAM = []
def camara():
    z, cx, cy = 1.0, VPW / 2, VPH / 2; a_z = 1 - np.exp(-1 / (FPS * 0.55)); a_c = 1 - np.exp(-1 / (FPS * 0.45))
    for k in range(int(TOTAL * FPS)):
        tout = k / FPS; zt = zoom_obj(tout)
        x, y = cur_en(src_en(tout)) if zt > 1.0 else (VPW / 2, VPH / 2)
        z += (zt - z) * a_z; cx += (x - cx) * a_c; cy += (y - cy) * a_c
        w, h = VPW / z, VPH / z
        CAM.append((min(max(cx - w / 2, 0), VPW - w), min(max(cy - h / 2, 0), VPH - h), w, h))

# ---------------- video ----------------
def video():
    nf = int(TOTAL * FPS)
    sal = f"{OUT}/{ID}_{'16x9' if FMT == 'h' else '9x16'}.mp4"
    fc = ((f"[1:v]format=yuv420p[a];" if FMT == 'h' else f"[1:v]scale={VW}:{VH}:flags=lanczos,format=yuv420p[a];") +
          f"[0:v][a]overlay={VX}:{VY}[b];[b][2:v]overlay=0:0[c];[c]ass={TMP}/subs.ass[d];"
          f"[3:v]format=rgba,fade=t=out:st={INTRO - 0.5}:d=0.5:alpha=1[i];[d][i]overlay=0:0:enable='lt(t,{INTRO})'[e];"
          f"[4:v]format=rgba,fade=t=in:st={TOTAL - OUTRO}:d=0.6:alpha=1[o];[e][o]overlay=0:0:enable='gte(t,{TOTAL - OUTRO})',format=yuv420p[v]")
    entrada = (['-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{VW}x{VH}', '-framerate', str(FPS), '-i', '-'] if FMT == 'h'
               else ['-f', 'image2pipe', '-framerate', str(FPS), '-c:v', 'mjpeg', '-i', '-'])
    if FMT == 'h': camara()
    cmd = ['ffmpeg', '-y', '-v', 'error',
           '-f', 'lavfi', '-i', f'color=c=0x0A2540:s={W}x{H}:r={FPS}:d={TOTAL}'] + entrada + [
           '-loop', '1', '-framerate', str(FPS), '-t', str(TOTAL), '-i', f'{TMP}/chrome.png',
           '-loop', '1', '-framerate', str(FPS), '-t', str(TOTAL), '-i', f'{TMP}/intro.png',
           '-loop', '1', '-framerate', str(FPS), '-t', str(TOTAL), '-i', f'{TMP}/outro.png',
           '-i', f'{TMP}/audio.wav',
           '-filter_complex', fc, '-map', '[v]', '-map', '5:a',
           '-c:v', 'libx264', '-preset', 'veryfast', '-crf', '18', '-pix_fmt', 'yuv420p', '-r', str(FPS),
           '-c:a', 'aac', '-b:a', '192k', '-movflags', '+faststart', '-t', str(TOTAL), sal]
    p = subprocess.Popen(cmd, stdin=subprocess.PIPE)
    cache = {}
    for k in range(nf):
        st = src_en(k / FPS); j = max(0, bisect.bisect_right(fts, st) - 1)
        path = frames[j][1]
        if FMT == 'h':
            if path not in cache: cache.clear(); cache[path] = Image.open(path).convert('RGB')
            im = cache[path]; sx = im.width / VPW
            x, y, w, h = CAM[k]
            p.stdin.write(im.resize((VW, VH), Image.LANCZOS, box=(x * sx, y * sx, (x + w) * sx, (y + h) * sx)).tobytes())
        else:
            if path not in cache: cache.clear(); cache[path] = open(path, 'rb').read()
            p.stdin.write(cache[path])
    p.stdin.close(); p.wait()
    print('listo', sal, p.returncode)


if __name__ == '__main__':
    chrome(); tarjeta('intro'); tarjeta('outro'); subtitulos(); audio(); video()
