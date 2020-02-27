import os


import readers.rnx_obs as rnx_obs
import readers.rnx_nav as rnx_nav
import readers.dcb as dcb
import write_raport

obs_files = [
    "C:\\users\\macie\\desktop\\EPN_DATA\\" + obs_file
    for obs_file in os.listdir(r"C:\users\macie\Desktop\EPN_DATA")
]
# obs_files = [r"C:\users\macie\Desktop\ion_map\tests\test_files\bor10760.15O"]
nav_file = r"C:\users\macie\Desktop\ion_map\tests\test_files\brdm0760.15p"
dcb_P1P2_file = r"C:\users\macie\desktop\ion_map\tests\test_files\P1P21503.DCB"
dcb_P1C1_file = r"C:\users\macie\desktop\ion_map\tests\test_files\P1C11503.DCB"
ionosphere_h = 450
elev_mask = 30


nav = rnx_nav.read(nav_file)
sat_dcb = dcb.read(dcb_P1P2_file, dcb_P1C1_file)


for obs_file in obs_files:
    site = rnx_obs.read(obs_file)
    site.process_data(nav, sat_dcb, ionosphere_h, elev_mask)
    write_raport.hour(site)
