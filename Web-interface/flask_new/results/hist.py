import numpy as np
import os
import csv
import sys
import matplotlib.pyplot as plt
f = open(sys.argv[1])
l = f.readlines()


for icolumn in range(len(l[1].split())-3):
    cis = []
    trans = [] 
    total = []
    for iline in range(1,len(l)) :
        temp = l[iline].split()
        datum = float(temp[icolumn+2])
        if datum == 0 :
            continue
        if temp[1] == 'cis' :
            cis.append(datum)
            total.append(datum)
        if temp[1] == 'trans' :
            trans.append(datum)
            total.append(datum)
    if icolumn == 0 :
        mxt = max(cis)
        if mxt <= 1000 :
            rg = (0,1000)
            bins = 40
            x = np.linspace(0,1000,10000)
            h = 20
        elif mxt > 1000 :
            rg = (0,1000)
            bins = 80
            x = np.linspace(0,2000,10000)
            h = 15
    else :
        rg = (0,180)
        bins = 18
        x = np.linspace(0,180,10000)
        h = 5
    cis_est = 0.0
    trans_est = 0.0
    for i in range(0,len(cis)):
        if cis[i] == 0.0 : 
            continue
        cis_est += rg[1]/bins*((2*np.pi*h**2)**(-0.5))*np.exp(-1*(x-cis[i])**2/(2*h**2))
                        
    for i in range(0,len(trans)):
        if trans[i] == 0.0 : 
            continue
        trans_est += rg[1]/bins*((2*np.pi*h**2)**(-0.5))*np.exp(-1*(x-trans[i])**2/(2*h**2))
    plt.plot(x,cis_est,color = 'r',linewidth=4)
    plt.plot(x,trans_est,color = 'b',linewidth=4)

    cis_label = '$cis$'+str(int(len(cis)/float(len(total))*100))+'%'
    trans_label = '$trans$'+str(int(len(trans)/float(len(total))*100))+'%'

    plt.hist(cis,bins = bins, range = rg, edgecolor='#8B0000',linewidth=2, hatch="\\\\", fill=False,  label=cis_label)
    plt.hist(trans,bins = bins,range = rg,  edgecolor='#0000CD',linewidth=2, hatch='////', fill=False,alpha=0.9,  label=trans_label)
    plt.hist(total, bins = bins, range = rg, edgecolor='k',linewidth=2,fill=False, hatch='X', alpha=0.7, label='Total')
    plt.legend()
    plt.show()
    plt.clf()
