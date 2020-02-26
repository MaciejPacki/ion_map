"""
Moduł testowy dcb_reader
"""
# Importy zewnętrzne
import sys
import unittest
import datetime

# Importy wewnętrzne
sys.path.append(r"..\ion_map")
import readers.dcb_reader as dcb_reader
from constants import c


class Test_dcb_reader(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        file1 = r"test_files\P1P21503.DCB"
        file2 = r"test_files\P1C11503.DCB"
        self.dcb = dcb_reader.read(file1, file2)

    def test_P1P2(self):
        self.assertEqual(self.dcb["P1P2"]["G01"], -8.003 * 10e-9 * c)
        self.assertEqual(self.dcb["P1P2"]["G27"], -5.649 * 10e-9 * c)
        self.assertEqual(self.dcb["P1P2"]["G07"], 2.793 * 10e-9 * c)

    def test_P1C1(self):
        self.assertEqual(self.dcb["P1C1"]["G01"], 1.469 * 10e-9 * c)
        self.assertEqual(self.dcb["P1C1"]["G27"], 0.062 * 10e-9 * c)
        self.assertEqual(self.dcb["P1C1"]["G07"], 1.049 * 10e-9 * c)


if __name__ == "__main__":
    unittest.main()
