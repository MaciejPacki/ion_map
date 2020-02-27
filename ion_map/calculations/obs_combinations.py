import math, statistics
from constants import L1_freq, L2_freq, L1_lambda, L2_lambda, c


def P4(obs, dcb_P1P2, dcb_P1C1):
    P4 = None
    try:
        P4 = obs["P2"] - obs["C1"] + dcb_P1P2 - dcb_P1C1

    except TypeError:
        pass
    return P4


def L4(obs):
    L4 = None
    try:
        L4 = obs["L1"] * L1_lambda - obs["L2"] * L2_lambda
    except TypeError:
        pass
    return L4


def MWWL(obs):
    MWWL = None
    try:
        MWWL = (L1_freq * L1_lambda * obs["L1"] - L2_freq * L2_lambda * obs["L2"]) / (
            L1_freq - L2_freq
        ) - (L1_freq * obs["C1"] + L2_freq * obs["P2"]) / (L1_freq + L2_freq)
    except TypeError:
        pass
    return MWWL


def L4_shifted(arcs, L4, P4):
    L4_shifted = {}
    epochs = sorted(L4.keys())
    for arc in arcs:
        # Znajdz łuk
        arc_beg, arc_end = arc
        arc_beg_index = epochs.index(arc_beg)
        arc_end_index = epochs.index(arc_end)
        current_epochs = epochs[arc_beg_index : arc_end_index + 1]
        L4_plus_P4 = []
        for epoch in current_epochs:
            L4_plus_P4.append(L4[epoch] - P4[epoch])
        my_median = statistics.median(L4_plus_P4)
        # Oblicz L4_shifted dla każdej epoki
        for epoch in current_epochs:
            L4_shifted[epoch] = L4[epoch] - my_median
    return L4_shifted
