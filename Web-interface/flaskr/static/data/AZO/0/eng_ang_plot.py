import numpy as np
import matplotlib.pyplot as plt

homo_vs_angle = np.loadtxt('homo_vs_angle')
lumo_vs_angle = np.loadtxt('lumo_vs_angle')

plt.plot(homo_vs_angle[:,0], homo_vs_angle[:,1], label='HOMO')
plt.plot(lumo_vs_angle[:,0], lumo_vs_angle[:,1], label='LUMO')
plt.xticks(np.arange(0, 180, 10))
plt.legend(loc=4)
plt.xlabel('Angle', fontsize=20)
plt.ylabel('Energy(eV)', fontsize=20)
plt.grid(True)
plt.savefig('energy_vs_angle.png')
plt.clf()
delta = lumo_vs_angle[:,1] - homo_vs_angle [:,1]
plt.plot(homo_vs_angle[:,0],delta)
plt.xticks(np.arange(0, 180, 10))
plt.xlabel('Angle', fontsize=20)
plt.ylabel('Energy(eV)', fontsize=20)
plt.grid(True)
plt.savefig('delta_E.png')
