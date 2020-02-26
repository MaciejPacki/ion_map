"""
Parser plików rinex (2.11 i 3.03)
"""
# Importy wewnętrzne
import readers.rnx2_obs as rnx2_obs
import readers.rnx3_nav as rnx3_nav
import readers.rnx3_obs as rnx3_obs


def read(obs_path, nav_path):
    """
    Główny parser
    IN:     obs_path (str) - sciezka pliku obs
            nav_path (str) - scieżka pliku nav
    OUT:    site (Site)    - obiekt stacji
    """
    # Czytaj plik obs
    with open(obs_path, "r") as file:
        lines = file.readlines()
        first_line = lines[0]
        # Znajdz wersję pliku rinex,
        rnx_version = first_line[5]
        # Znajdz typ pliku
        rnx_type = first_line[20]
        #
        if rnx_type == "O":
            if rnx_version == "2":
                site = rnx2_obs.read(lines)
                site.rnx_obs_version = 2
            elif rnx_version == "3":
                site = rnx3_obs.read(lines)
                site.rnx2_obs_version = 3
            else:
                print(f"Trouble reading {obs_path} file. Unsupported format version.")
        else:
            print(f"Trouble reading {obs_path} file. Not a observation rinex file.")
    # Czytaj plik nav
    with open(nav_path, "r") as file:
        lines = file.readlines()
        first_line = lines[0]
        # Znajdz wersję pliku rinex,
        rnx_version = first_line[5]
        # Znajdz typ pliku
        rnx_type = first_line[20]
        #
        if rnx_type == "N":
            if rnx_version == "3":
                site = rnx3_nav.read(lines, site)
            else:
                print(f"Trouble reading {nav_path} file. Unsupported format version.")
        else:
            print(f"Trouble reading {nav_path} file. Not a navigation rinex file.")
    return site
