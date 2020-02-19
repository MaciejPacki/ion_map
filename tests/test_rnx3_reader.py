"""
Moduł testowy rnx_reader
"""
# Importy zewnętrzne
import sys
import unittest
import datetime
from textwrap import wrap 
# Importy wewnętrzne
sys.path.append(r"..\ion_map")
import readers.rnx_reader as rnx_reader

class Test_rnx_reader(unittest.TestCase):
    
    @classmethod
    def setUpClass(self):
        obs_file = r"test_files\WROC00POL_R_20193200000_01D_30S_MO.rnx"
        nav_file = r"test_files\brdm0760.15p"
        self.site = rnx_reader.read(obs_file, nav_file)
        
    @classmethod
    def tearDownClass(self):
        self.site = None
        
    def test_site_name(self):
        name = self.site.name
        self.assertEqual(name, "WROC")
        
    def test_site_xyz(self):
        xyz = self.site.xyz
        self.assertEqual(xyz, (3835751.6257, 1177249.7445, 4941605.0540))
        
    def test_raw_obs(self):

        epoch = datetime.datetime(2019, 11, 16, 6, 23, 30)
        obs = self.site.satellites['G01'].obs[epoch]
        for k, v in obs.items():
            print(k, v)
        # self.assertEqual(obs['C1C'], 22037613.687)
        # self.assertEqual(obs['L1C'], 115808467.712)
    
    
        
        
        
if __name__ == "__main__":
    unittest.main()
    