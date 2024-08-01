import numpy as np
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cfeature
from netCDF4 import Dataset

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

# Adjust longitudes to be in the range -180 to 180 degrees
longitudes_adjusted = (longitudes + 180) % 360 - 180

# Subsample the data for faster plotting (e.g., every 20th point)
subsample = 11
lat_sub = latitudes[::subsample]
lon_sub = longitudes_adjusted[::subsample]
u_ekm_sub = u_ekm[::subsample, ::subsample].T  # Transpose for plotting
v_ekm_sub = v_ekm[::subsample, ::subsample].T  # Transpose for plotting

# Create a meshgrid for the subsampled latitude and longitude
lon_mesh, lat_mesh = np.meshgrid(lon_sub, lat_sub)

# Normalize wind vectors for uniform arrow size
magnitude = np.sqrt(u_ekm_sub**2 + v_ekm_sub**2)
u_ekm_norm = u_ekm_sub / magnitude
v_ekm_norm = v_ekm_sub / magnitude

# Create the plot and projection
fig = plt.figure(figsize=(15, 10))
ax = plt.axes(projection=ccrs.PlateCarree(central_longitude=0))

ax.set_extent([-180, 180, -90, 90], crs=ccrs.PlateCarree())
ax.coastlines()
ax.add_feature(cfeature.LAND, zorder=0)

# Use a colormap to represent the wind speed
magnitude = np.sqrt(u_ekm_sub**2 + v_ekm_sub**2)
norm = plt.Normalize(0, 30)
cmap = plt.cm.jet

# Create the quiver plot with uniform arrow size and color coding based on wind speed
q = ax.quiver(lon_mesh, lat_mesh, u_ekm_norm, v_ekm_norm, magnitude, 
              transform=ccrs.PlateCarree(), scale=170, cmap=cmap, norm=norm, 
              headlength=4, headaxislength=4, headwidth=3)

# Add a color bar
cbar = plt.colorbar(q, ax=ax, orientation='vertical', shrink=0.75)
cbar.set_label('Currents Speed (cm/s)')
cbar.set_ticks([0, 3, 6, 9, 12, 15, 18, 21, 24, 27, 30])
cbar.set_ticklabels([0, 3, 6, 9, 12, 15, 18, 21, 24, 27, 30])

# Add additional map features
ax.gridlines(draw_labels=True)
ax.set_title('Global Ocean Ekman Currents with Speed Gradient')

# Show the plot
plt.show()

# Close the dataset
dataset.close()
