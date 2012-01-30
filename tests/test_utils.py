import os
import glob
import unittest
import json
from cctbx import xray
import abitbx.utils as utils

TEST_FILES = 'data'

class TestUtils(unittest.TestCase):
    """
    docstring for Utils
    """
    def setUp(self):
        self.mp_dicts = {}
        for file_name in glob.glob(os.path.join(TEST_FILES, '*.json')):
            with open(os.path.abspath(file_name),'r') as f:
                d = json.loads(f.read())
                d['file_name'] = file_name
                self.mp_dicts[file_name] = d
        self.cif_file_names = [os.path.abspath(file_name) for file_name in glob.glob(os.path.join(TEST_FILES, 'cifs/*.cif'))]

    def test_mg_structure_dict_cctbx_crystal(self):
        """
        This isn't really a test
        """
        for file_name, d in self.mp_dicts.items():
            c = utils.mg_structure_dict_to_cctbx_crystal_structure(d)
            #c.show_summary()
            #c.show_scatterers()
            sg, s = utils.find_symmetry(c)
            #print (sg, s)
            
    def test_mg_structure_from_cif(self):
        """
        Functional test to see if the parsing from a cif works
        """
        crystals = []
        for file_name in self.cif_file_names:
            crystal = utils.cctbx_crystal_structure_from_cif(file_name)
            #crystal.show_summary()
            #crystal.show_scatterers()
    
    def find_symmetry_of_LiFePO4(self):
        file_name = 'task-11614-LiFePO4.json'
        correct_sg = {'cctbx_name': 'C m c m ', 'hermann_mauguin': 'C m c m ', 'crystal_system': 'Orthorhombic', 'number': 63, 'hall': '-C 2c 2 '}
        d = self.mp_dict[file_name]
        c = utils.mg_structure_dict_to_cctbx_crystal_structure(d)
        sg, s = utils.find_symmetry(c)
        self.assertEqual(correct_sg, sg)

    def find_symmetry_of_MgO(self):
        file_name = 'task-1265-MgO.json'
        # This is wrong! THe correct space group is F m -3 m
        correct_sg = {'cctbx_name': 'P m -3 m', 'hermann_mauguin': 'P m -3 m', 'crystal_system': 'Cubic', 'number': 221, 'hall': '-P 4 2 3'}
        d = self.mp_dict[file_name]
        c = utils.mg_structure_dict_to_cctbx_crystal_structure(d)
        sg, s = utils.find_symmetry(c)
        self.assertEqual(correct_sg, sg)

if __name__ == '__main__':
    unittest.main()
