import numpy as np
import matplotlib.pyplot as plt
import os
import os.path
import sqlite3
from flask import Flask, request, session, g, redirect, url_for, abort, render_template, flash

# configuration
DATABASE = '/tmp/flaskr.db'
DEBUG = True
SECRET_KEY = 'development key'
USERNAME = 'admin'
PASSWORD = 'default'

# def CHANGE(group,pos_group) :
	# CHANGE1 = '../static/data/'+group+'/'+pos_group+'/cis/'+group+pos_group+'_cis.mol'
	# CHANGE2 = '../static/data/'+group+'/'+pos_group+'/trans/image.png'
	# CHANGE3 = ,'../static/data/OH1'
	# CHANGE4 = '../../static/data/'+group+'/'+pos_group+'/cis/'+group+pos_group+'_cis.mol'
	# CHANGE5 = '../../static/data/'+group+'/'+pos_group+'/trans/'+group+pos_group+'_trans.mol'
	# CHANGE6 = 'data/'+group+'/'+pos_group+'/cis/'+'angle_hist.png'
	# CHANGE7 = 'data/'+group+'/'+pos_group+'/trans/'+'angle_hist.png'
	# CHANGE8 = 'data/'+group+'/'+pos_group+'/cis/'+'timestep_hist.png'
	# CHANGE9 = 'data/'+group+'/'+pos_group+'/trans/'+'timestep_hist.png'
	# CHANGE10 = 'data/'+group+'/'+pos_group+'energy_vs_angle.png'
	# return CHANGE1, CHANGE2, CHANGE3, CHANGE4, CHANGE5, CHANGE6, CHANGE7, CHANGE8, CHANGE9, CHANGE10

#	../static/data/OH/3/cis/azo_cis_oh_p3.mol          CHANGE1
#	../../static/data/OH/3/trans/image.png             CHANGE2
#	../../static/OH1.spt						       CHANGE3
#	../../static/data/OH/3/cis/azo_cis_oh_p3.mol 	   CHANGE4
#	../../static/data/OH/2/trans/azo_trans_oh_p2.mol   CHANGE5
#	data/OH/2/cis/angle_hist.png					   CHANGE6
#	data/OH/2/trans/angle_hist.png					   CHANGE7
#	data/OH/2/cis/timestep_hist.png					   CHANGE8
#	data/OH/2/trans/timestep_hist.png				   CHANGE9
#	data/OH/2/energy_vs_angle.png					   CHANGE10
	
	
#def list_groups() :
#	list = os.listdir('C:/Users/Pedram/Desktop/flaskr - Copy - Copy/static/data')
	# for group in list :
		# pos_list = os.listdir('C:/Users/Pedram/Desktop/flaskr - Copy - Copy/static/data'+'/'+group)
		# for pos_group in pos_list :
			# creat_html(group,pos_group)
				

def Content():
	TOPIC_DICT = {"Results":[["histogram","link to histogram"],["angle","link to angle"]],"PLOTs":[["enegy","link to energy"]]}
	return TOPIC_DICT
def connect_db():
    return sqlite3.connect(app.config['DATABASE'])
TOPIC_DICT = Content()
 
def FUNCTIONAL_GROUP():
	FUNCTIONAL_GROUP = os.listdir('..'+os.sep+'flaskr'+os.sep+'static'+os.sep+'data')
	return FUNCTIONAL_GROUP
FUNCTIONAL_GROUP = FUNCTIONAL_GROUP()


#def html_creat():
#	for f in FUNCTIONAL_GROUP :
#		if not os.path.exists(f):
#			os.makedirs(f)
#		for i in range(2,6):
#			if not os.path.exists(f+'/'+str(i))
#			os.makedirs(f+'/'+str(i))
			
			

app = Flask(__name__)
app.config.from_object(__name__)

@app.route('/')
def homepage():
	return render_template("main.html")

@app.route("/interface")
def interface():
    return render_template("interface_input.html")





@app.route('/slashboard/')
@app.route('/intro/')
def intro():
	return render_template("intro.html", FUNCTIONAL_GROUP = FUNCTIONAL_GROUP)
	
@app.route("/result")
def result():
    return render_template("result.html")

	
@app.errorhandler(404)
def page_not_found(e):
	return render_template("404.html")




