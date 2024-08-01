import numpy as np
import matplotlib.pyplot as plt
from netCDF4 import Dataset
from matplotlib.colors import BoundaryNorm, LinearSegmentedColormap

# Load the dataset
dataset_path = 'ISRO_immersion_data\\oceancurrents.nc'
dataset = Dataset(dataset_path)

# Read latitude, longitude, and Ekman currents data
latitudes = dataset.variables['latitude'][:]
longitudes = dataset.variables['longitude'][:]
u_ekm = dataset.variables['u_ekm'][:]
v_ekm = dataset.variables['v_ekm'][:]

# Mask the _FillValue for proper visualization
u_ekm = np.ma.masked_equal(u_ekm, -9999)
v_ekm = np.ma.masked_equal(v_ekm, -9999)

# Calculate Eddy Kinetic Energy (EKE)
eke = 0.5 * (u_ekm**2 + v_ekm**2)

# Adjust longitudes to be in the range specified by metadata
longitudes_adjusted = (longitudes + 180) % 360 - 180

# Define the color scale based on the provided bounds
bounds = [0, 100, 200, 300, 400, 500, 600, 700, 800, 900, 1000, 1200, 1400, 1500, 1600, 1700, 1800, 2000, 2200]

# Create a custom rainbow colormap
colors = [
    "#000080", "#380097", "#7000AF", "#A700C7", "#8600D9", "#4E00E9" ,"#1600F9" ,"#0017FF" ,"#003EFF", "#0065FF", "#008DFF", "#00B4FF" , "#00DBFF", "#05FAFA", "#22FBDD" , "#3FFCC0", "#5BFCA4" ,"#78FD87" ,"#95FD6A" , "#B2FE4D" , "#CEFF31", "#EBFF14" , "#F8ED07" , "#F9CB06" ,"#FAA905" ,"#FC8703" ,"#FD6602" , "#FE4401" , "#FF2200" , "#F90700" , "#D90400" , "#B90200" , "#990000"]

# To match the number of bounds, create an interpolation of these colors
n_bins = len(bounds) - 1  # Number of bins is one less than the number of bounds
cmap_name = 'rainbow_gradient'
cmap = LinearSegmentedColormap.from_list(cmap_name, colors, N=n_bins)
norm = BoundaryNorm(bounds, cmap.N)

# Slice the EKE array to match the specified geographic bounds
lat_min_idx = np.abs(latitudes - -30).argmin()
lat_max_idx = np.abs(latitudes - 30).argmin()
lon_min_idx = np.abs(longitudes - 40).argmin()
lon_max_idx = np.abs(longitudes - 110).argmin()

lat_range = latitudes[lat_min_idx:lat_max_idx+1]
lon_range = longitudes[lon_min_idx:lon_max_idx+1]
eke_range = eke[lon_min_idx:lon_max_idx+1, lat_min_idx:lat_max_idx+1]

# Create the contour plot
plt.figure(figsize=(12, 6), dpi=150)  # Increase dpi for high resolution

# Use plt.contourf() for filled contours
contour = plt.contourf(lon_range, lat_range, eke_range.T, levels=bounds, cmap=cmap, norm=norm)

# Add a color bar
plt.colorbar(contour, label='Eddy Kinetic Energy (EKE) [cm²/s²]', boundaries=bounds, ticks=bounds)

# Add title and labels
plt.title('Eddy Kinetic Energy (EKE) Contour Plot\n'
          'Tropical Indian Ocean (40°E to 110°E, 30°S to 30°N)')
plt.xlabel('Longitude')
plt.ylabel('Latitude')

# Show the plot
plt.show()

# Close the dataset
dataset.close()
