import sys,os,json,warnings
warnings.filterwarnings('ignore')
from PIL import Image,ImageChops
ref,cur=sys.argv[1],sys.argv[2]; out={}
for f in sys.argv[3:]:
    a=os.path.join(ref,f); b=os.path.join(cur,f)
    if not os.path.exists(a): out[f]={"miss":1}; continue
    A=Image.open(a).convert('RGB'); B=Image.open(b).convert('RGB')
    if A.size!=B.size: out[f]={"size":f"{A.size}→{B.size}","px":1}; continue
    d=ImageChops.difference(A,B); bb=d.getbbox()
    if not bb: out[f]={"px":0}; continue
    n=sum(1 for p in list(d.crop(bb).getdata()) if p!=(0,0,0)); out[f]={"px":n}
    m=B.copy(); r=Image.new('RGB',B.size,(255,0,0)); m.paste(r,mask=d.convert('L').point(lambda v:255 if v else 0)); m.save(os.path.join(os.path.dirname(ref),'diff_'+f))
print(json.dumps(out))
