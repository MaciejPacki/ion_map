import matplotlib.pyplot as plt
from matplotlib.pyplot import cm
import numpy as np
import calculations.common as common


def L4(sat):
    epochs = []
    L4 = []
    cs_glab = [2490.00,
    31650.00,
31890.00,
31890.00,
53550.00,
]
    cs_mwwl = [52560, 55470, 59130, 59160, 59250, 59280, 59460, 59490]
    cs_tecr = [34710, 49080, 49470]
    for e in sat.L4.keys():
        epochs.append(common.datetime_to_secs_of_day(e))
        L4.append(sat.L4[e])

        
    plt.plot(epochs, L4, "b.", label="L4")

    
    # for i in cs_glab[:-1]:
    #     plt.axvline(x=i, color="r")
    # plt.axvline(x=cs_glab[-1], color="r", label="GLAB CS")
    for i in cs_mwwl[:-1]:    
        plt.axvline(x=i, color="g")
    plt.axvline(x=cs_mwwl[-1], color="g", label="MWWL CS")
    # for i in cs_tecr[:-1]:    
    #     plt.axvline(x=i, color="y")
    # plt.axvline(x=cs_tecr[-1], color="y", label="TECR CS")
    
        
    plt.legend(loc="upper right")
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
