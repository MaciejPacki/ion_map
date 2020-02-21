"""
Klasy satelitów
"""
# import zewnętrzne
import math
import numpy
# importy wewnętrzne
import calculations.satellite_xyz
import calculations.common
import calculations.obs_combinations
import calculations.arc_detection
import calculations.stec
import calculations.vtec

class Satellite:
    def __init__(self, prn):
        self.prn = prn
        self.system = prn[0]
        self.num = prn[1:]
        self.obs = {}
        self.nav = {}
        self.xyz = {}
        self.azimuth = {}
        self.elevation = {}
        self.ipp = {}
        self.P4 = {}
        self.L4 = {}
        self.MWWL = {}
        self.L4_shifted = {}
        
    @property
    def epochs(self):
        epochs = []
        for epoch in sorted(self.obs.keys()):
            if any([self.obs[epoch][o] == None for o in ['C1', 'P2', 'L1', 'L2']]):
                pass
            else:
                epochs.append(epoch)
        return  epochs
    
    def add_obs(self, epoch_time, obs_data):
        self.obs[epoch_time] = obs_data
            
    def add_nav(self, epoch_time, nav_data):
        self.nav[epoch_time] = nav_data
    
    def get_closest_nav(self, epoch):
        nav_epochs = self.nav.keys()
        closest_epoch = min(nav_epochs, key = lambda x: abs(x - epoch))
        return self.nav[closest_epoch]
    
    def _calculate_xyz(self, site_xyz, calculator):
        for epoch in self.epochs:
            pseudo = self.obs[epoch]["C1"]
            nav = self.get_closest_nav(epoch)
            self.xyz[epoch] = calculator(epoch, nav, site_xyz, pseudo)

    def _calculate_azimuth_and_elevation(self, site_xyz):
        for epoch in self.epochs:
            sat_xyz = self.xyz[epoch]
            if sat_xyz != None:
                azimuth, elevation = calculations.common.azimuth_elevation(sat_xyz, site_xyz)
                self.azimuth[epoch] = azimuth
                self.elevation[epoch] = elevation
            
    def _calculate_ipp(self, site_blh, ionosphere_h):
        # Maska elewacji
        elevation_mask = math.radians(30)
        for epoch in self.epochs:
            if epoch in self.elevation and self.elevation[epoch] > elevation_mask:
                sat_az_el = self.azimuth[epoch], self.elevation[epoch]
                ipp = calculations.common.ipp(site_blh, sat_az_el, ionosphere_h)
                self.ipp[epoch] = ipp
    
    def calculate_P4_L4_MWWL(self, sat_dcb):
        dcb_P1P2 = sat_dcb['P1P2'][self.prn]
        dcb_P1C1 = sat_dcb['P1C1'][self.prn]
        for epoch in self.epochs:
            if epoch in self.ipp:
                obs = self.obs[epoch]
                P4 = calculations.obs_combinations.P4(obs, dcb_P1P2, dcb_P1C1)
                L4 = calculations.obs_combinations.L4(obs)
                MWWL = calculations.obs_combinations.MWWL(obs)
                if P4 != None:
                    self.P4[epoch] = P4
                if L4 != None:
                    self.L4[epoch] = L4
                if MWWL != None:
                     self.MWWL[epoch] = MWWL
                                  
    def calculate_L4_shifted(self):
        val = calculations.obs_combinations.L4_shifted(self.arcs, self.L4, self.P4)
        self.L4_shifted = val

    def calculate_STEC(self):
        self.STEC_P4 = {}
        self.STEC_L4 = {}
        for epoch, P4 in self.P4.items():
            c_STEC = calculations.stec.from_P4(P4)
            self.STEC_P4[epoch] = c_STEC
        for epoch, L4 in self.L4_shifted.items():
            c_STEC = calculations.stec.from_L4(L4)
            self.STEC_L4[epoch] = c_STEC
            
    def calculate_VTEC(self, ionosphere_h):
        self.VTEC = {}
        for epoch in self.STEC_L4.keys():
            stec = self.STEC_L4[epoch]
            el = self.elevation[epoch]    
            c_VTEC = calculations.vtec.single_layer_mapping(stec, el, ionosphere_h)
            self.VTEC[epoch] = c_VTEC
    
    def calculate_arcs(self):
        if self.L4 != {}:
            self.arcs = calculations.arc_detection.arc_detector(self.L4, self.MWWL)
        else:
            self.arcs = {}

    def prepare_out_data(self):
        out_data = ""
        for epoch in self.epochs:
            line = ""
            if epoch in self.STEC:
                date = epoch.strftime("%Y-%m-%d %H:%M:%S")
                prn = self.prn
                x = self.xyz[epoch][0]
                y = self.xyz[epoch][1]
                z = self.xyz[epoch][2]
                az = math.degrees(self.azimuth[epoch])
                el = math.degrees(self.elevation[epoch])
                ipp_lat = math.degrees(self.ipp[epoch][0])
                ipp_lon = math.degrees(self.ipp[epoch][1])
                VTEC = self.VTEC[epoch]
                
                line += "{:>20}{:>10}{:>-20.3f}{:>-20.3f}{:>-20.3f}".format(date, prn, x, y, z)
                line += "{:>-20.4f}{:>-20.4f}{:>-20.7f}{:>-20.7f}{:>-20.7f}\n".format(az, el, ipp_lat, ipp_lon, VTEC)
                
            out_data += line    
        return out_data
        
    def prepare_out_hour(self, hour):
        out = []
        for epoch, L4 in self.L4_shifted.items():
            if epoch.hour == hour:
                out.append([epoch, self.prn, math.degrees(self.ipp[epoch][0]), math.degrees(self.ipp[epoch][1]), 
                            self.VTEC[epoch]]) 
        return out
        
        
class Satellite_GPS(Satellite):
    
    def __init__(self, prn):
        super().__init__(prn)    
        
    def calculate_xyz(self, site_xyz):
        calculator = calculations.satellite_xyz.GPS
        self._calculate_xyz(site_xyz, calculator)
        
    def calculate_azimuth_and_elevation(self, site_xyz):
        self._calculate_azimuth_and_elevation(site_xyz)
        
    def calculate_ipp(self, site_blh, ionosphere_h):
        self._calculate_ipp(site_blh, ionosphere_h)
        
        
class Satellite_OTHER(Satellite):
    
    def __init__(self, prn):
        super().__init__(prn)
        
    def calculate_azimuth_and_elevation(self, site_xyz):
        pass
    
    def calculate_xyz(self, site_xyz):
        pass
    
    def calculate_ipp(self, site_blh, ionosphere_h):
        pass
        
    def calculate_arcs(self):
        pass
    
    def calculate_L4_shifted(self):
        pass
    
    def calculate_P4_L4_MWWL(self, sat_dcb):
        pass
    

