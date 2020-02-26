"""
Funkcje wyznaczania pozycji dla satelitów
"""
# Importy zewnętrzne
import datetime
import math

# Importy wewnętrzne
import calculations.common
from constants import c, GM, OMEGA_E


def OTHER(epoch, nav, site_xyz):
    pass


def GPS(epoch, nav, site_xyz, pseudo):
    """
    Wyznaczanie pozycji dla satelitów GPS
    IN:     epoch (datetime)    - epoka dla której wyznaczna jest pozycja
            nav (dict)          - dane nawigacyjne z pliku rinex dla najbliższej epoki
            site_xyz (truple)   - pozycja odbiornika 
    """

    THRESHOLD = 1e-4

    if nav["SV_health"]:
        return None

    def calculate_xyz(epoch_sec, nav):
        def calculate_E(e, M):
            # Oblicz E wykorzysując metodę Newtona
            def func(e, E, M):
                return E - M - e * math.sin(E)

            def dfunc(e, E, M):
                return 1 - e * math.cos(E)

            # Inicializacjia E
            E = M
            while math.fabs(func(e, E, M)) > 1e-12:
                E -= func(e, E, M) / dfunc(e, E, M)
            return E

        # Wyznacz deltę dla epoki
        tk = epoch_sec - nav["toe"]
        if tk > 302400:
            tk -= 604800
        elif tk < -302400:
            tk += 604800
        else:
            pass
        # Oblicz x y z
        a = nav["sqrtA"] ** 2
        n0 = math.sqrt(GM / a ** 3)
        n = n0 + nav["delta_n"]
        Mk = nav["M0"] + n * tk
        Mk = math.fmod(Mk, 2 * math.pi)

        Ek = calculate_E(nav["e"], Mk)
        q = math.sqrt(1.0 - nav["e"] ** 2)
        nominator = q * math.sin(Ek)
        denominator = math.cos(Ek) - nav["e"]
        Vk = math.atan2(nominator, denominator)
        if Vk < 0:
            Vk += 2 * math.pi
        if Vk > 2 * math.pi:
            Vk -= 2 * math.pi
        Uk = nav["omega"] + Vk
        duk = nav["cuc"] * math.cos(2 * Uk) + nav["cus"] * math.sin(2 * Uk)
        drk = nav["crc"] * math.cos(2 * Uk) + nav["crs"] * math.sin(2 * Uk)
        dik = nav["cic"] * math.cos(2 * Uk) + nav["cis"] * math.sin(2 * Uk)
        uk = Uk + duk
        rk = a * (1.0 - nav["e"] * math.cos(Ek)) + drk
        ik = nav["i0"] + nav["IDOT"] * tk + dik
        lambda_k = (
            nav["OMEGA0"] + (nav["OMEGA_DOT"] - OMEGA_E) * tk - OMEGA_E * nav["toe"]
        )
        Xk_p = rk * math.cos(uk)
        Yk_p = rk * math.sin(uk)
        Xk = Xk_p * math.cos(lambda_k) - Yk_p * math.sin(lambda_k) * math.cos(ik)
        Yk = Xk_p * math.sin(lambda_k) + Yk_p * math.cos(lambda_k) * math.cos(ik)
        Zk = Yk_p * math.sin(ik)
        return Xk, Yk, Zk

    #
    epoch_week, epoch_sec = calculations.common.datetime_to_gpstime(epoch)

    # Oblicz pozycję dla czasu odbioru
    # xyz = calculate_xyz(epoch_sec, nav)
    # Oblicz pozycję dla czasu emisji
    # range = calculations.common.geometric_range(xyz, site_xyz)
    range = pseudo
    range_p = 1
    while math.fabs(range - range_p) > THRESHOLD:
        flight_time = range / c
        xyz = calculate_xyz(epoch_sec - flight_time, nav)
        xyz = calculations.common.correct_earth_rotation(xyz, flight_time, OMEGA_E)
        range_p = range
        range = calculations.common.geometric_range(xyz, site_xyz)
    return xyz
