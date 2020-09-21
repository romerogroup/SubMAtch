import numpy as np
import matplotlib.pyplot as plt
data_cis = np.loadtxt('cis_timestep')
data_trans = np.loadtxt('trans_timestep')
cis = 0
x = np.linspace(0,1000,10000)
for idata in range(len(data_cis)):
#    nnd = 1000
#    for jdata in range(len(data_cis)):
#        if idata == jdata :
#            continue 
#        temp = abs(data_cis[idata,1]-data_cis[jdata,1])
#        nnd = min(temp,nnd) 
#        print('2h'+str(nnd))
#        h = nnd/2
#    print('2h'+str(nnd))
    h = 0.25
    cis += 1/((2*np.pi*h)**(-0.5))*np.exp(-1*(x-data_cis[idata,1])**2/2*h**2)

plt.hist(data_cis[:,1], bins = 40, edgecolor='#8B0000',linewidth=2, range = (0,1000), fill=False)    
plt.plot(x,cis)
plt.show()
