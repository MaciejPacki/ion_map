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
from readers import rnx_obs, rnx_nav


class Test_rnx_reader(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        # obs_file = r"test_files\WROC00POL_R_20193200000_01D_30S_MO.rnx"
        obs_file = r"test_files\bogi0760.15o"
        nav_file = r"test_files\brdm0760.15p"
        self.site = rnx_obs.read(obs_file)
        self.nav = rnx_nav.read(nav_file)


    def test_site_name(self):
        name = self.site.name
        self.assertEqual(name, "BOGI")

    def test_site_network(self):
        network = self.site.network
        self.assertEqual(network, "ASG-EUPOS IGiK")

    def test_site_xyz(self):
        xyz = self.site.xyz
        self.assertEqual(xyz, (3633815.6800, 1397453.9157, 5035280.8028))

    def test_satellite_in_epoch(self):
        epoch = datetime.datetime(2015, 3, 17, 14, 40, 30, 0)
        ref_sats_str = "G11G12G13G15G17G18G22G24G28G30"
        ref_sats = sorted(wrap(ref_sats_str, 3))
        test_sats = []
        for prn, sat in self.site.satellites.items():
            if epoch in sat.obs.keys():
                test_sats.append(prn)
            else:
                pass
        test_sats = sorted(test_sats)

        self.assertEqual(ref_sats, test_sats)

    def test_obs_in_epoch(self):
        epoch = datetime.datetime(2015, 3, 17, 11, 38, 00, 0)
        sat1 = self.site.satellites["G07"].obs[epoch]

        self.assertEqual(sat1["L1"], 110440932.100)
        self.assertEqual(sat1["P2"], 21016202.080)
        self.assertEqual(sat1["C2"], None)


    def test_nav_in_epoch(self):
        epoch = datetime.datetime(2015, 3, 17, 13, 59, 44)
        sat = self.nav["G24"][epoch]

        ref_raw = (
            "-4.512676969171e-05-6.821210263297e-13+0.000000000000e+00"
            + "+3.000000000000e+00+1.062500000000e+01+4.443756528868e-09+2.284627768260e-01"
            + "+4.805624485016e-07+3.169246716425e-03+1.233443617821e-05+5.153687980652e+03"
            + "+2.231840000000e+05+4.470348358154e-08+2.446837413720e+00+1.676380634308e-08"
            + "+9.541896396799e-01+1.337500000000e+02+3.210554058863e-01-8.043549331830e-09"
            + "-5.107355599004e-10+1.000000000000e+00+1.836000000000e+03+0.000000000000e+00"
            + "+2.000000000000e+00+0.000000000000e+00+2.328306436539e-09+3.000000000000e+00"
            + "+2.160000000000e+05+4.000000000000e+00"
        )
        keys = [
            "a0",
            "a1",
            "a2",
            "IODE",
            "crs",
            "delta_n",
            "M0",
            "cuc",
            "e",
            "cus",
            "sqrtA",
            "toe",
            "cic",
            "OMEGA0",
            "cis",
            "i0",
            "crc",
            "omega",
            "OMEGA_DOT",
            "IDOT",
            "L2",
            "gps_week",
            "L2_P_flag",
            "SV_acc",
            "SV_health",
            "TGD",
            "IODC",
            "transmision_time",
            "fit_interval",
        ]
        ref = wrap(ref_raw, 19)
        ref = list(map(float, ref))
        for key, ref_val in zip(keys, ref):
            self.assertEqual(sat[key], ref_val)


if __name__ == "__main__":
    unittest.main()
