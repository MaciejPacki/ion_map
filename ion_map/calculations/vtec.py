import math
from constants import r_earth


def single_layer_mapping(stec, el, ionosphere_h):
    f = 1 / ((1 - (math.cos(el) * r_earth / (r_earth + ionosphere_h)) ** 2) ** (-1 / 2))
    return stec * f
