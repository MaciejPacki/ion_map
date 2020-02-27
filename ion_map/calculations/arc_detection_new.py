from constants import wl_lambda, TEC_const
import numpy as np
import calculations.common as common


def MWWL_detector(L4, MWWL):
    epochs = sorted(L4)
    cs_terms = []
    cs = []
    for i in range(1, len(epochs)):
        cs_term = MWWL[epochs[i - 1]] / wl_lambda - MWWL[epochs[i]] / wl_lambda
        if abs(cs_term) > 4 * np.std(cs_terms):
            print(epochs[i], "MWWL", common.datetime_to_secs_of_day(epochs[i]))
            cs.append(epochs[i])
        cs_terms.append(cs_term)
    return cs


def TECR_detector(L4):
    epochs = sorted(L4)
    cs = []
    tecr = [0]
    tecr_dot = [0, 0]
    tec_res = []

    init_tecr1 = (L4[epochs[1]] * TEC_const - L4[epochs[0]] * TEC_const) / (
        epochs[1] - epochs[0]
    ).seconds
    init_tecr2 = (L4[epochs[2]] * TEC_const - L4[epochs[1]] * TEC_const) / (
        epochs[2] - epochs[1]
    ).seconds
    tecr.append(init_tecr1)
    tecr.append(init_tecr2)
    init_tecr_dot = (tecr[2] - tecr[1]) / (epochs[2] - epochs[1]).seconds
    tecr_dot.append(init_tecr_dot)
    init_pred_tecr = tecr[1] + tecr_dot[1] * (epochs[2] - epochs[1]).seconds
    tec_res.append(init_tecr2 - init_pred_tecr)
    for i in range(3, len(epochs)):
        delta_t = (epochs[i] - epochs[i - 1]).seconds
        pred_tecr = tecr[i - 1] + tecr_dot[i - 1] * delta_t
        obs_tecr = (L4[epochs[i]] * TEC_const - L4[epochs[i - 1]] * TEC_const) / delta_t
        tecr.append(obs_tecr)
        c_tecr_dot = (tecr[i] - tecr[i - 1]) / delta_t
        tecr_dot.append(c_tecr_dot)
        c_tecr_res = obs_tecr - pred_tecr
        if abs(c_tecr_res) > 4 * np.std(tec_res):
            cs.append(epochs[i])
            print(epochs[i], "TECR", common.datetime_to_secs_of_day(epochs[i]))
        tec_res.append(c_tecr_res)

    return cs


def arc_detector(L4, MWWL):
    MWWL_cs = MWWL_detector(L4, MWWL)
    TECR_cs = TECR_detector(L4)
    cs = [common.datetime_to_secs_of_day(i) for i in (MWWL_cs + TECR_cs)]
    return (
        [common.datetime_to_secs_of_day(i) for i in MWWL_cs],
        [common.datetime_to_secs_of_day(i) for i in TECR_cs],
    )
