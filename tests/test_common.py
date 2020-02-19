import sys
import unittest
import datetime
import math
# Importy wewnętrzne
sys.path.append(r"..\ion_map")
import calculations.common as common

class Test_common(unittest.TestCase):
    
    def test_xyz_to_blh(self):
        p_xyz = (3633815.6800, 1397453.9157,  5035280.8028)
        ref = (0.91586133387, 0.36713367853, 139.91404166352)
        
        p_blh = common.xyz_to_blh(p_xyz)
        self.assertAlmostEqual(p_blh[0], ref[0], places = 11)
        self.assertAlmostEqual(p_blh[1], ref[1], places = 11)
        self.assertAlmostEqual(p_blh[2], ref[2], places = 4)
        
            
    def test_geometric_range(self):
        p1 = (14140733.710, -15191466.432, 16458906.828)
        p2 = (3633815.6800, 1397453.9157,  5035280.8028)
        range = common.geometric_range(p1, p2)
        self.assertEqual(range,  22717544.681481335)
        
    def test_azimuth_elevation(self):
        sat = (14140733.710, -15191466.432, 16458906.828)
        rec = (3633815.6800, 1397453.9157,  5035280.8028)
        ref = (281.4588, 30.1388)
        
        az, el = common.azimuth_elevation(sat, rec)
        az = math.degrees(az)
        el = math.degrees(el)
        
        self.assertAlmostEqual(az, ref[0], places = 4)
        self.assertAlmostEqual(el, ref[1], places = 4)
        
    def test_datetime_to_gpstime(self):
        dt = datetime.datetime(2019, 11, 7, 14, 0, 0)
        week, secs = common.datetime_to_gpstime(dt)
        self.assertEqual(week, 2078)
        self.assertEqual(secs, 396000)
        
    def test_ipp(self):
        blh_site = (0.91586133387, 0.36713367853, 139.9140)
        az_el = (4.912382902151182, 0.526020853586303)
        ionosphere_h = 300
        ref = (52.4759109, 21.0277424)
        
        b_ipp, l_ipp = common.ipp(blh_site, az_el, ionosphere_h)
        b_ipp = math.degrees(b_ipp)
        l_ipp = math.degrees(l_ipp)
        
        
        self.assertAlmostEqual(b_ipp, ref[0], places=7)
        self.assertAlmostEqual(l_ipp, ref[1], places=7)
        
if __name__ == "__main__":
    unittest.main()
    