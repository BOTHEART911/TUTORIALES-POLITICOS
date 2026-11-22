import json, sys, bisect
from PIL import Image, ImageDraw
d=sys.argv[1]; R=json.load(open(d+'/rec.json')); fr=R['frames']; ts=[f[0] for f in fr]; mk=R['marcas']
pts=[]
for i in range(len(mk)-1):
    a,b=mk[i][1],mk[i+1][1]
    for q in (0.35,0.98): pts.append((mk[i][0]+f'@{q}',a+(b-a)*q))
ims=[]
for name,t in pts:
    k=max(0,bisect.bisect_right(ts,t)-1); im=Image.open(fr[k][1]); im.thumbnail((640,640)); ImageDraw.Draw(im).text((8,8),name,fill='red'); ims.append(im)
w,h=ims[0].size; cols=4 if w>h else 6; rows=(len(ims)+cols-1)//cols
S=Image.new('RGB',(w*cols,h*rows),'white')
for i,im in enumerate(ims): S.paste(im,((i%cols)*w,(i//cols)*h))
S.save(sys.argv[2]); print(len(fr),'frames', [(m[0],round(m[1]-mk[0][1],1)) for m in mk])
