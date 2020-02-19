"""
Parser plików obs rnx 3
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
    
    
def parse_obs_type_order(header):
    index = get_line_index_ending_with(header, "SYS / # / OBS TYPES")
    obs_order = {}
    for full_line in header[index:]:
        if full_line[60:79] != "SYS / # / OBS TYPES":
            break
        else:
            line = full_line[:60].split()
            if line[0].isalpha():
                system = line[0]
                obs_order[system]= line[2:]
            else:
                obs_order[system] += line
    return obs_order
    
    
def parse_site_name(header):
    # Znajdz nazwę stacji w nagłówku
    index = get_line_index_ending_with(header, "MARKER NAME")
    return header[index].split()[0]        


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
    
def parse_new_epoch(line):
    time_raw = line.split()[1:-2]
    # Zmniejsz precyzję sekund
    time_raw[-1] = time_raw[-1][:-1]
    #Stwórz obiekt epoki
    time_str = "".join(time_raw)
    time = datetime.datetime.strptime(time_str, '%Y%m%d%H%M%S.%f')
    return time
    
    
def parse_sat_obs(line, obs_order):
    # Prn satelity
    prn = line[:3]
    # Rodzaj systemu
    sat_system = prn[0]
    # Linia obserwacji bez prn
    data_line = line[3:]
    # Typ obserwacji dla danego systemu
    obs_types = obs_order[sat_system]
    obs_types_number = len(obs_types)
    
    _obs = []
    for i in range(obs_types_number):
        beg = i * 16
        end = (i + 1) * 16 - 2
        try:
            value = float(data_line[beg:end])
            if value == 0:
                value = None
            else:
                pass
        except ValueError:
            value = None
        _obs.append(value)
        
    obs = dict(zip(obs_types, _obs))
    return prn, obs


def get_current_data(data, epoch_tittle_index, epoch_lines):
    beg = epoch_tittle_index + 1
    end = epoch_tittle_index + epoch_lines
    return data[beg:end]

def transform_obs(obs):
    obs['C1'] = None
    obs['P2'] = None
    obs['L1'] = None
    obs['L2'] = None
    for freq in ['1', '2']:
        if freq == '1':
            aux = 'C1'
        else:
            aux = 'P2'
        for attr in ["P", "C", "D", "Y", "M", "N", "I", "Q", "S", "L", "X"]:
            c_obs = 'C' + freq + attr
            p_obs = 'L' + freq + attr     
            try:
                if obs[c_obs] != None and obs[p_obs] != None:    
                    obs[aux] = obs[c_obs]    
                    obs['L' + freq] = obs[p_obs] 
                    break
            except KeyError:
                pass
    return obs
       
def read(lines):
    """
    IN:     lines (str)     - linie pliku
    OUT:    site (Site)     - instancja stacji
    """
    
    def read_flag0():
        current_data = get_current_data(data, epoch_tittle_index, epoch_lines_number)
        epoch_time = parse_new_epoch(epoch_tittle)
        epochs.append(epoch_time)
        
        for line in current_data:
            prn, obs = parse_sat_obs(line, obs_type_order)
            obs = transform_obs(obs)
            system = prn[0]
            try:
                satellites[prn].add_obs(epoch_time, obs)
            except KeyError:
                if system == "G":
                    satellites[prn] = Satellite.Satellite_GPS(prn)
                else:
                    satellites[prn] = Satellite.Satellite_OTHER(prn)
                satellites[prn].add_obs(epoch_time, obs)                
                
    # Znajdz indeks końca nagłówka.    
    header_end_index = get_line_index_ending_with(lines, "END OF HEADER")
    # Podział na nagłówek i dane
    header = lines[:header_end_index + 1]
    data = lines[header_end_index + 1 :]
    
    # Czytaj nagłówek
    obs_type_order = parse_obs_type_order(header)
    site_name = parse_site_name(header)
    site_network = parse_site_network(header)
    site_xyz = parse_site_xyz(header)
    
    # Inicializuj 
    epochs = []
    satellites = {}
    epoch_tittle_index = 0
    
    while True:
        try:
            epoch_tittle = data[epoch_tittle_index]
        except IndexError:
            break
            
        epoch_flag = epoch_tittle[31]
        epoch_lines_number = int(epoch_tittle[32:35])
        if epoch_flag == "0":
            read_flag0()
        #TODO Dopisać inne flagi
        else:
            pass
        epoch_tittle_index += epoch_lines_number + 1
    site = Site.Site(site_name, site_network, site_xyz, epochs, satellites)
    return site

