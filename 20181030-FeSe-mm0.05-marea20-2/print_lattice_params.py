#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Nov 27 16:11:37 2018

@author: petavazohi
"""

import json
import pychemia
import pymatgen
import os

dbsettings={'host'  : 'mongo01.systems.wvu.edu', 
            'name'  : 'PyChemiaMasterDB', 
            'user'  : 'guest', 
            'passwd': 'aldo', 
            'ssl'   : True}
pcdb=pychemia.db.get_database(dbsettings)
    


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
        st = pcdb.get_structure(_id)
        substrate_bulk = pymatgen.core.structure.Structure(lattice=st.lattice.cell,species=st.symbols,coords=st.reduced)
        sa_sub = pymatgen.symmetry.analyzer.SpacegroupAnalyzer(substrate_bulk)
        substrate_bulk = sa_sub.get_conventional_standard_structure()
        a = substrate_bulk.lattice.a.round(decimals=3)
        b = substrate_bulk.lattice.a.round(decimals=3)
        c = substrate_bulk.lattice.a.round(decimals=3)
        formula = substrate_bulk.composition.formula
        print("{:>15}    {:>15}    {:>15}    {:>15}    {:>15}".format(a,b,c,formula,_id))