@app.route('/OH1/')
def login_page():
	return render_template("OH1.html")

@app.route('/results/<fn_group>/')
def dynam(fn_group):
	group = fn_group.split("p")[0]
	pos_group = fn_group.split("p")[1]
	POS_LIST = os.listdir('..'+os.sep+'flaskr'+os.sep+'static'+os.sep+'data'+os.sep+''+group)
	not_valid=np.array([[0,0],[0,0],[0,0],[0,0],[0,0],[0,0],[0,0]])
	if os.path.isfile('..'+os.sep+'flaskr'+os.sep+'static'+os.sep+'data'+os.sep+''+group+''+os.sep+''+pos_group+''+os.sep+'cis'+os.sep+'info_table_angle') :
		angle_info_cis = np.loadtxt('..'+os.sep+'flaskr'+os.sep+'static'+os.sep+'data'+os.sep+''+group+''+os.sep+''+pos_group+''+os.sep+'cis'+os.sep+'info_table_angle',delimiter=',',dtype='str')
	else :
		angle_info_cis = not_valid
	if os.path.isfile('..'+os.sep+'flaskr'+os.sep+'static'+os.sep+'data'+os.sep+''+group+''+os.sep+''+pos_group+''+os.sep+'trans'+os.sep+'info_table_angle') :
		angle_info_trans = np.loadtxt('..'+os.sep+'flaskr'+os.sep+'static'+os.sep+'data'+os.sep+''+group+''+os.sep+''+pos_group+''+os.sep+'trans'+os.sep+'info_table_angle',delimiter=',',dtype='str')
	else :
		angle_info_trans = not_valid
	if os.path.isfile('..'+os.sep+'flaskr'+os.sep+'static'+os.sep+'data'+os.sep+''+group+''+os.sep+''+pos_group+''+os.sep+'cis'+os.sep+'info_table_time'):
		timestep_info_cis = np.loadtxt('..'+os.sep+'flaskr'+os.sep+'static'+os.sep+'data'+os.sep+''+group+''+os.sep+''+pos_group+''+os.sep+'cis'+os.sep+'info_table_time',delimiter=',',dtype='str')
	else :
		timestep_info_cis = not_valid
	if os.path.isfile('..'+os.sep+'flaskr'+os.sep+'static'+os.sep+'data'+os.sep+''+group+''+os.sep+''+pos_group+''+os.sep+'trans'+os.sep+'info_table_time') :
		timestep_info_trans = np.loadtxt('..'+os.sep+'flaskr'+os.sep+'static'+os.sep+'data'+os.sep+''+group+''+os.sep+''+pos_group+''+os.sep+'trans'+os.sep+'info_table_time',delimiter=',',dtype='str')
	else :
		timestep_info_trans = not_valid
	#CHANGE1 = '../static/data/'+group+'/'+pos_group+'/cis/'+group+'p'+pos_group+'_cis.mol'
	#CHANGE2 = '../static/data/'+group+'/'+pos_group+'/trans/image.png'
	#CHANGE3 = '../static/data/OH1'
	#CHANGE4 = '../../static/data/'+group+'/'+pos_group+'/cis/'+group+'p'+pos_group+'_cis.mol'
	#CHANGE5 = '../../static/data/'+group+'/'+pos_group+'/trans/'+group+'p'+pos_group+'_trans.mol'
	#CHANGE6 = 'data/'+group+'/'+pos_group+'/cis/'+'angle_hist.png'
	#CHANGE7 = 'data/'+group+'/'+pos_group+'/trans/'+'angle_hist.png'
	#CHANGE8 = 'data/'+group+'/'+pos_group+'/cis/'+'timestep_hist.png'
	#CHANGE9 = 'data/'+group+'/'+pos_group+'/trans/'+'timestep_hist.png'
	#CHANGE10 = 'data/'+group+'/'+pos_group+'energy_vs_angle.png'
	return render_template("dynamic.html", FUNCTIONAL_GROUP = FUNCTIONAL_GROUP , POS_LIST = POS_LIST , group = group , pos_group = pos_group, angle_info_cis = angle_info_cis , angle_info_trans = angle_info_trans , timestep_info_cis = timestep_info_cis , timestep_info_trans = timestep_info_trans)			


if __name__ == "__main__":
	app.run()
