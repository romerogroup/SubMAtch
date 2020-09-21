import numpy as np
import matplotlib.pyplot as plt
import sys
s0_pop = np.loadtxt('S0_pop')
s1_pop = np.loadtxt('S1_pop')
#for w in range(1001,200001):
#	s0_pop = np.append(s0_pop,[[w,1]],axis=0)
#	s1_pop = np.append(s1_pop,[[w,0]],axis=0)
der_s0 = []

for i in range(0, len(s0_pop)-1):
	#print('step='+str(i)+','+str((s0_pop[i+1,1]-s0_pop[i,1]) / (s0_pop[i+1,0]-s0_pop[i,0])))
	der_s0.append( (s0_pop[i+1,1]-s0_pop[i,1]) / (s0_pop[i+1,0]-s0_pop[i,0]) )
der_s0.append(der_s0[len(der_s0)-1])
pnt=int(sys.argv[1])
pnt2=int(sys.argv[2])
plt.plot(s0_pop[:,0],s0_pop[:,1])
plt.plot(s1_pop[:,0],s1_pop[:,1])
plt.savefig('population.png')

for i in range(0,len(s0_pop)):
	k=0
	sum1=0
	sum2=0
	for j in range((-1)*(pnt/2),(pnt/2)+1):
		if j+i >= 0 and j+i < len(s0_pop):
			k = k + 1
			sum1 = sum1 + s0_pop[i+j,1] 
			sum2 = sum2 + s1_pop[i+j,1]
	s0_pop[i,1] = sum1/k
	s1_pop[i,1] = sum2/k

plt.plot(s0_pop[:,0],s0_pop[:,1])
plt.plot(s1_pop[:,0],s1_pop[:,1])
plt.grid(True, which = 'major' )
plt.grid(True, which = 'minor' )
plt.minorticks_on()
plt.savefig('smooth_pop')
plt.clf()
der_s0 = []

for i in range(0, len(s0_pop)-1):
	der_s0.append( (s0_pop[i+1,1]-s0_pop[i,1]) / (s0_pop[i+1,0]-s0_pop[i,0]) )
der_s0.append(der_s0[len(der_s0)-1])
plt.plot(s0_pop[:,0],der_s0)
plt.grid(True, which = 'major' )
plt.grid(True, which = 'minor' )
plt.minorticks_on()
plt.savefig('der_smooth')
plt.clf()
np.savetxt('der_prime',der_s0)
fft = abs(np.fft.rfft(der_s0))
size = s0_pop[:,0].size
timestep = (s0_pop[0,0]-s0_pop[0,1])*0.001
freq = np.fft.rfftfreq(size , d=timestep)

for i in range(0,len(fft)):
	k=0
	sum=0
	for j in range((-1)*(pnt2/2),(pnt2/2)+1):
		if j+i >= 0 and j+i < len(fft):
			k = k + 1
			sum = sum + fft[i+j] 
	fft[i] = sum/k

print(fft)
print(freq)
plt.plot(freq, fft)
plt.grid(True, which = 'major' )
plt.grid(True, which = 'minor' )
plt.minorticks_on()
plt.xlim([0,60])
plt.ylim([0,3])
plt.xlabel('Frequency (THz)', fontsize=20)
plt.ylabel('Magnitude', fontsize=20)
plt.savefig('fft')
plt.clf()
# for j in range(0,100):
	# for i in range(0, len(s0_pop)-1 ):
		# s0_pop[i,0] = (s0_pop[i,0]+s0_pop[i+1,0])/2
		# s0_pop[i,1] = (s0_pop[i,1]+s0_pop[i+1,1])/2
		# s1_pop[i,0] = (s1_pop[i,0]+s1_pop[i+1,0])/2
		# s1_pop[i,1] = (s1_pop[i,1]+s1_pop[i+1,1])/2
		# der_s0[i] = (s0_pop[i+1,1]-s0_pop[i,1]) / (s0_pop[i+1,0]-s0_pop[i,0])
		# # fft = np.fft.rfft(der_s0)
		# # size = s0_pop[:,0].size
		# # timestep = s0_pop[1,0]-s0_pop[0,1]
		# # freq = np.fft.rfftfreq(size , d=timestep)
	# # np.savetxt('s0_prime'+str(j),s0_pop)
	# # np.savetxt('s1_prime'+str(j),s1_pop)
	# plt.plot(s0_pop[:,0],s0_pop[:,1])
	# plt.plot(s1_pop[:,0],s1_pop[:,1])
	# plt.savefig('prime'+str(j))
	# plt.clf()
	# plt.plot(s1_pop[:,0],der_s0)
	# plt.savefig('der'+str(j))
	# plt.clf()
	# # plt.plot(freq, fft)
	# # plt.savefig('fft'+str(j))
	# # plt.clf()
# np.savetxt('der',der_s0)
# np.savetxt('s0_prime',s0_pop)
