import sys
import unittest
import math
import numpy as np

# Importy wewnętrzne
sys.path.append(r"..\ion_map")
import calculations.arc_detection_new
import calculations.arc_detection
import calculations.common as common
from readers import rnx_obs, rnx_nav, dcb
from constants import L1_lambda


class Test_plots(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        o_file = r"C:\users\macie\desktop\ion_map\tests\test_files\bogi0760.15o"
        n_file = r"C:\users\macie\desktop\ion_map\tests\test_files\brdm0760.15p"
        dcb_P1P2_file = r"C:\users\macie\desktop\ion_map\tests\test_files\P1P21503.DCB"
        dcb_P1C1_file = r"C:\users\macie\desktop\ion_map\tests\test_files\P1C11503.DCB"

        site = rnx_obs.read(o_file)
        nav = rnx_nav.read(n_file)
        sat_dcb = dcb.read(dcb_P1P2_file, dcb_P1C1_file)
        xyz = site.xyz
        blh = site.blh
        ionosphere_h = 450
        elev_mask = 30

        self.sat = site.satellites["G24"]
        self.sat.calculate_eligible_epochs()
        self.sat.calculate_xyz(xyz, nav)
        self.sat.calculate_azimuth_and_elevation(xyz)
        self.sat.calculate_ipp(blh, ionosphere_h, elev_mask)
        self.sat.calculate_P4_L4_MWWL(sat_dcb)
        self.sat.calculate_arcs()

    def test_arc_detector(self):
        new_arcs = calculations.arc_detection_new.arc_detector(
            self.sat.L4, self.sat.MWWL
        )
        old_arcs = self.sat.arcs
        print(new_arcs)
        print("-> LEAST FIT ARCS")
        for i in old_arcs:
            print(i[0], i[1])
            print(
                common.datetime_to_secs_of_day(i[0]),
                common.datetime_to_secs_of_day(i[1]),
            )
        #
        # print("\n-> MWWL_TECR CS")
        # for i in new_arcs:
        #     print(i, common.datetime_to_secs_of_day(i))


if __name__ == "__main__":
    unittest.main()
