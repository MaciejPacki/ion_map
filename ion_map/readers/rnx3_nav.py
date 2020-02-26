"""
Parser plików nav rnx 3
"""

# Import zewnętrzne
import datetime

# Stałe
FRAMES_PER_SYSTEM = {"G": 8, "E": 8, "J": 8, "I": 8, "C": 8, "R": 4, "S": 4}


def get_line_index_ending_with(lines, phrase):
    # Zwraca pierwszy indeks encji lines kończący się na wyrażenie phrase
    for index in range(len(lines)):
        line = lines[index].rstrip("\n\r")
        line = line.rstrip()
        if line.endswith(phrase):
            return index
        else:
            pass
    return None


def convert_epoch_to_datetime(epoch):
    return datetime.datetime.strptime(epoch, "%Y %m %d %H %M %S")


def get_current_frames(system, data, frame0_index):
    end = frame0_index + FRAMES_PER_SYSTEM[system]
    return data[frame0_index:end]


def parse_GPS_data(satellite, data):

    keys = [
        "toc",
        "a0",
        "a1",
        "a2",
        "IODE",
        "crs",
        "delta_n",
        "M0",
        "cuc",
        "e",
        "cus",
        "sqrtA",
        "toe",
        "cic",
        "OMEGA0",
        "cis",
        "i0",
        "crc",
        "omega",
        "OMEGA_DOT",
        "IDOT",
        "L2",
        "gps_week",
        "L2_P_flag",
        "SV_acc",
        "SV_health",
        "TGD",
        "IODC",
        "transmision_time",
        "fit_interval",
    ]
    values = []
    for line in data:
        # Przygotuj linię
        line = line.rstrip("\n\r")
        line = line[4:]
        # Czytaj wartości
        for i in range(4):
            beg = i * 19
            end = (i + 1) * 19
            value = line[beg:end]
            if "d" in value:
                value = value.replace("d", "e")
            elif "D" in value:
                value = value.replace("D", "e")
            values.append(value)
    # Przygotuj wartości
    del values[-2:]
    values[0] = convert_epoch_to_datetime(values[0])
    values[1:] = list(map(float, values[1:]))
    final_values = dict(zip(keys, values))
    # Dodaj dane do obiektu satelity
    satellite.add_nav(final_values["toc"], final_values)


def read(lines, site):
    # Znajdz indeks końca nagłówka.
    header_end_index = get_line_index_ending_with(lines, "END OF HEADER")
    # Podział na nagłówek i dane
    header = lines[: header_end_index + 1]
    data = lines[header_end_index + 1 :]

    frame0_index = 0

    while True:
        # Sprawdz system, jeśli nie można przeczyczać -
        # przeczytano cały plik
        try:
            prn = data[frame0_index][:3]
            system = prn[0]
        except IndexError:
            break
        # Sprawdz czy satelita jest obserwowany przez stację
        try:
            satellite = site.satellites[prn]
            # Czytaj aktualne klatki
            frames = get_current_frames(system, data, frame0_index)
            # Czytaj obserwację dla odpowiedniego systemu
            # TODO Dopisać resztę systemów
            if system == "G":
                parse_GPS_data(satellite, frames)
            else:
                pass
        except KeyError:
            pass
        # Oblicz indeks następnej klatki 0
        frame0_index += FRAMES_PER_SYSTEM[system]
    return site
