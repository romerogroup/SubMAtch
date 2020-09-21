#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Nov 27 15:14:58 2018

@author: Pedram Tavadze
@email : petavazohi@mix.wvu.edu
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


#setup database connection
dbsettings={'host'  : 'mongo01.systems.wvu.edu', 
            'name'  : 'PyChemiaMasterDB', 
            'user'  : 'guest', 
            'passwd': 'aldo', 
            'ssl'   : True}
pcdb=pychemia.db.get_database(dbsettings)
    

mat2d_slab = utils.slab_from_file([0, 0, 1], 'POSCAR.mp-20311_FeSe')

ls = os.listdir("results")
counter = 0
for item in ls :
#    if counter > 10 :
#        continue
    if ".json" in item : 
        rf = open("results"+os.sep+item)
        data = json.load(rf)
        rf.close()
        key = [x for x in data][0]
        _id = data[key]["_id"]
        _id = '2_O2Ti_000000000000000002575'
        st = pcdb.get_structure(_id)
        entry = pcdb.get_entry(_id)
        substrate_bulk = pymatgen.core.structure.Structure(lattice=st.lattice.cell,species=st.symbols,coords=st.positions)
    
        sa_sub = pymatgen.symmetry.analyzer.SpacegroupAnalyzer(substrate_bulk)
        substrate_bulk = sa_sub.get_conventional_standard_structure()
        spg = sa_sub.get_space_group_number()
        directions = []
        for direction in data[key]:
            if ('_' not in direction) and (len(data[key][direction]) != 0) :
                directions.append(json.loads(direction))
        dir_name = "matched_poscars"+os.sep+_id
        if not os.path.exists(dir_name):
            os.mkdir(dir_name)
        for direction in directions : 
            address = dir_name+os.sep+str(direction)
            if not os.path.exists(address):
                os.mkdir(address)
            substrate_slab = Interface(substrate_bulk,
                                           hkl=direction,
                                           min_thick=10,
                                           min_vac=15,
                                           primitive=False, from_ase=True)
            sd_flags = CalibrateSlab.set_sd_flags(interface=substrate_slab,
                                                              n_layers=nlayers_substrate,
                                                              top=True, bottom=False)
            
            substrate_slab_aligned, mat2d_slab_aligned,mismatch = transformations.get_aligned_lattices(substrate_slab,
                                                                                      mat2d_slab           ,
                                                                                      max_area       = 20 ,
                                                                                      max_mismatch   = 0.05,
                                                                                      max_angle_diff = 1,
                                                                                      r1r2_tol       = 0.01)
            substrate_slab_aligned.to(fmt='poscar',filename=address+os.sep+'POSCAR_substrate_aligned.vasp')
            mat2d_slab_aligned.to    (fmt='poscar',filename=address+os.sep+'POSCAR_mat2d_aligned.vasp')
            substrate_bulk.to(fmt='poscar',filename=address+os.sep+'POSCAR_substrate_bulk.vasp')
            hetero_interfaces = transformations.generate_all_configs(mat2d_slab_aligned,
                                                                             substrate_slab_aligned,
                                                                             nlayers_2d, nlayers_substrate,
                                                                             separation)

            for i, iface in enumerate(hetero_interfaces):
                sd_flags = CalibrateSlab.set_sd_flags(interface=iface,n_layers=nlayers_2d + nlayers_substrate, top=True, bottom=False)
                poscar = pymatgen.io.vasp.inputs.Poscar(iface, selective_dynamics=sd_flags)
                poscar.write_file(filename=address+os.sep+'POSCAR_final_{}.vasp'.format(i))
        counter += 1
                
                    
