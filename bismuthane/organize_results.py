#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri May 31 20:04:33 2019

@author: petavazohi
"""

import os
import pandas as pd
import json
import re

def get_mismatch(data,direction):
    ret = ''
    if len(data[key][direction]) != 0 :
        for x in data[key][direction]['mismatch']:
            ret += str(round(x,4))+','
        return ret[:-1]
    else :
        return ',,,'
        
def get_oqmd_id(_id):
    return re.findall('[0-9]*_[A-Za-z0-9]*_0*([1-9][0-9]*)',_id)[0]

formulas = []
match_001 = []
match_010 = []
match_011 = []
match_100 = []
match_101 = []
match_110 = []
match_111 = []
oqmd_id = []
pcdb_id = []
oqmd_spg = []
calc_spg = []
oqmd_link = []
icsd = []

client = pymongo.MongoClient()
entries = client.PyChemiaDB_OQMD12.pychemia_entries
    

for imatch in os.listdir('results_Bi-POSCAR-pcell'):
    if '.json' in imatch:
        rf = open('results_Bi-POSCAR-pcell'+os.sep+imatch)
        data = json.load(rf) 
        key = [x for x in data][0]
        formula = key.replace(' ','')
        rf.close()
        nmatch = 0
        _id = data[key]['_id']
        entry = entries.find_one({'_id':_id})
        formulas.append(formula)
        match_001.append(get_mismatch(data,"[0, 0, 1]"))
        match_010.append(get_mismatch(data,"[0, 1, 0]"))
        match_011.append(get_mismatch(data,"[0, 1, 1]"))
        match_100.append(get_mismatch(data,"[1, 0, 0]"))
        match_101.append(get_mismatch(data,"[1, 0, 1]"))
        match_110.append(get_mismatch(data,"[1, 1, 0]"))
        match_111.append(get_mismatch(data,"[1, 1, 1]"))
        oqmd_id.append(get_oqmd_id)
        pcdb_id.append(_id)
        oqmd_spg.append(data[key]["space_group_oqmd"])
        calc_spg.append(data[key]['space_group_pymatgen'])
        if entry['properties']['oqmd']['path'] != None :
            if 'icsd' in entry['properties']['oqmd']['path']:
                icsd.append(True)
            else : 
                icsd.append(False)
        else : 
            icsd.append(False)
        oqmd_link.append('http://oqmd.org/materials/entry/'+get_oqmd_id(_id))

df = pd.DataFrame(data={'Formula':formulas,'ICSD':icsd,'Calculated SPG':calc_spg,'OQMD SPG':oqmd_spg,
                        'Link':oqmd_link,
                        'Mismatch 001 [a,b,angle]':match_001,
                        'Mismatch 010 [a,b,angle]':match_010,
                        'Mismatch 011 [a,b,angle]':match_011,
                        'Mismatch 100 [a,b,angle]':match_100,
                        'Mismatch 101 [a,b,angle]':match_101,
                        'Mismatch 110 [a,b,angle]':match_110,
                        'Mismatch 111 [a,b,angle]':match_111,})
df.to_excel('Bismuth.xlsx',sheet_name='Mismatch0.5_MaxArea40A')