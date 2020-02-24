import sys
import unittest
import math
import numpy as np
# Importy wewnętrzne
sys.path.append(r"..\ion_map")
import calculations.arc_detection_new
import calculations.arc_detection
import calculations.common
from readers import rnx_reader, dcb_reader


class Test_plots(unittest.TestCase):
    
    @classmethod
    def setUpClass(self):
        o_file = r"C:\users\macie\desktop\ion_map\tests\test_files\bogi0760.15o"
        n_file = r"C:\users\macie\desktop\ion_map\tests\test_files\brdm0760.15p"
        dcb_P1P2_file = r"C:\users\macie\desktop\ion_map\tests\test_files\P1P21503.DCB"
        dcb_P1C1_file = r"C:\users\macie\desktop\ion_map\tests\test_files\P1C11503.DCB"
                
        site = rnx_reader.read(o_file, n_file)
        sat_dcb = dcb_reader.read(dcb_P1P2_file, dcb_P1C1_file)
        
        site.calculate_satellites_xyz()
        site.calculate_satellites_azimuths_and_elevations()
        site.calculate_satellites_ipp(ionosphere_h=350)
        site.calculate_satellites_P4_L4_MWWL(sat_dcb)
        

        self.sat = site.satellites['G24']
        self.sat.calculate_arcs()
        
    def test_arc_detector(self):
        new_arcs = calculations.arc_detection_new.arc_detector(self.sat.L4, self.sat.MWWL)
        old_arcs = self.sat.arcs
        
        
        print('-> LEAST FIT ARCS')
        for i in old_arcs:
            print(i[0], i[1])
            
        print('\n-> MWWL_TECR CS')
        for i in new_arcs:
            print(i)

    
if __name__ == "__main__":
    unittest.main()        