#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Dec 19 13:29:46 2018

@author: Pedram Tavadze
"""

import pymongo
import pymatgen
from multiprocessing import Pool
from mpinterfaces.calibrate import CalibrateSlab
from mpinterfaces.interface import Interface
from mpinterfaces import transformations
from mpinterfaces import utils
import json
import os
import numpy as np



def get_entry(args):
    # return -1 ran with an error
    # return 0 ran with no error
    # return 1 match was not found
    # return 2 skiped because radioactive
    # return 3 skipped because noble gas
    # return 4 skipped because atomic number greater than 83 
    _id = args[0]
    counter = args[1]
    mat2d_slab = args[2]
    if counter % 1000 ==0 :
        print("Reached entry number {}".format(counter))
    radioactive_elemets = ["U","Ra","Th","Rn","Po","Pu","Tc","Np","Fr","Cm","Pm","Hs","Re"]
    noble_gases = ["He","Ne","Ar","Kr","Xe","Rn"]
    client = pymongo.MongoClient()
    entries = client.PyChemiaDB_OQMD12.pychemia_entries
    entry = entries.find_one({'_id':_id})
    if len(entry['init_structure']) != 0 :
        st_dict = entry['init_structure']
    elif len(entry['structure']) !=0 : 
        st_dict = entry['structure']
    else :
        print("Structure {} was not found".format(_id))
        return -1
    substrate_bulk = pymatgen.core.Structure(lattice=st_dict["cell"],
                                             species=st_dict['symbols'],coords=st_dict['positions'],coords_are_cartesian=True)
    for element in substrate_bulk.symbol_set : 
        if element in radioactive_elemets : 
            
            return 2
        elif element in noble_gases : 
            return  3
        elif pymatgen.core.Element(element).number > 83 :
            return 4
    sa_sub = pymatgen.symmetry.analyzer.SpacegroupAnalyzer(substrate_bulk)
    try :
        substrate_bulk = sa_sub.get_conventional_standard_structure()
    except :
        return -1
    spg = sa_sub.get_space_group_number()
                
    directions = [ [1,0,0],[0,1,0],[0,0,1],
                  [1,1,0],[0,1,1],[1,0,1],
                  [1,1,1]]
    formula = substrate_bulk.composition.hill_formula

    data = {}
    data[formula] = {}
    data[formula]["space_group_pymatgen"] = spg
    data[formula]["space_group_oqmd"] = entry['properties']['oqmd']['spacegroup_number']
    data[formula]["_id"] = _id

                
    found_one = False
    for direction in directions : 
        data[formula][str(direction)] = {}
        substrate_slab = Interface(substrate_bulk,
                                   hkl=direction,
                                   min_thick=10,
                                   min_vac=15,
                                   primitive=False, from_ase=True)

        try :
            substrate_slab_aligned, mat2d_slab_aligned,mismatch = transformations.get_aligned_lattices(substrate_slab,
                                                                                  mat2d_slab           ,
                                                                                  max_area       = 40 ,
                                                                                  max_mismatch   = 0.05,
                                                                                  max_angle_diff = 1,
                                                                                  r1r2_tol       = 0.01)
        except :    
            print("Except error Matching {} ,id : {}".format(formula,_id))
            continue
            
        if substrate_slab_aligned == None or mat2d_slab_aligned == None :
            continue            
        else :
            data[formula][str(direction)]["mismatch"] = mismatch
          
            if any(mismatch) : 
                found_one = True
    if found_one :
        wf = open("results"+os.sep+str(spg)+'-'+_id+".json",'w')
        json.dump(data,wf,sort_keys=True,indent=4,separators=(',',': '))
        wf.close()
        return 0
    else :
        return 1

db = pymongo.MongoClient()
args = []
mat2d_slab = utils.slab_from_file([0, 0, 1], 'Bi-POSCAR-pcell')
if not os.path.exists("results"):
    os.mkdir("results")
counter = 1
for entry in db['PyChemiaDB_OQMD12']['pychemia_entries'].find(no_cursor_timeout=True):
    args.append((entry['_id'],counter,mat2d_slab))
    counter += 1

p = Pool(8)
rets = p.map(get_entry,args)
p.close()
    # return -1 ran with an error
    # return 0 ran with no error
    # return 1 match was not found
    # return 2 skiped because radioactive
    # return 3 skipped because noble gas
    # return 4 skipped because atomic number greater than 83 
nTotal = len(rets)
nNot_found = np.sum(np.array(rets)==1)
nFound = np.sum(np.array(rets)==0)
nError = np.sum(np.array(rets)==-1)
nRaAc = np.sum(np.array(rets)==2)
nNoble = np.sum(np.array(rets)==3)
nLargeAtom = np.sum(np.array(rets)==4)

print("Total search          : {}".format(nTotal))
print("Matches not found     : {}".format(nNot_found))
print("Matches found         : {}".format(nFound))
print("Error                 : {}".format(nError))
print("Skipped Radio Activce : {}".format(nRaAc))
print("Skipped Noble Gas     : {}".format(nNoble))
print("Skipped Atomic # > 83 : {}".format(nLargeAtom))
      
search_result = {}
for i in range(len(rets)):
    search_result[args[i][0]] = rets[i]
wf = open("search_result.json",'w')
json.dump(search_result,wf,sort_keys=True,indent=4,separators=(',',': '))
wf.close()

