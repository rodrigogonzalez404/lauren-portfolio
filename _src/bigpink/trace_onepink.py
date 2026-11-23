import numpy as np, potrace, cv2
from PIL import Image
a=np.asarray(Image.open('/workspace/bigpink/media/logo-4.jpg').convert('L'),np.float32)
x0,x1,y0,y1=1030,1280,430,2120
c=a[y0:y1,x0:x1]
S=4
big=cv2.resize(c,None,fx=S,fy=S,interpolation=cv2.INTER_CUBIC)
big=cv2.GaussianBlur(big,(0,0),1.6)
m=(big>165).astype(np.uint8)
n,lab,st,_=cv2.connectedComponentsWithStats(m)
keep=np.zeros_like(m)
for i in range(1,n):
    if st[i,cv2.CC_STAT_AREA]>3000*S: keep[lab==i]=1
print('components kept',int(sum(st[i,cv2.CC_STAT_AREA]>3000*S for i in range(1,n))))
Image.fromarray(keep*255).resize((keep.shape[1]//8,keep.shape[0]//8)).save('/tmp/mask.png')
def trace(mask):
    bmp=potrace.Bitmap(~mask.astype(bool))
    path=bmp.trace(turdsize=50,alphamax=1.0,opticurve=True,opttolerance=0.3)
    d=[]
    for curve in path:
        s0=curve.start_point; d.append(f'M{s0.x:.1f},{s0.y:.1f}')
        for seg in curve.segments:
            if seg.is_corner: d.append(f'L{seg.c.x:.1f},{seg.c.y:.1f}L{seg.end_point.x:.1f},{seg.end_point.y:.1f}')
            else: d.append(f'C{seg.c1.x:.1f},{seg.c1.y:.1f} {seg.c2.x:.1f},{seg.c2.y:.1f} {seg.end_point.x:.1f},{seg.end_point.y:.1f}')
        d.append('Z')
    return ''.join(d)
comps=sorted([i for i in range(1,n) if st[i,cv2.CC_STAT_AREA]>3000*S],key=lambda i:-st[i,cv2.CC_STAT_TOP])
one=np.isin(lab,comps[:3]).astype(np.uint8); pink=np.isin(lab,comps[3:]).astype(np.uint8)
D1,D2=trace(one),trace(pink)
ys,xs=np.nonzero(keep); bx0,bx1,by0,by1=xs.min(),xs.max()+1,ys.min(),ys.max()+1
w,h=bx1-bx0,by1-by0
g=lambda tr:f'<g transform="{tr}"><path class="w1" fill="currentColor" fill-rule="evenodd" d="{D1}"/><path class="w2" fill="currentColor" fill-rule="evenodd" d="{D2}"/></g>'
open('onepink-vertical.svg','w').write(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{bx0} {by0} {w} {h}">'+g('')+'</svg>')
open('onepink-h.svg','w').write(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {h} {w}">'+g(f'translate({h},0) rotate(90) translate({-bx0},{-by0})')+'</svg>')
print(w,h,len(D1),len(D2))
