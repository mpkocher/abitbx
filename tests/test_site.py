from abitbx.site import Site
import unittest

class TestSite(unittest.TestCase):
    def setUp(self):
        """docstring for setUp"""
        self.site = Site(name = 'Li', label='Li-1', abc=(0.25, 0.5, 0.6), occupancy=1.0)
    
    def test_site(self):
        """docstring for test_name"""
        site = Site(name = 'Li', label='Li-1', abc=(0.25, 0.5, 0.6), occupancy=1.0)
        self.assertEqual(site.label, 'Li-1')
        self.assertEqual(site.name, 'Li')
        self.assertEqual(site.abc, [0.25,0.5,0.6])
        self.assertEqual(site.occupancy, 1.0)
    
        
    def test_abc(self):
        """docstring for test_abc"""
        self.assertEqual(self.site.a, 0.25)
        self.assertEqual(self.site.b, 0.5)
        self.assertEqual(self.site.c, 0.6)
        self.assertEqual(self.site.abc, [0.25, 0.5, 0.6])


if __name__ == '__main__':
    unittest.main()
