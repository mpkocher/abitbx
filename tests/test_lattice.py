from abitbx.lattice import Lattice
import unittest

class TestLattice(unittest.TestCase):
    def setUp(self):
        a,b,c = 4,5,6
        alpha,beta,gamma = 90., 90.0, 90.0
        self.lattice =  Lattice(a,b,c,alpha,beta,gamma)
        
    def test_volume(self):
        """docstring for test_volume"""
        self.assertEqual(self.lattice.volume, 4*5*6.0)

    def test_distance(self):
        """docstring for test_volume"""
        abc1 = [0.2, 0.35, 0.45]
        abc2 = [0.1, 0.15, 0.15]
        d = self.lattice.distance(abc1,abc2)
        print d

    def test_convert_to_xyz(self):
        """docstring for test_volume"""
        abc = [0.2, 0.35, 0.45]
        xyz = self.lattice.fractionalize(abc)
        print xyz

    def test_convert_to_abc(self):
        """docstring for test_volume"""
        xyz = [1.2, 1.35, 2.45]
        abc = self.lattice.orthogonalize(xyz)
        print abc

if __name__ == '__main__':
    unittest.main()
