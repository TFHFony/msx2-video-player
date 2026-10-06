import sys,numpy as np
p=sys.argv[1]
r=[float(l.split()[1]) for l in open(p+'_info.txt')]
d=np.diff(r)*1000
print('frame ms mean %.3f min %.3f max %.3f'%(d.mean(),d.min(),d.max()))
w=np.array([float(x) for x in open(p+'_wt.txt')]); iv=np.diff(w)*1e6
g=iv[iv<200]
print(len(w),'sample interval mean(no gaps) %.2f us = %.0f Hz'%(g.mean(),1e6/g.mean()),'gaps',np.round(np.sort(iv)[-4:],0))
