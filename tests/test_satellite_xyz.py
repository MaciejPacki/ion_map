# Importy zewnętrzne
import sys
import unittest
import datetime

# Importy wewnętrzne
sys.path.append(r"..\ion_map")
import readers.rnx_reader as rnx_reader
import calculations.satellite_xyz


class Test_satellite_xyz(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        obs_file = r"test_files\bogi0760.15o"
        nav_file = r"test_files\brdm0760.15p"
        self.site = rnx_reader.read(obs_file, nav_file)
        self.site.satellites["G24"].calculate_xyz(self.site.xyz)

    @classmethod
    def tearDownClass(self):
        self.site = None

    def test_GPS(self):
        sat = self.site.satellites["G24"]

        epoch1 = datetime.datetime(2015, 3, 17, 14, 35, 30)
        epoch2 = datetime.datetime(2015, 3, 17, 16, 20, 0)

        result1 = tuple(round(p, 3) for p in sat.xyz[epoch1])
        result2 = tuple(round(p, 3) for p in sat.xyz[epoch2])

        self.assertEqual(result1, (14140733.710, -15191466.432, 16458906.828))
        self.assertEqual(result2, (15997113.069, 841757.083, 21174019.951))


if __name__ == "__main__":
    unittest.main()
