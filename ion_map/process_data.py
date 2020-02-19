from readers import rnx_reader, dcb_reader

def site(o_file, n_file, dcb_P1C1_file, dcb_P1P2_file):
    site = rnx_reader.read(o_file, n_file)
    sat_dcb = dcb_reader.read(dcb_P1P2_file, dcb_P1C1_file)

    site.calculate_satellites_xyz()
    site.calculate_satellites_azimuths_and_elevations()
    # Wysokosc wartstwy jonosfery w km
    site.calculate_satellites_ipp(ionosphere_h=350)
    site.calculate_satellites_P4_L4_MWWL(sat_dcb)
    site.calculate_satellites_arcs()
    site.calculate_satellites_L4_shifted()

    site.calculate_satellites_STEC()
    site.calculate_satellites_VTEC(ionosphere_h=350)
    
    return site