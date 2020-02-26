"""
Klasa stacji
"""
import calculations.common


class Site:
    def __init__(self, name, network, xyz, epochs, satellites):
        self.name = name
        self.network = network
        self.xyz = xyz
        self.epochs = epochs
        self.satellites = satellites

    @property
    def blh(self):
        blh = calculations.common.xyz_to_blh(self.xyz)
        return blh

    def calculate_satellites_xyz(self):
        for satellite in self.satellites.values():
            satellite.calculate_xyz(site_xyz=self.xyz)

    def calculate_satellites_azimuths_and_elevations(self):
        for satellite in self.satellites.values():
            satellite.calculate_azimuth_and_elevation(site_xyz=self.xyz)

    def calculate_satellites_ipp(self, ionosphere_h):
        for satellite in self.satellites.values():
            satellite.calculate_ipp(self.blh, ionosphere_h)

    def calculate_satellites_P4_L4_MWWL(self, sat_dcb):
        for satellite in self.satellites.values():
            satellite.calculate_P4_L4_MWWL(sat_dcb)

    def calculate_satellites_arcs(self):
        for satellite in self.satellites.values():
            satellite.calculate_arcs()

    def calculate_satellites_L4_shifted(self):
        for satellite in self.satellites.values():
            satellite.calculate_L4_shifted()

    def calculate_satellites_STEC(self):
        for satellite in self.satellites.values():
            satellite.calculate_STEC()

    def calculate_satellites_VTEC(self, ionosphere_h):
        for satellite in self.satellites.values():
            satellite.calculate_VTEC(ionosphere_h)

    def get_print_data(self):
        out = "#{:>19}{:>10}{:>20}{:>20}{:>20}{:>20}{:>20}{:>20}{:>20}{:>20}\n".format(
            "Date",
            "System",
            "X [m]",
            "Y [m]",
            "Z [m]",
            "Az [deg]",
            "El [deg]",
            "IPP lat [deg]",
            "IPP lon [deg]",
            "VTEC [TECU]",
        )
        for satellite in self.satellites.values():
            out += satellite.prepare_out_data()
        return out

    def get_hour_data(self):
        hours = {}
        for hour in range(0, 24):
            c_hour = []
            for satellite in self.satellites.values():
                c_hour += satellite.prepare_out_hour(hour)
            hours[hour] = c_hour

        for hour, lines in hours.items():
            lines.sort(key=lambda x: x[0])

        return hours
