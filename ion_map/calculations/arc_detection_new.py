from constants import wl_lambda, TEC_const
import numpy as np


def MWWL_detector(L4, MWWL):
    epochs = sorted(L4)
    cs_terms = []
    cs = []
    for i in range(1, len(epochs)):
        cs_term = MWWL[epochs[i - 1]] / wl_lambda - MWWL[epochs[i]] / wl_lambda
        cs_terms.append(cs_term)
        if cs_term > 4 * np.std(cs_terms):
            cs.append(epochs[i])
    return cs


def TECR_detector(L4):
    epochs = sorted(L4)
    cs_terms = []
    cs = []
    for i in range(1, len(epochs)):
        cs_term = MWWL[epochs[i - 1]] / wl_lambda - MWWL[epochs[i]] / wl_lambda
        cs_terms.append(cs_term)
        if cs_term > 4 * np.std(cs_terms):
            cs.append(epochs[i])
    return cs


def arc_detector(L4, MWWL):
    return MWWL_detector(L4, MWWL)
