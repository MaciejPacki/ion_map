"""
Klasa stacji
"""
import calculations.common


class Site:
    def __init__(self, name, network, xyz, satellites):
        self.name = name
        self.network = network
        self.xyz = xyz
        self.satellites = satellites

    def __str__(self):
        out = f"SITE: {self.name}\n"
        out += f"SATS: {len(self.satellites.keys())}\n"
        out += f"{sorted(list(self.satellites.keys()))}"
        return out

    @property
    def blh(self):
        blh = calculations.common.xyz_to_blh(self.xyz)
        return blh

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

    def process_data(self, nav, sat_dcb, ionosphere_h, elev_mask):
        for satellite in self.satellites.values():
            satellite.calculate_eligible_epochs()
            satellite.calculate_xyz(self.xyz, nav)
            satellite.calculate_azimuth_and_elevation(self.xyz)
            satellite.calculate_ipp(self.blh, ionosphere_h, elev_mask)
            satellite.calculate_P4_L4_MWWL(sat_dcb)
            satellite.calculate_arcs()
            satellite.calculate_L4_shifted()
            satellite.calculate_STEC()
            satellite.calculate_VTEC(ionosphere_h)
