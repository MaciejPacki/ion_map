import os
import datetime
import numpy as np
from scipy import interpolate

import readers.ionex as ionex
from constants import TEC_const, c


def get_closest_number(n, m):
    q = int(n / m)
    n1 = m * q
    if (n * m) > 0:
        n2 = m * (q + 1)
    else:
        n2 = m * (q - 1)

    return n1, n2


def interpolator(observed, map):
    lat, lon, tec = observed

    map_lats = np.array(get_closest_number(lat, 2.5))
    map_lons = np.array(get_closest_number(lon, 5))
    map_lats = np.repeat(map_lats, 2)
    map_lons = np.tile(map_lons, 2)
    map_tec = [map[map_lat][map_lon] for map_lat, map_lon in zip(map_lats, map_lons)]
    my_inter = interpolate.interp2d(map_lons, map_lats, map_tec)
    inter_tec = float(my_inter(lon, lat))
    s = inter_tec - tec
    st = s / TEC_const
    sc = st / c
    print(
        "{:>20.4f}{:>20.4f}{:>20.4f}{:>20.4f}{:>20.2e}".format(
            inter_tec, tec, s, st, sc
        )
    )


comparison = {
    "BOGI": 3.723,
    "BOGO": -4.123,
    "BOR1": 19.898,
    "JOZ2": 11.385,
    "JOZE": -10.638,
    "LAMA": 14.441,
    "WROC": 19.056,
}


dir = r"C:\users\macie\Desktop\ion_map\ion_map\TEST_OUT"
ion_file = r"C:\Users\macie\Desktop\ion_map\tests\test_files\igsg0760.15i"

ionex_map = ionex.read(ion_file)
hour = datetime.datetime(2015, 3, 17, 8)
obs = {}
for file in os.listdir(dir):
    site = file[:4]
    if site in comparison:
        obs[site] = []
        file_path = dir + "\\" + file
        with open(file_path, "r") as file:
            lines = file.readlines()
        for line in lines[1:]:
            if line[:20] != r" 2015/03/17 08:00:00":
                break
            data = [float(x) for x in line.split()[3:]]
            obs[site].append(data)

# for site in obs:
#     print(site, comparison[site])
#     for o in obs[site]:
#         interpolator(o, ionex_map[hour])
#
print(ionex_map[hour][50])
