import numpy as np
import matplotlib.pyplot as plt
import os
import os.path
import sqlite3
import shutil 
from flask import Flask, request, session, g, redirect, url_for, abort, render_template, flash

# configuration
DATABASE = '/tmp/flaskr.db'
DEBUG = True
SECRET_KEY = 'development key'
USERNAME = 'admin'
PASSWORD = 'default'
			


def Content():
	TOPIC_DICT = {"Results":[["histogram","link to histogram"],["angle","link to angle"]],"PLOTs":[["enegy","link to energy"]]}
	return TOPIC_DICT
def connect_db():
    return sqlite3.connect(app.config['DATABASE'])
TOPIC_DICT = Content()
 
def FUNCTIONAL_GROUP():
    FUNCTIONAL_GROUP = []
    ls = os.listdir('..'+os.sep+'flask_new'+os.sep+'results'+os.sep)
    for ilist in range(len(ls)):
            temp = ls[ilist].split('_')[0]
            seen = 0
            for j in range(len(FUNCTIONAL_GROUP)):
                if FUNCTIONAL_GROUP[j] == temp : 
                    seen = 1
                if seen == 0 :
                    FUNCTIONAL_GROUP.append(temp)
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


@app.route('/slashboard/')
@app.route('/intro/')
def intro():
	return render_template("intro.html", FUNCTIONAL_GROUP = FUNCTIONAL_GROUP)
	
@app.route('/cmp_method/')
def comp_method():
	return render_template("cmp_method.html", FUNCTIONAL_GROUP = FUNCTIONAL_GROUP)
	
	
@app.route('/Tables/')
def Tables():
	return render_template("Tables.html", FUNCTIONAL_GROUP = FUNCTIONAL_GROUP)


	
@app.errorhandler(404)
def page_not_found(e):
	return render_template("404.html")


#@app.route('/login/', methods=['GET','POST'])
#def login_page():
#	return render_template("login.html")

#@app.route('/OH/')
#def login_page():
#	return render_template("OH.html")
#  


@app.route('/OH1/')
def login_page():
	return render_template("OH1.html")
def analyze():
        
        FUNCTIONAL_GROUP = []
        ls = os.listdir('..'+os.sep+'flask_new'+os.sep+'results'+os.sep+'')
        for ilist in range(len(ls)):
                temp = ls[ilist].split('_')[0]
                seen = 0
                for j in range(len(FUNCTIONAL_GROUP)):
                        if FUNCTIONAL_GROUP[j] == temp : 
                               seen = 1
                if seen == 0 :
                        FUNCTIONAL_GROUP.append(temp)
        script_src = '..'+os.sep+'flask_new'+os.sep+'python_scripts'+os.sep+'hist.py'
        for fg in FUNCTIONAL_GROUP :
                directory = '..'+os.sep+'flask_new'+os.sep+'static'+os.sep+'data'+os.sep+''+fg
                if not os.path.exists(directory):
                        os.makedirs(directory)
                cis_dir = directory+''+os.sep+'cis'
                trans_dir = directory+''+os.sep+'trans'
                cis_src = '..'+os.sep+'flask_new'+os.sep+'results'+os.sep+''+fg+'_cis_angle_analysis.csv'
                trans_src = '..'+os.sep+'flask_new'+os.sep+'results'+os.sep+''+fg+'_trans_angle_analysis.csv'
                if not os.path.exists(cis_dir):
                        os.makedirs(cis_dir)
                if not os.path.exists(trans_dir):
                        os.makedirs(trans_dir)
                shutil.copy(cis_src,cis_dir+''+os.sep+'time.csv')
                shutil.copy(trans_src,trans_dir+''+os.sep+'time.csv')
                shutil.copy(script_src,cis_dir+'hist.py')
                shutil.copy(script_src,trans_dir+'hist.py')
        return FUNCTIONAL_GROUP



@app.route('/results/<fn_group>/')
def dynam(fn_group):
	group = 'mytest'
	pos_group = 'mytest'
	POS_LIST = 'mytest'
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
	
        
	return render_template("dynamic.html", FUNCTIONAL_GROUP = FUNCTIONAL_GROUP , POS_LIST = POS_LIST , group = group , pos_group = pos_group, angle_info_cis = angle_info_cis , angle_info_trans = angle_info_trans , timestep_info_cis = timestep_info_cis , timestep_info_trans = timestep_info_trans)			


if __name__ == "__main__":
	app.run()
