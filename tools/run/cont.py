import sys,numpy as np
rom=open(sys.argv[1],'rb').read(); cap=[l.split() for l in open(sys.argv[2])]
R=float(sys.argv[3]) if len(sys.argv)>3 else 14546.0
t=np.array([float(a) for a,b in cap]); v=np.array([int(b) for a,b in cap]).astype(np.uint8)
# find frame starts: block k sample 0..15
starts=[]
k0=None
for k in range(1,121):
    blk=np.frombuffer(rom[k*16384+0x40:k*16384+0x40+1472],np.uint8)
    idx=np.where(v==blk[0])[0]
    for s in idx:
        if s+16<=len(v) and (v[s:s+16]==blk[:16]).all(): starts.append((k,s)); break
# source time of each captured sample = k/12 + (position-in-frame)/R ; frames may start at j0=0 or 2 (H: P7/P8 are idx 0/1)
src=np.full(len(v),np.nan)
for (k,s),(k2,s2) in zip(starts,starts[1:]+[(None,len(v))]):
    n=s2-s
    for j in range(min(n,1472)):
        src[s+j]=k/12.0+j/R
ok=~np.isnan(src)
d=src[ok]-t[ok]
# remove a linear trend (clock ratio between video grid and emulated time)
p=np.polyfit(t[ok]-t[ok][0],d,1); dd=d-np.polyval(p,t[ok]-t[ok][0])
# jumps at frame boundaries
steps=[]
for (k,s),(k2,s2) in zip(starts,starts[1:]):
    if s2-1<len(v) and s2>0 and ok[s2-1] and ok[s2]:
        steps.append((src[s2]-t[s2])-(src[s2-1]-t[s2-1]))
steps=np.array(steps)*R   # in samples
print('boundaries %d | time jump at frame boundary (samples): mean %+.2f  rms %.2f  max|.| %.2f'%(len(steps),steps.mean(),np.sqrt((steps**2).mean()),np.abs(steps).max()))
