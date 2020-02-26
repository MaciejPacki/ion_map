import datetime
import os
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import matplotlib.pyplot as plt


def get_vtec(data_file):
    global lat, lon, VTEC, beg_date, end_date

    with open(data_file, "r") as file:

        lines = file.readlines()
        for line in lines[1:]:
            c_line = line.split()

            date_str = c_line[0] + " " + c_line[1]
            date = datetime.datetime.strptime(date_str, "%Y/%m/%d %H:%M:%S")
            if date > end_date:
                break
            else:
                lat.append(float(c_line[-3]))
                lon.append(float(c_line[-2]))
                VTEC.append(float(c_line[-1]))


def absoluteFilePaths(directory):
    for dirpath, _, filenames in os.walk(directory):
        for f in filenames:
            yield os.path.abspath(os.path.join(dirpath, f))


files = absoluteFilePaths(r"..\TEST_OUT")


for file in files:
    beg_date = datetime.datetime(2015, 3, 17, 8, 0)
    end_date = beg_date + datetime.timedelta(minutes=15)
    lat = []
    lon = []
    VTEC = []

    get_vtec(file)

    proj = ccrs.EuroPP()
    color_map = plt.cm.get_cmap("jet")
    ax = plt.axes(projection=proj)
    country_boundary = cfeature.NaturalEarthFeature(
        category="cultural",
        name="admin_0_boundary_lines_land",
        scale="50m",
        facecolor="none",
    )
    coast_line = cfeature.NaturalEarthFeature(
        category="physical", name="coastline", scale="50m", facecolor="none"
    )
    ax.add_feature(coast_line, edgecolor="black")
    ax.add_feature(country_boundary, edgecolor="gray")
    ax.gridlines()
    m = ax.scatter(
        lon, lat, c=VTEC, marker=".", transform=ccrs.PlateCarree(), cmap=color_map
    )

    ax.set_global()
    plt.colorbar(m)
    plt.title(f"{file} VTEC [TECU] 17.03.2015")
    plt.show()
    plt.savefig("test_map")
