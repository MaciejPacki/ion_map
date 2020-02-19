import process_data
import write_raport
# import plotters.map as map
import datetime
import os





obs_files = ["C:\\users\\macie\\desktop\\EPN_DATA\\" + obs_file for obs_file in os.listdir(r"C:\users\macie\Desktop\EPN_DATA")]
nav_file = r"C:\users\macie\Desktop\ion_map\tests\test_files\brdm0760.15p"
dcb_P1P2_file = r"C:\users\macie\desktop\ion_map\tests\test_files\P1P21503.DCB"
dcb_P1C1_file = r"C:\users\macie\desktop\ion_map\tests\test_files\P1C11503.DCB"

for obs_file in obs_files:
    print(obs_file)
    site = process_data.site(obs_file, nav_file, dcb_P1C1_file, dcb_P1P2_file)
    write_raport.hour(site)

