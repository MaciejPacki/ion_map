import os
import datetime


def hour(site):
    data = site.get_hour_data()
    try:
        os.mkdir("TEST_OUT")
    except FileExistsError:
        pass

    site_path = "TEST_OUT//{}".format(site.name + "_H")
    for hour, c_data in data.items():
        if hour == 8:
            out_file = site_path + str(hour).zfill(2)
            write_data = "#N{:>19}{:>10}{:>20}{:>20}{:>20}\n".format(
                "EPOCH", "PRN", "IPP lat [deg]", "IPP lon [deg]", "VTEC"
            )
            for line in c_data:
                epoch = line[0].strftime("%Y/%m/%d %H:%M:%S")
                write_data += "{:>20}{:>10}{:>-20.6f}{:>-20.6f}{:>-20.4f}\n".format(
                    epoch, line[1], line[2], line[3], line[4]
                )

            with open(out_file, "w") as file:
                file.write(write_data)
