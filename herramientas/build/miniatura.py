"""Miniaturas: python3 miniatura.py <guion.json>
Usa G['mini'] = {texto, linea2, escena_h, q_h, escena_v, q_v, recorte_h:[x0,y0,x1,y1] (fracción)}"""
import json, sys, bisect, os
from PIL import Image, ImageDraw, ImageFont, ImageFilter
T = '/home/claude/tut'; G = json.load(open(sys.argv[1])); ID = G['id']; M = G['mini']
OUT = f'{T}/out/{ID}'; os.makedirs(OUT, exist_ok=True)
SORA = lambda w, s: ImageFont.truetype(f'{T}/fuente/ttf/Sora-{w}.ttf', s)
INTER = lambda n, s: ImageFont.truetype(f'/usr/share/fonts/opentype/inter/Inter-{n}.otf', s)


def frame(fmt, esc, q):
    R = json.load(open(f'{T}/rec/{ID}_{fmt}/rec.json')); mk = R['marcas']; ts = [f[0] for f in R['frames']]
    i = [m[0] for m in mk].index(esc); a, b = mk[i][1], mk[i + 1][1]
    k = max(0, bisect.bisect_right(ts, a + (b - a) * q) - 1)
    return Image.open(R['frames'][k][1]).convert('RGB')


def fondo(W, H):
    im = Image.new('RGB', (W, H), '#0A2540'); d = ImageDraw.Draw(im)
    for y in range(H): k = y / H; d.line([(0, y), (W, y)], fill=(int(10 + 10 * k), int(37 + 22 * k), int(64 + 46 * k)))
    g = Image.new('L', (W, H), 0); ImageDraw.Draw(g).ellipse([W * .45, -H * .2, W * 1.25, H * .9], fill=120)
    return Image.composite(Image.new('RGB', (W, H), '#1d6fe6'), im, g.filter(ImageFilter.GaussianBlur(W // 8)))


def tarjeta(img, radio, borde=0):
    m = Image.new('L', img.size, 0); ImageDraw.Draw(m).rounded_rectangle([0, 0, img.width - 1, img.height - 1], radio, fill=255)
    out = img.convert('RGBA'); out.putalpha(m); return out


def sombra(base, card, x, y, blur=30, alpha=170):
    sh = Image.new('RGBA', base.size, (0, 0, 0, 0)); a = card.split()[3].point(lambda v: alpha if v else 0)
    s2 = Image.new('RGBA', card.size, (0, 0, 0, 255)); s2.putalpha(a); sh.alpha_composite(s2, (x + 10, y + 24))
    base.alpha_composite(sh.filter(ImageFilter.GaussianBlur(blur))); base.alpha_composite(card, (x, y))


def lineas(d, txt, font, ancho):
    out, cur = [], ''
    for w in txt.split():
        p = (cur + ' ' + w).strip()
        if font.getlength(p) <= ancho or not cur: cur = p
        else: out.append(cur); cur = w
    return out + [cur]


def pastilla(d, x, y, txt, font, fondo_='#C2410C', color='#FFFFFF', pad=(22, 12)):
    w = font.getlength(txt); h = font.size
    d.rounded_rectangle([x, y, x + w + pad[0] * 2, y + h + pad[1] * 2], (h + pad[1] * 2) // 2, fill=fondo_)
    d.text((x + pad[0], y + pad[1] + h / 2), txt, font=font, fill=color, anchor='lm')
    return y + h + pad[1] * 2


# ---------- horizontal 1280x720 ----------
W, H = 1280, 720
im = fondo(W, H).convert('RGBA'); d = ImageDraw.Draw(im)
f = frame('h', M['escena_h'], M['q_h']); r = M.get('recorte_h', [0, 0, 1, 1])
f = f.crop((int(r[0] * f.width), int(r[1] * f.height), int(r[2] * f.width), int(r[3] * f.height)))
k = min(560 / f.width, 540 / f.height); f = f.resize((int(f.width * k), int(f.height * k)), Image.LANCZOS)
card = tarjeta(f, 26).rotate(-4, resample=Image.BICUBIC, expand=True)
sombra(im, card, W - card.width - 30, (H - card.height) // 2 + 10)
d = ImageDraw.Draw(im)
y = 70
y = pastilla(d, 64, y, f"TUTORIAL {G['num']} · {G.get('zona', 'PANEL PRIVADO')}", INTER('Bold', 24), fondo_='#0063D8') + 30
tam = 96
while True:
    tf = SORA(800, tam); ls = lineas(d, M['texto'], tf, 600)
    if (len(ls) <= 2 and max(tf.getlength(l) for l in ls) <= 600) or tam <= 60: break
    tam -= 4
for ln in ls:
    d.text((60, y), ln, font=tf, fill='#FFFFFF'); y += int(tam * 1.13)
y += 10
d.text((64, y), M['linea2'], font=INTER('SemiBold', 38), fill='#FDBA74')
ic = Image.open(f'{T}/assets/icono_tut.png').resize((64, 64), Image.LANCZOS); im.alpha_composite(ic, (64, H - 64 - 48))
d.text((144, H - 80), 'Oscar Polanía', font=INTER('Bold', 26), fill='#FFFFFF', anchor='lm')
im.convert('RGB').save(f'{OUT}/{ID}_miniatura_16x9.jpg', quality=92)

# ---------- vertical 1080x1920 ----------
W, H = 1080, 1920
im = fondo(W, H).convert('RGBA'); d = ImageDraw.Draw(im)
y = 130
fp = INTER('Bold', 34); tw = fp.getlength(f"TUTORIAL {G['num']} · {G.get('zona', 'PANEL PRIVADO')}") + 44
pastilla(d, int((W - tw) / 2), y, f"TUTORIAL {G['num']} · {G.get('zona', 'PANEL PRIVADO')}", fp, fondo_='#0063D8'); y += 120
tam = 124
while True:
    tf = SORA(800, tam); ls = lineas(d, M['texto'], tf, W - 110)
    if len(ls) <= 2 or tam <= 80: break
    tam -= 6
for ln in ls:
    d.text((W // 2, y), ln, font=tf, fill='#FFFFFF', anchor='mt'); y += int(tam * 1.12)
d.text((W // 2, y + 16), M['linea2'], font=INTER('SemiBold', 50), fill='#FDBA74', anchor='mt'); y += 110
f = frame('v', M['escena_v'], M['q_v']); f = f.resize((760, int(f.height * 760 / f.width)), Image.LANCZOS)
alto = H - y - 40
f = f.crop((0, 0, 760, min(f.height, alto - 40)))
bez = Image.new('RGBA', (f.width + 28, f.height + 28), (17, 24, 39, 255)); bez = tarjeta(bez, 70)
bez.alpha_composite(tarjeta(f, 56), (14, 14))
bez = bez.rotate(-3, resample=Image.BICUBIC, expand=True)
sombra(im, bez, (W - bez.width) // 2 + 20, y)
im.convert('RGB').save(f'{OUT}/{ID}_miniatura_9x16.jpg', quality=92)
print('ok')
