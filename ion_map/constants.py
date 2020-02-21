import datetime

c = 299792458 # prędkość światła w próźni [m/s]
r_earth = 6378.137 # Promien Ziemi [km]

GM = 3986005e8 # paramter WGS84  grawitacyjny ziemi [m^3/s^2]
OMEGA_E = 7.2921151467e-5 # parametr WGS84  prędkość obrotu Ziemi [rad/s]

L1_freq = 1575.42e6 # Częstotliwość L1 [Hz]
L2_freq = 1227.60e6 # Częstotliwość L2 [Hz]
L1_lambda = c / L1_freq # Dł. fali L1 [m]
L2_lambda = c / L2_freq # Dł. fali L2 [m]
wl_lambda = c / (L1_freq + L2_freq) # Dł. fali wide lane [m]

TEC_const = 1 /40.3e16 * (L1_freq**2 * L2_freq**2) / (L1_freq**2 - L2_freq**2)


dcb_rec = 20.039e-9 * c # ns, bor1
# dcb_rec = 4.468e-9 * c # ns, bogi
# dcb_rec = 0

secs_in_week = 604800 # Sekundy w tygodniu
init_gps_epoch = datetime.datetime(1980, 1, 6, 0, 0, 0)

e2 =  6.69437999014e-3 # Kwadrat pierwszej ekscentryczności 
a = 6378137 # Półoś duża WGS84 [m]