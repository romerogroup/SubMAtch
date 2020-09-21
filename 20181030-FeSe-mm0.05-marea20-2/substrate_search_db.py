# -*- coding: utf-8 -*-
from __future__ import division, print_function, unicode_literals, \
    absolute_import
    
"""
This script is meant to search in the database 
for different substrates for FeS
Author : Pedram Tavadze
Email  : petavazohi@mix.wvu.edu
"""

import os
import pychemia
import pymatgen
from mpinterfaces.calibrate import CalibrateSlab
from mpinterfaces.interface import Interface
from mpinterfaces import transformations
from mpinterfaces import utils

import json


separation = 3  # in angstroms
nlayers_2d = 1
nlayers_substrate = 2

#if os.path.isfile("matches_FeSe.json") :
#    rf = open("matches_FeSe.json")
#    data = json.load(rf)
#    rf.close()
#else : 
#    data = {}

faulty_data = []
#setup database connection
dbsettings={'host'  : 'mongo01.systems.wvu.edu', 
            'name'  : 'PyChemiaMasterDB', 
            'user'  : 'guest', 
            'passwd': 'aldo', 
            'ssl'   : True}
pcdb=pychemia.db.get_database(dbsettings)
counter = 0
if not os.path.exists("results"):
    os.mkdir("results")
    
if not os.path.exists("checked"):
    os.mkdir("checked")

radioactive_elemets = ["U","Ra","Th","Rn","Po","Pu","Bi","Tc","Np","Fr","Cm","Pm","Hs","Re"]
noble_gases = ["He","Ne","Ar","Kr","Xe","Rn"]
bad_ids= ["2_BeZn_000000000000000758706"] 

mat2d_slab = utils.slab_from_file([0, 0, 1], 'POSCAR.mp-20311_FeSe')

for i in pcdb.entries.find(no_cursor_timeout=True):
            #try :
                data = {}

                _id = i['_id']
                if _id in bad_ids : 
                    continue
                try :
                    st = pcdb.get_structure(_id)
                    entry = pcdb.get_entry(_id)
                except :
                    faulty_data.append(_id)
                    continue
                skip_this = False
                for element in st.composition : 
                    if element in radioactive_elemets : 
                        skip_this = True
                        continue 
                    if element in noble_gases : 
                        skip_this = True
                        continue
                    if pychemia.core.Element(element).atomic_number > 83 :
                        skip_this = True
                        continue
                if skip_this : 
                    continue
                if st.natom > 20 :
                    continue
                
                # Loading random structure from mongodb and preparing
                counter += 1
                
                print("matrial number {}  {}".format(counter,st.formula))
                
                
                

                
#                if not(os.path.exists(dir_name)):
#                    os.mkdir(dir_name)
#                else :
#                    continue


#                lattice = pymatgen.Lattice.from_parameters(a=st.lattice.a,
#                                                           b=st.lattice.b,
#                                                           c=st.lattice.c,
#                                                           alpha=st.lattice.alpha,
#                                                           beta=st.lattice.beta,
#                                                           gamma=st.lattice.gamma)
                
                substrate_bulk = pymatgen.core.structure.Structure(lattice=st.lattice.cell,species=st.symbols,coords=st.reduced)

                sa_sub = pymatgen.symmetry.analyzer.SpacegroupAnalyzer(substrate_bulk)
                substrate_bulk = sa_sub.get_conventional_standard_structure()
                spg = sa_sub.get_space_group_number()
                
                directions = [ [1,0,0],[0,1,0],[0,0,1],
                               [1,1,0],[0,1,1],[1,0,1],
                               [1,1,1]]

                
                data[st.formula] = {}
                data[st.formula]["space_group_pymatgen"] = spg
                data[st.formula]["space_group_oqmd"] = entry['properties']['oqmd']['spacegroup_number']
                data[st.formula]["_id"] = _id
                dir_name = str(spg)+'-'+_id
                
                found_one = False
                for direction in directions : 
                    data[st.formula][str(direction)] = {}
                    address = dir_name+os.sep+str(direction)
#                    if not(os.path.exists(address)):
#                        os.mkdir(address)
                    # min_think = 10 , min_vac = 10?
                    substrate_slab = Interface(substrate_bulk,
                                           hkl=direction,
                                           min_thick=10,
                                           min_vac=15,
                                           primitive=False, from_ase=True)
