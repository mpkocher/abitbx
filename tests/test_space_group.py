import unittest
from abitbx.space_group import SpaceGroup


class TestSpaceGroup(unittest.TestCase):
    def setUp(self):
        """docstring for setUp"""
        cctbx_names = ["P m m n :1", "P 1", "C 1 2/m 1"]
        self.space_groups = [SpaceGroup(name) for name in cctbx_names]

    def test_basic(self):
        """docstring for test_basic"""
        for space_group in self.space_groups:
            print ("\n").join(space_group.summary())
            print space_group.cctbx_name
            print space_group.point_group
            print space_group.laue
            print space_group.schoenflies
            print space_group.to_db()
            

if __name__ == '__main__':
    unittest.main()
