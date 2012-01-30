import glob
import unittest
from abitbx.crystal import Crystal
import abitbx.converters as converters

class TestConverters(unittest.TestCase):
    def setUp(self):
        self.crystals = []
        for file_name in glob.glob('data/cifs/*.cif'):
            #file_name = 'test_cifs/icsd-12301.cif'
            c = Crystal.from_cif(file_name)
            c.print_summary
            self.crystals.append(c)

    def test_crystal_to_doc(self):
        crystal = self.crystals[0]
        doc = converters.crystal_to_doc(crystal)
        print doc
        self.assertTrue('nelements' in doc)
        
    def test_mp_dict_to_crystal(self):
        mp_dict = {'lattice': {'a': 3.8401979336999998, 'volume': 40.044794644251596, 'c': 3.8401979337177736, 'b': 3.8401989943442438, 'matrix': [[3.8401979337, 0.0, 0.0], [1.9200989668, 3.3257101909, 0.0], [0.0, -2.2171384943, 3.1355090603]], 'alpha': 119.99999086398419, 'beta': 90.0, 'gamma': 60.000009137322195}, 'sites': [{'occu': 0.5, 'abc': [0, 0, 0], 'xyz': [0.0, 0.0, 0.0], 'species': [{'occu': 0.5, 'element': 'Mn'}, {'occu': 0.5, 'oxidation_state': 4, 'element': 'Si'}], 'label': 'Mn: 0.5000, Si4+: 0.5000'}, {'occu': 0.5, 'abc': [0.75, 0.5, 0.75], 'xyz': [3.8401979336749994, 1.2247250003039056e-06, 2.3516317952249999], 'species': [{'occu': 0.5, 'oxidation_state': 4, 'element': 'Ge'}], 'label': 'Ge4+: 0.5000'}]}
        #crystal = converters.


if __name__ == '__main__':
    unittest.main()
