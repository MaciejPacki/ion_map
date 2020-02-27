import sys
import unittest
import datetime
import math
import numpy as np

# Importy wewnętrzne
sys.path.append(r"..\ion_map")
import plotters.plots
from readers import rnx_obs, rnx_nav, dcb


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
        ionosphere_h = 450
        elev_mask = 30

        site.process_data(nav, sat_dcb, ionosphere_h, elev_mask)

        self.site = site

    # def test_plot_vtec(self):
    #     plotters.plots.vtec(self.site)

    def test_plot_l4(self):
        sat = self.site.satellites["G24"]
        plotters.plots.L4(sat)


if __name__ == "__main__":
    unittest.main()
