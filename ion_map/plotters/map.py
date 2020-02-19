import datetime
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import matplotlib.pyplot as plt

def plot(data):
    d = "16:00:00"
    lat = []
    lon = []
    P4 = []
    with open(data, "r") as file:
        lines = file.readlines()
        for line in lines[1:]:
            c_line = line.split()
            if c_line[1] == d:
                date_out = c_line[0] + " " + c_line[1]
                lat.append(float(c_line[-3]))
                lon.append(float(c_line[-2]))
                P4.append(float(c_line[-1]))

    proj = ccrs.EuroPP()
    color_map = plt.cm.get_cmap('jet')
    ax = plt.axes(projection=proj)
    country_boundary = cfeature.NaturalEarthFeature(
        category='cultural',
        name='admin_0_boundary_lines_land',
        scale='50m',
        facecolor='none')
    coast_line = cfeature.NaturalEarthFeature(
        category='physical',
        name="coastline",
        scale='50m',
        facecolor='none')
    ax.add_feature(coast_line, edgecolor='black')
    ax.add_feature(country_boundary, edgecolor='gray')
    ax.gridlines()
    m = ax.scatter(lon, lat, c=P4, transform=ccrs.PlateCarree(), cmap = color_map)

    ax.set_global()
    plt.colorbar(m)
    plt.title(f"VTEC MAP {date_out}")
    plt.savefig("test_map")
