import json,bisect,sys
from PIL import Image, ImageDraw
d=sys.argv[1]; esc=sys.argv[2].split(','); out=sys.argv[3]
R=json.load(open(d+'/rec.json')); fr=R['frames']; ts=[f[0] for f in fr]; mk=R['marcas']; nm=[m[0] for m in mk]
ims=[]
for s in esc:
  i=nm.index(s); a,b=mk[i][1],mk[i+1][1]
  for q in [k/6 for k in range(1,6)]:
    k=max(0,bisect.bisect_right(ts,a+(b-a)*q)-1); im=Image.open(fr[k][1]); im.thumbnail((640,480)); ImageDraw.Draw(im).text((8,8),f'{s}@{q:.2f}',fill='red'); ims.append(im)
w,h=ims[0].size; c=5; r=(len(ims)+c-1)//c; S=Image.new('RGB',(w*c,h*r),'white')
for i,im in enumerate(ims): S.paste(im,((i%c)*w,(i//c)*h))
S.save(out)
