"""
Parser plików DCB (tylko sat)
"""

from constants import c
def read(P1P2_path, P1C1_path):
    
    def _read(f_path):
        dcb = {}
        with open(f_path, 'r') as file:
            lines = file.readlines()
            for line in lines[7:]:
                try:
                    data = line.split()
                    sat = data[0]
                    val = float(data[1]) * 10e-10 * c
                    dcb[sat] = val
                except IndexError:
                    pass
        return dcb
        
    dcb = {}
    dcb['P1P2'] = _read(P1P2_path)
    dcb['P1C1'] = _read(P1C1_path)
    return dcb