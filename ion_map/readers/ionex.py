import datetime


def get_line_indices_ending_with(lines, phrase):
    out = []
    # Zwraca pierwszy indeks encji lines kończący się na wyrażenie phrase
    for index in range(len(lines)):
        line = lines[index].rstrip("\n\r")
        line = line.rstrip()
        if line.endswith(phrase):
            out.append(index)
    return out
    
    
def transform_date_line(line):
    dates = [int(x) for x in line.split()[:-4]]
    return datetime.datetime(*dates)


def get_data(data_lines):
    data = {}
    data_lines = [line.split() for line in data_lines]
    data_lines = [x for line in data_lines for x in line]
    lon = -180
    for tec in data_lines:
        data[lon] = float(tec) / 10
        lon += 5
    return data
    
    
def read(obs_path):
    ionex_map = {}
    with open(obs_path, "r") as file:
        lines = file.readlines()
    start_map_indicies = get_line_indices_ending_with(lines, "START OF TEC MAP")
    
    for i in range(len(start_map_indicies)-1):
        start_map_index = start_map_indicies[i]
        end_map_index = start_map_indicies[i+1]-1
        map_date = transform_date_line(lines[start_map_index+1])
        ionex_map[map_date] = {}
        for j in range(start_map_index+2, end_map_index, 6):
            lat = float(lines[j][:8])
            data = get_data(lines[j+1:j+6])
            ionex_map[map_date][lat] = data
    return ionex_map
