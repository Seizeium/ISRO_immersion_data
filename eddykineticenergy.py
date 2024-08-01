import netCDF4 as nc
import numpy as np
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cfeature
from matplotlib.colors import BoundaryNorm, LinearSegmentedColormap

# Open the netCDF file
file_path = '/mnt/c/Users/ASUS/Desktop/terraspatial/ISRO_immersion_data/Eddykinetic20230710.nc'  # Replace with your actual file path
nc_file = nc.Dataset(file_path, 'r')

# Access the dimensions
lon_dim = nc_file.dimensions['LON82_361']
lat_dim = nc_file.dimensions['LAT181_420']
print(f"Longitude dimension: {lon_dim.size}")
print(f"Latitude dimension: {lat_dim.size}")

# Access the variables
lon = nc_file.variables['LON82_361'][:]
lat = nc_file.variables['LAT181_420'][:]
eke = nc_file.variables['EKE'][:]

# Provided data (accessed from the netCDF file)
longitude = lon
latitude = lat
eke_data = eke[0, :, :]  # Assuming time is the first dimension

# Mask invalid data and clip to the max known value
eke_data = np.ma.masked_invalid(eke_data)
eke_data = np.ma.masked_greater(eke_data, 2200)  # Clip to 2200

# Define the color scale based on the provided bounds
bounds = [0, 100, 200, 300, 400, 500, 600, 700, 800, 900, 1000, 1200, 1400, 1500, 1600, 1700, 1800, 2000, 2200]

# Create a custom rainbow colormap
colors = [
    "#000080", "#380097", "#7000AF", "#A700C7", "#8600D9", "#4E00E9", "#1600F9", "#0017FF",
    "#003EFF", "#0065FF", "#008DFF", "#00B4FF", "#00DBFF", "#05FAFA", "#22FBDD", "#3FFCC0",
    "#5BFCA4", "#78FD87", "#95FD6A", "#B2FE4D", "#CEFF31", "#EBFF14", "#F8ED07", "#F9CB06",
    "#FAA905", "#FC8703", "#FD6602", "#FE4401", "#FF2200", "#F90700", "#D90400", "#B90200",
    "#990000"
]

# Create a LinearSegmentedColormap from the list of colors
cmap = LinearSegmentedColormap.from_list("custom_cmap", colors, N=len(bounds) - 1)

# Create a BoundaryNorm with the defined bounds
norm = BoundaryNorm(boundaries=bounds, ncolors=cmap.N)

# Creating the plot
fig = plt.figure(figsize=(12, 8))
ax = plt.axes(projection=ccrs.PlateCarree())

# Add coastlines and gridlines
ax.coastlines()
ax.add_feature(cfeature.LAND, zorder=0, edgecolor='black')
ax.gridlines(draw_labels=True)

# Create a contourf plot
eke_plot = ax.contourf(longitude, latitude, eke_data, levels=bounds, transform=ccrs.PlateCarree(), cmap=cmap, norm=norm)

# Adding a colorbar
cbar = plt.colorbar(eke_plot, orientation='vertical', pad=0.05)
cbar.set_label('Eddy Kinetic Energy')

# Title and labels
plt.title('Eddy Kinetic Energy Heatmap')
plt.xlabel('Longitude')
plt.ylabel('Latitude')

plt.show()
