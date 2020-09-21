import numpy as np
import matplotlib.pyplot as plt
data_cis = np.loadtxt('cis_timestep')
data_trans = np.loadtxt('trans_timestep')
cis = 0.0
trans = 0.0

x = np.linspace(0,2000,100000)

for idata in range(len(data_cis)):
     nnd = 2000.0
     if data_cis[idata,1] == 0.0 : 
          continue
     h = 20
     cis += 25*((2*np.pi*h**2)**(-0.5))*np.exp(-1*(x-data_cis[idata,1])**2/(2*h**2))

for idata in range(len(data_trans)):
     nnd = 2000.0
     if data_trans[idata,1] == 0.0 : 
          continue
     h = 20
     trans += 25*((2*np.pi*h**2)**(-0.5))*np.exp(-1*(x-data_trans[idata,1])**2/(2*h**2))

plt.hist(data_trans[:,1], bins = 80,linewidth=2, range = (0,2000), fill=False)
plt.hist(data_cis[:,1], bins = 80,linewidth=2, range = (0,2000), fill=False)  
plt.plot(x,cis)
plt.plot(x,trans)
plt.show()
