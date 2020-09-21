import numpy as np
import matplotlib.pyplot as plt
import matplotlib.figure 
import matplotlib.colors as color
import matplotlib.image as mpimg

def calc_prec(ni,nt,iso_type):		# ni=number of transition to an isomer, nt= total, iso_type= isomer type
	np=(ni/nt)*100
 	np="%.2f" % np
	np='$'+iso_type+'$'+' ('+str(np)+'%)'
	return np

def load_and_plot(cis,trans,ntotal,out_plot,typ) :			# cisfn=cis filename, transfn= trans file name , typ=Angle,Time
	
	total = np.append(cis, trans, axis=0)
	ncis = float(len(cis))
	ntrans = float(len(trans))
	not_relaxed = "%.2f" % ((1-((ncis+ntrans)/ntotal))*100)
	img=mpimg.imread('image.png')
	fig=plt.figure()
	
	if typ=='Angle' :
		bins = 18
		rg=(0,180)
		unit= ''
                x = np.linspace(0,180,100000)
                h = 5
                
	elif typ=='Time' :
		bins = 32
		rg=(0,2000)
		unit=' (fs)'
                x = np.linspace(0,2000,100000)
                h = 20
        cis_est = 0.0
        trans_est = 0.0
        
       
        for i in range(0,len(cis)):
                if cis[i,1] == 0.0 : 
                        continue
                cis_est += rg[1]/bins*((2*np.pi*h**2)**(-0.5))*np.exp(-1*(x-cis[i,1])**2/(2*h**2))
                        
        for i in range(0,len(trans)):
                if trans[i,1] == 0.0 : 
                        continue
                trans_est += rg[1]/bins*((2*np.pi*h**2)**(-0.5))*np.exp(-1*(x-trans[i,1])**2/(2*h**2))
        plt.plot(x,cis_est,color = 'r')
        plt.plot(x,trans_est,color = 'b')

        ax= fig.add_subplot(1,1,1)
	ax.hist(cis[:,1], bins = bins, edgecolor='#8B0000',linewidth=2, range = rg, hatch="\\\\", fill=False,  label=calc_prec(ncis,ntotal,'cis'))
	ax.hist(trans[:,1], bins = bins, edgecolor='#0000CD',linewidth=2, range = rg, hatch='////', fill=False,alpha=0.9,  label=calc_prec(ntrans,ntotal,'trans'))
	ax.hist(total[:,1], bins = bins, edgecolor='k',linewidth=2, range = rg,fill=False, hatch='X', alpha=0.7, label='Total')
	plt.grid(True, which = 'major')
	plt.grid(True, which = 'minor')
	plt.minorticks_on()
	#if not_relaxed !=0 :
	#	ax.text(720, 28, 'Not relaxed(' + str(not_relaxed)+'%)', fontsize=12)
	plt.legend()
	plt.xlabel(typ+unit, fontsize=20)
	plt.ylabel("Count", fontsize=20)
	ax= fig.add_subplot(3,4,8)
	plt.axis("off")
	ax.imshow(img)
	plt.savefig(out_plot+'.png', format='png')

cis_angle = np.loadtxt('cis_angle')
trans_angle = np.loadtxt('trans_angle')
cis_timestep = np.loadtxt('cis_timestep')
trans_timestep = np.loadtxt('trans_timestep')

new_cis_angle = np.array([[0,0]])
new_trans_angle = np.array([[0,0]])
new_cis_timestep = np.array([[0,0]])
new_trans_timestep = np.array([[0,0]])

for i in range(0,len(cis_timestep)):
	if cis_timestep[i,1] != 0 :
		new_cis_timestep = np.append(new_cis_timestep,np.array([[cis_timestep[i,0],cis_timestep[i,1]]]), axis=0)
		new_cis_angle = np.append(new_cis_angle, np.array([[cis_angle[i,0],cis_angle[i,1]]]), axis=0)

for i in range(0,len(trans_timestep)):
	if trans_timestep[i,1] != 0 :
		new_trans_timestep = np.append(new_trans_timestep, np.array([[trans_timestep[i,0],trans_timestep[i,1]]]), axis=0)
		new_trans_angle = np.append(new_trans_angle, np.array([[trans_angle[i,0],trans_angle[i,1]]]), axis=0)

new_cis_angle = np.delete(new_cis_angle,0,0)
new_trans_angle = np.delete(new_trans_angle,0,0)
new_cis_timestep = np.delete(new_cis_timestep,0,0)
new_trans_timestep = np.delete(new_trans_timestep,0,0)
ntotal = float(len(np.append(cis_timestep, trans_timestep, axis=0)))

def info_table(cis,trans,ntotal,type):
	total = np.append( cis, trans,axis = 0 )
	avg_cis = "%.2f" % np.average(cis[:,1])
	std_cis = "%.2f" % np.std(cis[:,1])
	avg_trans = "%.2f" % np.average(trans[:,1])
	std_trans = "%.2f" % np.std(trans[:,1])
	avg_total = "%.2f" % np.average(total[:,1])
	std_total = "%.2f" % np.std(total[:,1])
	ncis = float(len(cis))
	ntrans = float(len(trans))
	not_relaxed = "%.2f" % ((1-((ncis+ntrans)/ntotal))*100)
	info=np.array([['Average '+type+' cis',avg_cis], ['Standard deviation '+type+' cis',std_cis],['Average '+type+' trans',avg_trans], ['Standard deviation '+type+' trans',std_trans],['Average '+type+' total',avg_total], ['Standard deviation '+type+' total',std_total] ,['Not relaxed',not_relaxed]])
	np.savetxt('info_table_'+type,info,delimiter = ',' , fmt='%s')
	

load_and_plot(new_cis_angle,new_trans_angle,ntotal,'angle_hist','Angle')
load_and_plot(new_cis_timestep,new_trans_timestep,ntotal,'timestep_hist','Time')
info_table(new_cis_angle,new_trans_angle,ntotal,'angle')
info_table(new_cis_timestep,new_trans_timestep,ntotal,'time')

#for i in cis[:,1]:
#	if i==0 :
#		np.delet

#cp=(ncis/ntotal)*100
#cp="%.2f" % cp
#cp='$cis$'+' ('+str(cp)+'%)'
#tp=(((ntrans[0])/(ntotal[0]) )*100)
#tp="%.2f" % tp
#tp='$trans$'+' ('+str(tp)+'%)'
#im = Image.open("image.png"),altenative command for image reading


