import numpy as np, sys
vram=np.fromfile(sys.argv[1],np.uint8)
states=np.load(sys.argv[2] if len(sys.argv)>2 else __import__('os').path.dirname(__import__('os').path.abspath(__file__))+'/states.npy')
img=np.empty((216,256),np.uint8)
v=vram.reshape(216,128)
img[:,0::2]=v>>4; img[:,1::2]=v&15
best=[(int((img!=s).sum()),i) for i,s in enumerate(states)]
best.sort()
print('closest states:',best[:4], 'pixels', img.size)
