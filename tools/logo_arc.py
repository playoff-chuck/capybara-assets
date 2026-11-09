#!/usr/bin/env python3
"""V496: Logo C1 – Schrift des Logos in engeren Bogen (R=200) biegen, hinter das Capybara legen (Martin 09.11. 11:26).
Aufruf: python3 tools/logo_arc.py <quelle logo_main.webp (alt, V258)> <ziel.png> [R=200] [OFF=6]"""
import numpy as np, sys
from PIL import Image
from scipy.ndimage import map_coordinates, binary_dilation, label
im=np.array(Image.open(sys.argv[1]).convert('RGBA')).astype(float)
out_path=sys.argv[2]; R1=float(sys.argv[3]) if len(sys.argv)>3 else 200.0; OFF=int(sys.argv[4]) if len(sys.argv)>4 else 6
H,W=im.shape[:2]
yy,xx=np.mgrid[0:H,0:W]
R_,G_,B_=im[...,0],im[...,1],im[...,2]
blue=(B_>R_+10)&(im[...,3]>40); lum=(R_+G_+B_)/3
bd=binary_dilation(blue,iterations=3)
bd6=binary_dilation(blue,iterations=6)
shadow=(R_>B_+25)&(lum<120)
ell=(((xx-250)/70)**2+((yy-134)/52)**2<1)
hat=ell&((yy>116)|blue|(bd&(lum<60))|(bd6&~shadow))
body=(yy>150)&(xx>140)&(xx<440)
mas=(hat|body)&(im[...,3]>0)
bd2=binary_dilation(blue,iterations=2)
mas=mas&~((yy<104)&~bd2)
lb,n=label(mas); sz=np.bincount(lb.ravel()); sz[0]=0; mas=lb==sz.argmax()
cx=280.0; R0=593.0; cy0=5+R0
r=np.hypot(xx-cx,yy-cy0)
textmask=(~mas)&(r>R0-175)&(r<R0+8)
T=im.copy(); T[~textmask]=0
M=im.copy(); M[~mas]=0
T[ell&bd6&(yy>=86)]=0
A=T[...,3]>128
def bot(x):
    ys=np.nonzero(A[:135,x])[0]; return ys.max() if len(ys) else None
edge=[x for x in list(range(150,172))+list(range(330,352)) if bot(x) is not None]
rb=np.median([np.hypot(x-cx,bot(x)-cy0) for x in edge])
sc=np.median([T[bot(x)-6,x,:3] for x in edge],axis=0); oc=np.median([T[bot(x),x,:3] for x in edge],axis=0)
for x in range(172,330):
    b=bot(x); yb=int(round(cy0-np.sqrt(max(0,rb**2-(x-cx)**2))))
    if b is None: b=bot(x-1) or bot(x+1) or yb
    b=min(b,yb)
    for y in range(b+1,yb+1):
        T[y,x,:3]=oc if y>yb-3 else sc; T[y,x,3]=255
def rewarp(R1,outW=760,outH=560,top=10):
    Rm0=R0-55; Rm1=R1-55
    cy1=top+R1; ocx=outW/2
    oy,ox=np.mgrid[0:outH,0:outW].astype(float)
    rr=np.hypot(ox-ocx,oy-cy1); th=np.arctan2(ox-ocx,cy1-oy)
    s=th*Rm1; th0=s/Rm0; r0=rr-R1+R0
    sx=cx+r0*np.sin(th0); sy=cy0-r0*np.cos(th0)
    out=np.zeros((outH,outW,4))
    for c in range(4): out[...,c]=map_coordinates(T[...,c],[sy,sx],order=1,mode='constant',cval=0)
    out[(rr<R1-180)|(rr>R1+10)]=0
    return out
tA=Image.fromarray(np.clip(rewarp(R1),0,255).astype('uint8'))
tA=tA.crop(tA.getbbox()); tw,th_=tA.size
a=np.array(tA)[:,:,3]; col=a[:,tw//2]; nz=np.nonzero(col>20)[0]; tbc=nz.max() if len(nz) else th_
can=Image.new('RGBA',(760,760),(0,0,0,0))
can.alpha_composite(tA,((760-tw)//2,0))
can.alpha_composite(Image.fromarray(M.astype('uint8')),((760-W)//2,tbc-88+OFF))
can=can.crop(can.getbbox()); can.save(out_path); print(can.size)
