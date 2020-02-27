"""
Parser plików obs rinex (2.11 i 3.03)
"""
# Importy wewnętrzne
import readers.rnx3_nav as rnx3_nav


def read(obs_path):
    """
    Główny parser
    IN:     nav_path (str) - scieżka pliku nav
    OUT:    nav    - 
    """
    # Czytaj plik obs
    with open(obs_path, "r") as file:
        lines = file.readlines()
        first_line = lines[0]
        # Znajdz wersję pliku rinex,
        rnx_version = first_line[5]
        # Znajdz typ pliku
        rnx_type = first_line[20]

        if rnx_type == "N":
            if rnx_version == "3":
                nav = rnx3_nav.read(lines)
            else:
                print(f"Trouble reading {obs_path} file. Unsupported format version.")
        else:
            print(f"Trouble reading {obs_path} file. Not a observation rinex file.")
    return nav
