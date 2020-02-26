import sys
import unittest
import datetime
import math
import numpy as np

# Importy wewnętrzne
sys.path.append(r"..\ion_map")
import plotters.plots
from readers import rnx_reader, dcb_reader


class Test_plots(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        o_file = r"C:\users\macie\desktop\ion_map\tests\test_files\bogi0760.15o"
        n_file = r"C:\users\macie\desktop\ion_map\tests\test_files\brdm0760.15p"
        o_file = r"C:\users\macie\desktop\ion_map\tests\test_files\BOR10760.15o"
        dcb_P1P2_file = r"C:\users\macie\desktop\ion_map\tests\test_files\P1P21503.DCB"
        dcb_P1C1_file = r"C:\users\macie\desktop\ion_map\tests\test_files\P1C11503.DCB"

        site = rnx_reader.read(o_file, n_file)
        sat_dcb = dcb_reader.read(dcb_P1P2_file, dcb_P1C1_file)

        site.calculate_satellites_xyz()
        site.calculate_satellites_azimuths_and_elevations()
        site.calculate_satellites_ipp(ionosphere_h=350)
        site.calculate_satellites_P4_L4_MWWL(sat_dcb)
        site.calculate_satellites_arcs()
        site.calculate_satellites_L4_shifted()
        site.calculate_satellites_STEC()
        site.calculate_satellites_VTEC(ionosphere_h=350)

        self.site = site
        self.sat1 = site.satellites["G21"]
        self.sat2 = site.satellites["G27"]

    # def test_obs_comb_2sat(self):
    #     plotters.plots.obs_comb_2sat(self.sat1, self.sat2)

    # def test_obs(self):
    #     plotters.plots.obs_comb(self.sat1)

    def test_plot_vtec(self):
        plotters.plots.vtec(self.site)


if __name__ == "__main__":
    unittest.main()
