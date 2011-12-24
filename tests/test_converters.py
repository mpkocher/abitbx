import glob
import unittest
from abitbx.crystal import Crystal
import abitbx.converters as converters

'''
Temporary solution to separate the conversion of db docs to objects
'''

class TestConverters(unittest.TestCase):
    '''
    docstring for Converters
    '''
    def setUp(self):
        '''
        setup doc...
        '''
        self.crystals = []
        for file_name in glob.glob('test_cifs/*.cif'):
            #file_name = 'test_cifs/icsd-12301.cif'
            c = Crystal.from_cif(file_name)
            c.print_summary
            self.crystals.append(c)

    def test_crystal_to_doc(self):
        '''
        '''
        crystal = self.crystals[0]
        doc = converters.crystal_to_doc(crystal)
        print doc
        self.assertTrue('nelements' in doc)
        

if __name__ == '__main__':
    unittest.main()