#                    mat2d_slab.to(fmt='poscar', filename=address+os.sep+'POSCAR_mat2d_slab.vasp')
                    try :
                        sd_flags = CalibrateSlab.set_sd_flags(interface=substrate_slab,
                                                              n_layers=nlayers_substrate,
                                                              top=True, bottom=False)
                    except :    
                        faulty_data.append(_id)
                        continue
#                    poscar = pymatgen.io.vasp.inputs.Poscar(substrate_slab, selective_dynamics=sd_flags)
#                    poscar.write_file(filename=address+os.sep+'POSCAR_substrate_slab.vasp')
                    try :
                        substrate_slab_aligned, mat2d_slab_aligned,mismatch = transformations.get_aligned_lattices(substrate_slab,
                                                                                      mat2d_slab           ,
                                                                                      max_area       = 20 ,
                                                                                      max_mismatch   = 0.05,
                                                                                      max_angle_diff = 1,
                                                                                      r1r2_tol       = 0.01)
#                    except : 
#                        for i in os.listdir(address):
#    
#                            os.remove(address+os.sep+i)
#                        try : 
#                            os.rmdir(address)
#                        except : 
#                            print("Directory {} not empty ".format(address))
#                        continue
                    except :    
                        print("Except error")
                    #time.sleep(10)
                    

#                   
                    if substrate_slab_aligned == None or mat2d_slab_aligned == None :
                        continue
#                        for i in os.listdir(address):
#    
#                            os.remove(address+os.sep+i)
#                        try : 
#                            os.rmdir(address)
#                        except : 
#                            print("Directory {} not empty ".format(address))
#                        continue
                    #  mismatch array [u , v , angle]
                    
                    data[st.formula][str(direction)]["mismatch"] = mismatch
                
                    if any(mismatch) : 
                        found_one = True
#                    substrate_slab_aligned.to(fmt='poscar',filename=address+os.sep+'POSCAR_substrate_aligned.vasp')
#                    mat2d_slab_aligned.to    (fmt='poscar',filename=address+os.sep+'POSCAR_mat2d_aligned.vasp')
#                    hetero_interfaces = transformations.generate_all_configs(mat2d_slab_aligned,
#                                                                             substrate_slab_aligned,
#                                                                             nlayers_2d, nlayers_substrate,
#                                                                             separation)

#                    for i, iface in enumerate(hetero_interfaces):
#                        sd_flags = CalibrateSlab.set_sd_flags(interface=iface,n_layers=nlayers_2d + nlayers_substrate, top=True, bottom=False)
#                        poscar = pymatgen.io.vasp.inputs.Poscar(iface, selective_dynamics=sd_flags)
                        #if iface.num_sites > 30 : 
                        #    continue
#                        poscar.write_file(filename=address+os.sep+'POSCAR_final_{}.vasp'.format(i))
                    
                
                    
#                    if not(any(["final" in x for x in os.listdir(address)])) :
#                        for i in os.listdir(address) : 
#                            os.remove(address+os.sep+i)
#                        try :
#                            os.rmdir(address)
#                        except : 
#                            print("Directory {} not empty ".format(address))
#                
#                os.remove(dir_name+os.sep+"POSCAR_substrate")
#                
#                if len(os.listdir(dir_name+os.sep)) == 0 :
#                    try :
#                        os.rmdir(dir_name+os.sep)
#                    except :
#                        print("Directory {} not empty".format(dir_name+os.sep))
#                else : 
#                    wf = open("results"+os.sep+dir_name+".json",'w')
#                    json.dump(data,wf,sort_keys=True,indent=4,separators=(',',': '))
#                    wf.close()
                if found_one :
                    wf = open("results"+os.sep+str(spg)+'-'+_id+".json",'w')
                    json.dump(data,wf,sort_keys=True,indent=4,separators=(',',': '))
                    wf.close()
                else : 
                    continue
#                wf = open("checked"+os.sep+dir_name+".json",'w')
#                json.dump(checked,wf,sort_keys=True,indent=4,separators=(',',': '))
#                wf.close()
                
                

                
            
wf = open("faulty_ids",'w')
for i in faulty_data :
    wf.write(str(i)+"\n")
wf.close()