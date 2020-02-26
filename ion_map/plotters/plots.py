import matplotlib.pyplot as plt
from matplotlib.pyplot import cm
import numpy as np
import calculations.common as common


def obs_comb(sat):
    epochs = []
    P4, L4, L4s = [], [], []

    for e in sat.L4_shifted.keys():
        epochs.append(common.datetime_to_secs_of_day(e))
        P4.append(sat.P4[e])
        L4.append(sat.L4[e])
        L4s.append(sat.L4_shifted[e])

    plt.plot(epochs, P4, "r.", label="P4")
    plt.legend(loc="upper right")
    plt.show()
    plt.plot(epochs, L4, "b.", label="L4")
    plt.legend(loc="upper right")
    plt.show()
    plt.plot(epochs, L4s, "g.", label="L4_s")
    plt.legend(loc="upper right")
    plt.show()


def obs_comb_2sat(sat1, sat2):
    fig, (ax1, ax2) = plt.subplots(2, 1)
    fig.subplots_adjust(hspace=0.5)

    epochs1 = []
    P41, L41, L4s1 = [], [], []

    for e in sat1.L4_shifted.keys():
        epochs1.append(common.datetime_to_secs_of_day(e))
        P41.append(sat1.P4[e])
        L41.append(sat1.L4[e])
        L4s1.append(sat1.L4_shifted[e])

    epochs2 = []
    P42, L42, L4s2 = [], [], []

    for e in sat2.L4_shifted.keys():
        epochs2.append(common.datetime_to_secs_of_day(e))
        P42.append(sat2.P4[e])
        L42.append(sat2.L4[e])
        L4s2.append(sat2.L4_shifted[e])

    ax1.plot(epochs1, P41, "r.", label="P4")
    ax1.plot(epochs1, L41, "b.", label="L4")
    ax1.plot(epochs1, L4s1, "g.", label="L4_s")
    ax1.set_title(f"{sat1.prn}")
    ax1.set_ylabel("[m]")
    ax1.set_xlabel("[s]")

    ax2.plot(epochs2, P42, "r.", label="P4")
    ax2.plot(epochs2, L42, "b.", label="L4")
    ax2.plot(epochs2, L4s2, "g.", label="L4_s")
    ax2.set_title(f"{sat2.prn}")
    ax2.set_ylabel("[m]")
    ax2.set_xlabel("[s]")
    plt.legend(loc="upper center", bbox_to_anchor=(0.5, -0.2), fancybox=True, ncol=3)

    plt.show()


def vtec(site):
    sats = [sat for sat in sorted(site.satellites.keys()) if sat[0] == "G"]
    color = iter(cm.rainbow(np.linspace(0, 1, len(sats))))
    for i in range(len(sats)):
        sat = site.satellites[sats[i]]
        c = next(color)
        x, y = [], []
        epochs = sorted(sat.VTEC.keys())
        vtec = [sat.VTEC[e] for e in epochs]
        plt.plot(epochs, vtec, ".", c=c, label=sats[i])

    plt.title(site.name + " VTEC 2015.03.17")
    plt.ylabel("[TECU]")
    plt.xlabel("time")
    plt.legend(loc="center left", bbox_to_anchor=(1, 0.5))
    plt.show()
