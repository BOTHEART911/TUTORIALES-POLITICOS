import json, sys, bisect
from PIL import Image
d = sys.argv[1]; r = json.load(open(d + '/rec.json'))
ts = [f[0] for f in r['frames']]; m = r['marcas']
picks = []
for i in range(len(m) - 1):
    a, b = m[i][1], m[i + 1][1]
    for q in (0.35, 0.95):
        t = a + (b - a) * q; k = max(0, min(len(ts) - 1, bisect.bisect_left(ts, t)))
        picks.append(r['frames'][k][1])
ims = [Image.open(p) for p in picks]; w = 640 if r['fmt'] == 'h' else 260
ims = [im.resize((w, int(im.height * w / im.width))) for im in ims]
cols = 4 if r['fmt'] == 'h' else 8; h = ims[0].height
out = Image.new('RGB', (w * cols, h * ((len(ims) + cols - 1) // cols)), 'white')
for i, im in enumerate(ims): out.paste(im, ((i % cols) * w, (i // cols) * h))
out.save(sys.argv[2]); print([x[0] for x in m], len(ts))
