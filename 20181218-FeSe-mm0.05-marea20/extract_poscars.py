import json
import os
import pymongo
from pymatgen.core.structure import Structure

ls = os.listdir('results')

if not os.path.exists('poscars'):
    os.mkdir('poscars')


for item in ls:
    continue
    if '.json' in item:
        rf = open("results"+os.sep+item)
        data = json.load(rf)
        rf.close()
        key = [x for x in data][0]
        _id = data[key]['_id']
        client = pymongo.MongoClient()
        entries = client.PyChemiaDB_OQMD12.pychemia_entries
        entry = entries.find_one({'_id':_id})
        if len(entry['init_structure']) != 0 :
            structure = entry['init_structure']
        elif len(entry['structure']) != 0 :
            structure = entry['structure']
        substrate = Structure(lattice=structure['cell'],species=structure['symbols'],coords=structure['reduced'])
        sa_sub = pymatgen.symmetry.analyzer.SpacegroupAnalyzer(substrate)
        substrate = sa_sub.get_conventional_standard_structure()
        substrate.to(fmt='poscar',filename='poscars'+os.sep+item.replace('json','vasp'))
        




