
import numpy as np
import math
import matplotlib.pyplot as plt
from scipy import interpolate
 
from constants import TEC_const, c


#50.0-180.0 180.0   5.0 450.0                            LAT/LON1/LON2/DLON/H
s1=   "181  156  138  126  120  115  109  102   96   94   97  107  121  138  153  164\
  170  169  162  153  142  132  124  120  118  114  107   97   87   79   79   89\
  109  135  164  193  222  251  280  311  343  372  399  423  446  466  484  496\
  499  493  482  470  462  456  451  444  434  422  412  407  404  402  397  385\
  367  346  325  306  286  265  239  210  181    ".split(' ')
                              
#    52.5-180.0 180.0   5.0 450.0                            LAT/LON1/LON2/DLON/H
s2 = "  151  129  114  107  105  105  107  107  109  112  118  128  141  154  166  172\
  174  171  164  155  146  138  134  132  130  127  121  112  102   94   93  100\
  115  137  161  187  213  240  268  297  326  355  381  404  425  445  461  471\
  475  472  465  456  449  443  437  430  421  412  405  400  396  390  380  363\
  340  316  292  270  250  228  203  177  151    ".split(' ')
s1 = [x for x in s1 if x != '']
s2 = [x for x in s2 if x != '']
#2015/03/17 08:00:00       G03           50.459964           25.532794              6.5019
#JOZ2 11.858 
# 2015/03/17 08:00:00       G23           51.282555           18.014147            -26.1164
#WROC 19.845     
aim = 19.845e-9
obs = -26.1164
my_lon = 18.014147    
my_lat = 51.282555

lat = [50, 50, 52.5, 52.5]
lon = [15, 20, 15, 20]
t1 = float(s1[36+3]) / 10
t2 = float(s1[36+4]) / 10
t3 = float(s2[36+3]) / 10
t4 = float(s2[36+4]) / 10

tec = [t1, t2, t3, t4]
print(tec)
my_inter = interpolate.interp2d(lon, lat, tec)
my_tec = my_inter(my_lon,my_lat)
s = (my_tec - obs) / TEC_const

print(f"OBSERVED: {obs} INTER {my_tec}")
print("RES: {:.2e}".format(float(s)/c))
print("AIM: {:.2e}".format(aim))
lat.append(my_lat)
lon.append(my_lon)
tec.append(my_tec)
color_map = plt.cm.get_cmap("jet")
# plt.scatter(lon, lat, c=tec, cmap=color_map)
# plt.colorbar()
# plt.show()
# 
# 
print('\n\n')
