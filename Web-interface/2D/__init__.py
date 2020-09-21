# -*- coding: utf-8 -*-
"""
Created on Mon Jul 12 11:33:47 2018

@author: Pedram
"""

from flask import Flask, render_template, request, redirect, url_for
from werkzeug import secure_filename
import os
import time

#from __future__ import division, print_function, unicode_literals, absolute_import
import pymatgen
from mpinterfaces.calibrate import CalibrateSlab
from mpinterfaces.interface import Interface
from mpinterfaces import transformations
from mpinterfaces import utils

from pymatgen.io.vasp import Poscar
from pymatgen.io.cif import CifWriter




app = Flask(__name__)

upload_dir = 'uploads'
if not os.path.exists(upload_dir):
    os.makedirs(upload_dir)

if not os.path.exists("operations"):
    os.makedirs("operations")

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = upload_dir


@app.route('/')
@app.route("/main")
def home_page():
    return render_template("main.html" ,_id='home')

@app.route("/about")
def about():
    return render_template("about.html",_id="about")

@app.route("/dashboard")
def dashboard():
    return render_template("dashboard.html",_id="dashboard")

@app.route("/substrate-search",methods=["GET","POST"])
def substrate_search():
    if request.method == "POST" : 
        return redirect(url_for("request_submited.html"))
    return render_template("substrate_search.html",_id="substrate_search")

@app.route("/result/<stamp>")
def result(stamp):
    return render_template("result.html",_id="matching",stamp=stamp)



    
@app.route("/matching", methods = ['GET', 'POST'])
def upload_file():
    stamp = ""
    if request.method == 'POST':
        #request.environ['REMOTE_ADDR']
        if request.environ.get('HTTP_X_FORWARDED_FOR') is None:
            ip = request.environ['REMOTE_ADDR']
        else:   
            ip = request.environ['HTTP_X_FORWARDED_FOR'] # if behind a proxy
        #substrate information#
        f1 = request.files['POSCAR_sub']
        stamp = time.strftime("%Y%m%d-%H%M%S")+'-'+ip
        poscar_sub = stamp+'-'+f1.filename
        f1.save(upload_dir + os.sep+ secure_filename(poscar_sub))
        h_sub             = int  (request.form["h_sub"])
        k_sub             = int  (request.form["k_sub"])
        l_sub             = int  (request.form["l_sub"])
        nlayers_substrate = int  (request.form["nlayers_substrate"])
        min_thick_sub     = float(request.form["min_thick_sub"])
        min_vac_sub       = float(request.form["min_vac_sub"])
        #is_primitive      = request.form.get["is_primitive"]
        hkl_sub = [h_sub,k_sub,l_sub]
        
        #2d information#
        f2 = request.files['POSCAR_2d']
        poscar_2d = stamp+'-'+f2.filename
        f2.save(upload_dir + os.sep+ secure_filename(poscar_2d))
        h_2d              = int(request.form["h_2d"])
        k_2d              = int(request.form["k_2d"])
        l_2d              = int(request.form["l_2d"])
        nlayers_2d        = int(request.form["nlayers_2d"])
        hkl_2d = [h_2d,k_2d,l_2d]
        
        #General information#
        separation        = float(request.form["separation"])
        max_area          = float(request.form["max_area"])
        max_mismatch      = float(request.form["max_mismatch"])
        max_angle_diff    = float(request.form["max_angle_diff"])

        #Matching#
        try : 
            substrate_bulk = pymatgen.Structure.from_file(upload_dir+os.sep+poscar_sub)        
            sa_sub = pymatgen.symmetry.analyzer.SpacegroupAnalyzer(substrate_bulk)        
            substrate_bulk = sa_sub.get_conventional_standard_structure()
            substrate_slab = Interface(substrate_bulk,
                               hkl=hkl_sub,
                               min_thick=min_thick_sub,
                               min_vac=min_vac_sub,
                               primitive=False, from_ase=True)
            
            mat2d_slab = utils.slab_from_file(hkl_2d, upload_dir+os.sep+poscar_2d)
            operation_dir = "static"+os.sep+"operations"+os.sep+stamp
            if not os.path.exists(operation_dir):
                os.makedirs(operation_dir)
            mat2d_slab.to(fmt="poscar", filename=operation_dir+"POSCAR_mat2d_slab.vasp")
            sd_flags = CalibrateSlab.set_sd_flags(interface=substrate_slab,
                                                  n_layers=nlayers_substrate,
                                                  top=True, bottom=False)
            poscar = pymatgen.io.vasp.inputs.Poscar(substrate_slab, selective_dynamics=sd_flags)        
            poscar.write_file(filename=operation_dir+os.sep+"POSCAR_substrate_slab.vasp")
            substrate_slab_aligned, mat2d_slab_aligned, mismatch = transformations.get_aligned_lattices(substrate_slab,
                                                                                                        mat2d_slab,
                                                                                                        max_area=max_area,
                                                                                                        max_mismatch=max_mismatch,
                                                                                                        max_angle_diff=max_angle_diff,
                                                                                                        r1r2_tol=0.01)
            substrate_slab_aligned.to(fmt="poscar",filename=operation_dir+os.sep+"POSCAR_substrate_aligned.vasp")   
            mat2d_slab_aligned.to    (fmt="poscar",filename=operation_dir+os.sep+"POSCAR_mat2d_aligned.vasp")        
            hetero_interfaces = transformations.generate_all_configs(mat2d_slab_aligned,
                                                     substrate_slab_aligned,    
                                                     nlayers_2d, nlayers_substrate,
                                                     separation)
            for i, iface in enumerate(hetero_interfaces):
                sd_flags = CalibrateSlab.set_sd_flags(interface=iface,
                                                      n_layers=nlayers_2d + nlayers_substrate,
                                                      top=True, bottom=False)
                poscar = pymatgen.io.vasp.inputs.Poscar(iface, selective_dynamics=sd_flags)
                poscar.write_file(filename=operation_dir+os.sep+'POSCAR_final_{}.vasp'.format(i))

                p = Poscar.from_file(operation_dir+os.sep+'POSCAR_final_{}.vasp'.format(i))
                w = CifWriter(p.structure)
                w.write_file(operation_dir+os.sep+'POSCAR_final_{}.cif'.format(i))
#                st = pychemia.code.vasp.read_poscar(operation_dir+os.sep+'POSCAR_final_{}.vasp'.format(i))
                #rf = open("testing")
                #rf.write("reading succesful")
                #rf.close()
#                pychemia.io.cif.save(structure=st,filename=operation_dir+os.sep+'POSCAR_final_{}.xyz'.format(i))
        except : 
            #redirect(url_for("error",_id="matching",stamp=stamp))
            return ("Error")

        return redirect(url_for('result',stamp=stamp))
    return  render_template("matching.html",_id="matching",test_var="test",stamp=stamp)  



if __name__ == '__main__':
   app.run(debug = True)
