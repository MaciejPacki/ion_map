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


class Satellite_GPS:
    def __init__(self, prn):
        self.prn = prn
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

    def calculate_eligible_epochs(self):
        epochs = []
        for epoch in sorted(self.obs.keys()):
            if any([self.obs[epoch][o] == None for o in ["C1", "P2", "L1", "L2"]]):
                pass
            else:
                epochs.append(epoch)
        self.epochs = epochs

    def add_obs(self, epoch_time, obs_data):
        self.obs[epoch_time] = obs_data

    def calculate_xyz(self, site_xyz, nav):
        for epoch in self.epochs:
            pseudo = self.obs[epoch]["C1"]
            nav_epochs = nav[self.prn].keys()
            closest_nav_epoch = min(nav_epochs, key=lambda x: abs(x - epoch))
            closest_nav = nav[self.prn][closest_nav_epoch]
            self.xyz[epoch] = calculations.satellite_xyz.GPS(
                epoch, closest_nav, site_xyz, pseudo
            )

    def calculate_azimuth_and_elevation(self, site_xyz):
        for epoch in self.epochs:
            sat_xyz = self.xyz[epoch]
            if sat_xyz != None:
                azimuth, elevation = calculations.common.azimuth_elevation(
                    sat_xyz, site_xyz
                )
                self.azimuth[epoch] = azimuth
                self.elevation[epoch] = elevation

    def calculate_ipp(self, site_blh, ionosphere_h, elev_mask):
        elevation_mask = math.radians(elev_mask)
        for epoch in self.epochs:
            if epoch in self.elevation and self.elevation[epoch] > elevation_mask:
                sat_az_el = self.azimuth[epoch], self.elevation[epoch]
                ipp = calculations.common.ipp(site_blh, sat_az_el, ionosphere_h)
                self.ipp[epoch] = ipp

    def calculate_P4_L4_MWWL(self, sat_dcb):
        dcb_P1P2 = sat_dcb["P1P2"][self.prn]
        dcb_P1C1 = sat_dcb["P1C1"][self.prn]
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

    def prepare_out_hour(self, hour):
        out = []
        for epoch, L4 in self.L4_shifted.items():
            if epoch.hour == hour:
                out.append(
                    [
                        epoch,
                        self.prn,
                        math.degrees(self.ipp[epoch][0]),
                        math.degrees(self.ipp[epoch][1]),
                        self.VTEC[epoch],
                    ]
                )
        return out
