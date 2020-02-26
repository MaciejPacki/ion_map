"""
Krótkie, często wykorzystywane funkcje obliczeniowe
"""

import datetime
import numpy
import math
from constants import r_earth, e2, a, secs_in_week, init_gps_epoch


def xyz_to_blh(xyz):
    x, y, z = xyz
    threshold = 10 ** -16

    p = math.sqrt(x ** 2 + y ** 2)
    # Wyznacz l
    l = math.atan2(y, x)
    # Wyznacz b i h
    b = math.atan2((z / p), (1 - e2))
    while True:
        N = a / math.sqrt(1 - e2 * (math.sin(b) ** 2))
        h = p / math.cos(b) - N
        new_b = math.atan2((z / p), (1 - (N / (N + h)) * e2))
        if abs(new_b - b) < threshold:
            break
        else:
            b = new_b
    return (new_b, l, h)


def geometric_range(xyz_sat, xyz_rec):
    delta_x2 = (xyz_sat[0] - xyz_rec[0]) ** 2
    delta_y2 = (xyz_sat[1] - xyz_rec[1]) ** 2
    delta_z2 = (xyz_sat[2] - xyz_rec[2]) ** 2
    out = math.sqrt(delta_x2 + delta_y2 + delta_z2)
    return out


def azimuth_elevation(xyz_sat, xyz_rec):

    sat = numpy.array(xyz_sat)
    rec = numpy.array(xyz_rec)

    range = geometric_range(xyz_sat, xyz_rec)

    b, l, h = xyz_to_blh(xyz_rec)

    p_hat = numpy.subtract(sat, rec) / range
    e_hat = numpy.array([-math.sin(l), math.cos(l), 0])
    n_hat = numpy.array(
        [-math.cos(l) * math.sin(b), -math.sin(l) * math.sin(b), math.cos(b)]
    )
    u_hat = numpy.array(
        [math.cos(l) * math.cos(b), math.sin(l) * math.cos(b), math.sin(b)]
    )

    azimuth = math.atan2(numpy.dot(p_hat, e_hat), numpy.dot(p_hat, n_hat))
    elevation = math.asin(numpy.dot(p_hat, u_hat))

    if azimuth < 0:
        azimuth += 2 * math.pi
    elif azimuth > 2 * math.pi:
        azimuth -= 2 * math.pi

    if elevation < 0:
        elevation += 2 * math.pi
    elif elevation > 2 * math.pi:
        elevation -= 2 * math.pi

    return azimuth, elevation


def ipp(blh_site, az_el, ionosphere_h):
    b, l, _ = blh_site
    az, el = az_el

    q = r_earth / (r_earth + ionosphere_h)
    psi = math.pi / 2.0 - el - math.asin(q * math.cos(el))

    b_ipp = math.asin(
        math.sin(b) * math.cos(psi) + math.cos(b) * math.sin(psi) * math.cos(az)
    )
    l_ipp = psi * math.sin(az) / math.cos(b_ipp) + l

    return b_ipp, l_ipp


def correct_earth_rotation(xyz, flight_time, earth_rotation_rate):
    x, y, z = xyz
    alpha = flight_time * earth_rotation_rate
    new_x = x * math.cos(alpha) + y * math.sin(alpha)
    new_y = y * math.cos(alpha) - x * math.sin(alpha)
    return new_x, new_y, z


def datetime_to_gpstime(dt):
    delta = (dt - init_gps_epoch).total_seconds()
    week = delta // secs_in_week
    secs = delta % secs_in_week
    return week, secs


def gpstime_to_datetime(week, secs):
    return init_gps_epoch + datetime.timedelta(seconds=week * secs_in_week + secs)


def datetime_to_secs_of_day(dt):
    return dt.hour * 3600 + dt.minute * 60 + dt.second
