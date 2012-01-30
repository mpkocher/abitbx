import os
import glob
import unittest
from abitbx.crystal import Crystal, SymmetryError
from abitbx.space_group import SpaceGroup
from abitbx.site import Site
from abitbx.lattice import Lattice

TEST_FILES = 'data'

class TestCrystal(unittest.TestCase):
    def setUp(self):
        self.cif_file_names = [os.path.abspath(file_name) for file_name in glob.glob(os.path.join(TEST_FILES, 'cifs/*.cif'))]
        space_group = SpaceGroup('C 1 2/m 1')
        lattice = Lattice(4.0, 5.0, 6.0, 90.0, 109.10, 90.0)
        sites = []
        sites.append(Site(label="Li", abc=(0.25, 0.0, 0.0), occupancy=0.80))
        sites.append(Site(label="Mn", abc=(0.25, 0.0, 0.0), occupancy=0.20))
        sites.append(Site(label="O", abc=(0.5, 0.5, 0.5)))
        self.crystal = Crystal(sites=sites, space_group=space_group, lattice=lattice)
    
    def test_load_cif(self):
        for file_name in self.cif_file_names:
            c = Crystal.from_cif(file_name)
            c.print_summary

    def test_crystal(self):
        for file_name in self.cif_file_names:
            c = Crystal.from_cif(file_name)
            c.print_summary()
            for site in c.sites:
                print site.to_dict()

    def test_to_niggli(self):
        for file_name in self.cif_file_names:
            c = Crystal.from_cif(file_name)
            n = c.to_niggli()
            n.print_summary()
            print n.to_dict()
    
    def test_to_standard(self):
        for file_name in self.cif_file_names:
            c = Crystal.from_cif(file_name)
            n = c.to_standard()
            n.print_summary()
            print n.to_dict()
    
    def test_multiple_transforms(self):
        """docstring for test_to_niggli"""
        for file_name in self.cif_file_names:
            c = Crystal.from_cif(file_name)
            n = c.to_standard()
            ssg = n.space_group.raw_cctbx_name
            f = n.to_niggli()
            ssf = f.space_group.raw_cctbx_name
            #self.assertEqual(ssg, ssf)
            print ssg + " *** " + ssf
            #f.print_summary()
            print f.to_dict()
            #transform_names = [t["name"] for t in f.transforms]
            #print transform_names
            #print f.transforms
            cry = c.to_standard().to_niggli()
            print c.to_standard().to_niggli().to_dict()
    
    
    def test_assign_coordination_number(self):
        
        print "Test assign coordination number."
        
        file_name = os.path.join(TEST_FILES, 'cifs', 'icsd-12301.cif')
        current_crystal = Crystal.from_cif(file_name)
        
        passed = True
        
        for sca in current_crystal.crystal_structure.scatterers():
            
            label = sca.label
            
            coord_num = current_crystal.get_coordination_number(sca)
            self.assertEqual(coord_num, 4.0)
            '''
            # make sure labels match cctbx output
            # not the most rigorous test but alright for now 
            if label == "Li-0":
                if coord_num != 6:
                    print "Coordination number test failed on label = " + label 
                    print "Number is", coord_num, "and should be 6."
                    passed = False 
            elif label == "Fe-1":
                if coord_num != 6:
                    print "Coordination number test failed on label = " + label 
                    print "Number is", coord_num, "and should be 6."
                    passed = False
            elif label == "P-2":
                if coord_num != 4:
                    print "Coordination number test failed on label = " + label
                    print "Number is", coord_num, "and should be 4." 
                    passed = False                    
            elif label == "O-3":
                if coord_num != 4:
                    print "Coordination number test failed on label = " + label
                    print "Number is", coord_num, "and should be 4." 
                    passed = False
            elif label == "O-4":
                if coord_num != 6:
                    print "Coordination number test failed on label = " + label
                    print "Number is", coord_num, "and should be 6." 
                    passed = False
            elif label == "O-5":
                if coord_num != 6:
                    print "Coordination number test failed on label = " + label 
                    print "Number is", coord_num, "and should be 6."
                    passed = False
            else:
                print "Unknown atom found for this test. Test Failed."
                passed = False 
                      
            '''
    def test_assign_wyckoff(self):
        """docstring for test_assign_wyckoff"""
        abc = [0.25, 0.25, 0.5]
        letter = self.crystal.assign_wyckoff(abc)
        self.assertEqual(letter, 'f')

    def test_symmetry_error(self):
        space_group = SpaceGroup('F d d 2')
        lattice = Lattice(4.0, 5.0, 6.0, 88.0, 91.0, 95.0)
        sites = []
        sites.append(Site(label="Li", abc=(0.25, 0.0, 0.0), occupancy=0.80))
        #crystal = Crystal(sites=sites, space_group=space_group, lattice=lattice)
        pass
                    
if __name__ == '__main__':
    unittest.main()
