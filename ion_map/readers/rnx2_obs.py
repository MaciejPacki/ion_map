"""
Parser plików obs rnx 2
"""
# Importy wewnętrzne
import data_holders.Satellite as Satellite
import data_holders.Site as Site
# Import zewnętrzne
import datetime


def get_line_index_ending_with(lines, phrase):
    # Zwraca pierwszy indeks encji lines kończący się na wyrażenie phrase
    for index in range(len(lines)):
        line = lines[index].rstrip("\n\r")
        line = line.rstrip()
        if line.endswith(phrase):
            return index 
    return None


def parse_site_name(header):
    # Znajdz nazwę stacji w nagłówku
    index = get_line_index_ending_with(header, "MARKER NAME")
    out = header[index].split()[0]    
    return out   


def parse_site_network(header):
    # Znajdz nazwę stacji w nagłówku
    index = get_line_index_ending_with(header, "OBSERVER / AGENCY")
    aux = header[index][:60].strip().split()
    out = " ".join(aux)
    return out


def parse_site_xyz(header):
    # Znajdz przybliżoną pozycję xyz stacji w nagłówku
    index = get_line_index_ending_with(header, "APPROX POSITION XYZ")
    out = header[index].split()[:3]
    out = tuple(map(float, out))
    return out


def parse_obs_type_order(header):
    # Znajdz kolejność obserwacji i ich liczbę.
    obs_type_order = []
    index = get_line_index_ending_with(header, "# / TYPES OF OBSERV")
    obs_type_number = int(header[index][:6])
    # Jeśli więcej niż 9 typów obserwacji, należy
    # wykorzystać następne linies
    for full_line in header[index:]:
        if full_line[60:79] != "# / TYPES OF OBSERV":
            break
        else:
            line = full_line[6:60].split()
            obs_type_order += line
    return obs_type_number, obs_type_order 


def parse_lines_per_sat(obs_type_number):
    if obs_type_number % 5 == 0:
        stay_in_line = 0
    else: 
        stay_in_line = 1
    number_of_lines = obs_type_number//5 + stay_in_line 
    return number_of_lines


def parse_epoch_time(epoch_title):
    def pad_with_zeros(value):
        # Przygotowuje wartość do konwersji do datetime
        if len(value) == 1:
            return value.zfill(2)
        elif len(value) == 9:
            return value.zfill(10)[:-1] 
        elif len(value) == 10:
            return value[:-1]
        else:
            return value  
    time_raw = epoch_title[1:26].split()
    time_padded = list(map(pad_with_zeros, time_raw))
    time_str = "".join(time_padded)
    return datetime.datetime.strptime(time_str, '%y%m%d%H%M%S.%f')


def parse_sat_number(epoch_title):
    return int(epoch_title[29:32])


def calculate_epoch_title_length(sat_number):
    if sat_number % 12 == 0:
        stay_in_line = 0
    else:
        stay_in_line = 1
    number_of_lines = sat_number//12 + stay_in_line
    return number_of_lines


def parse_sat_order(epoch_title_index, data, sat_number, epoch_title_length):
    sat_order = []
    for extra_line in range(epoch_title_length):
        line = data[epoch_title_index + extra_line]
        sat = line[32:]
        for i in range(12):
            beg = 3 * i
            end = 3 * (i + 1)
            value = sat[beg:end]
            sat_order.append(value)
            if len(sat_order) == sat_number:
                break
    return sat_order


def parse_obs_in_line(line, obs, obs_type_number):
    line = line.rstrip("\n\r")
    # Czytaj obserwacje dla satelity, max 5 obserwacji w 
    # linii.
    for obs_in_line in range(5):
        # Obserwacje zpaisywane w 16 znakowych interwałach,
        # 2 ostatnie znaki winny być odrzucone.
        beg = obs_in_line * 16
        end = (obs_in_line + 1) * 16 - 2 
        try:
            value = float(line[beg:end])
            if value == 0:
                value = None
            else:
                pass
        except ValueError:
            value = None
        obs.append(value)
        if len(obs) == obs_type_number:
            break  
        else:
            continue
            

def read(lines):
    """
    IN:     lines (str)     - linie pliku
    OUT:    site (Site)     - instancja stacji
    """
    # Funkcje czytania epoch dla danej flagi
    def read_flag0():
        # Nowa epoka, inicializuj zmienne
        epoch_time = parse_epoch_time(epoch_title)
        sat_number = parse_sat_number(epoch_title)
        epoch_title_length = calculate_epoch_title_length(sat_number)
        sat_order = parse_sat_order(epoch_title_index, data, sat_number, epoch_title_length)
        obs_index = epoch_title_index + epoch_title_length
        # Dodaj epokę do listy epok
        epochs.append(epoch_time)
        # Czytaj obserwacje dla każego satelity
        for sat_index in range(sat_number):
            _obs = []
            # Wczytaj wszystkei obserwacje 
            for i in range(lines_per_sat):
                line = data[obs_index + i]
                parse_obs_in_line(line, _obs, obs_type_number)
            obs_index += lines_per_sat
            # Utwórz słownik obserwacji
            obs = dict(zip(obs_type_order, _obs))
            # Utwórz obiekt satelity
            prn = sat_order[sat_index]
            system = prn[0]
            try:
                satellites[prn].add_obs(epoch_time, obs)
            # Utwórz obiekt satelity dla odpowiedniego systemu
            except KeyError:
                if system == "G":
                    satellites[prn] = Satellite.Satellite_GPS(prn)
                else:
                    satellites[prn] = Satellite.Satellite_OTHER(prn)
                satellites[prn].add_obs(epoch_time, obs)
        return obs_index

    def read_flag4():
        extra_lines = parse_sat_number(epoch_title)
        # Następny nagłówek epocki 
        return epoch_title_index + extra_lines + 1

    # Znajdz indeks końca nagłówka.    
    header_end_index = get_line_index_ending_with(lines, "END OF HEADER")
    # Podział na nagłówek i dane
    header = lines[: header_end_index + 1]
    data = lines[header_end_index + 1:]
    
    # Czytaj nagłówek
    obs_type_number, obs_type_order = parse_obs_type_order(header)
    lines_per_sat = parse_lines_per_sat(obs_type_number)
    site_name = parse_site_name(header)
    site_network = parse_site_network(header)
    site_xyz = parse_site_xyz(header)

    # Epoch tittle to nagłówek epoki, inicializuj zmienne 
    epoch_title_index = 0
    epoch_title = data[epoch_title_index]
    epochs = []
    satellites = {}

    # Czytaj dane
    while True:
        epoch_flag = epoch_title[28]
        if epoch_flag == "0":
            epoch_title_index = read_flag0()
        elif epoch_flag == "4":
            epoch_title_index = read_flag4()
        else:
            print("Unknown epoch flag")
        # Jeśli nie można wczytać następne nagłówka epoki,
        # przeczytano cały plik
        try:
            epoch_title = data[epoch_title_index]
        except IndexError:
            site = Site.Site(site_name, site_network, site_xyz, epochs, satellites)
            break
    return site

