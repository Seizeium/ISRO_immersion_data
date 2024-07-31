import numpy as np
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cfeature
from netCDF4 import Dataset
from cartopy.util import add_cyclic_point

# Load the dataset
dataset_path = '/mnt/c/Users/ASUS/Downloads/NICES_EOS06_SCTL4WW_20240305/E06SCTL4WW_20240305_01_12km_v1.0.2.nc'
dataset = Dataset(dataset_path)

# Extract the necessary data
latitude = dataset.variables['latitude'][:]
longitude = dataset.variables['longitude'][:]
WS = dataset.variables['WS'][0, :, :]
WD = dataset.variables['WD'][0, :, :]

# Convert wind direction and speed to U and V components
U = -WS * np.sin(np.radians(WD))
V = -WS * np.cos(np.radians(WD))

# Subsample the data for faster plotting (e.g., every 20th point)
subsample = 20
lat_sub = latitude[::subsample]
lon_sub = longitude[::subsample]
U_sub = U[::subsample, ::subsample].T  # Transpose U_sub
V_sub = V[::subsample, ::subsample].T  # Transpose V_sub
WS_sub = WS[::subsample, ::subsample].T  # Transpose WS_sub

# Create a meshgrid for the subsampled latitude and longitude
lon_mesh, lat_mesh = np.meshgrid(lon_sub, lat_sub)

# Normalize wind vectors for uniform arrow size
magnitude = np.sqrt(U_sub**2 + V_sub**2)
U_norm = U_sub / magnitude
V_norm = V_sub / magnitude

# Create the plot and projection
fig = plt.figure(figsize=(15, 10))
ax = plt.axes(projection=ccrs.PlateCarree(central_longitude=180))

ax.set_extent([0, 360, -90, 90], crs=ccrs.PlateCarree())
ax.coastlines()
ax.add_feature(cfeature.LAND, zorder=0)

# Define a function to mask land areas
def mask_land(lon, lat):
    """
    Create a mask for land using cartopy's land feature.
    """
    land = cfeature.LAND
    land_polygons = [polygon for polygon in land.geometries()]
    
    mask = np.zeros(lon.shape, dtype=bool)
    
    for polygon in land_polygons:
        for coord in polygon.exterior.coords:
            mask |= (np.abs(lon - coord[0]) < 1) & (np.abs(lat - coord[1]) < 1)
    
    return mask

# Apply land mask to U, V and WS components
land_mask = mask_land(lon_mesh, lat_mesh)
U_sub[land_mask] = np.nan
V_sub[land_mask] = np.nan
WS_sub[land_mask] = np.nan

# Use a colormap to represent the wind speed
norm = plt.Normalize(0, 20)
cmap = plt.cm.jet

# Create the quiver plot with uniform arrow size and color coding based on wind speed
q = ax.quiver(lon_mesh, lat_mesh, U_norm, V_norm, WS_sub, 
              transform=ccrs.PlateCarree(), scale=150, cmap=cmap, norm=norm, 
              headlength=4, headaxislength=4, headwidth=3)

# Add a color bar
cbar = plt.colorbar(q, ax=ax, orientation='vertical', shrink=0.75)
cbar.set_label('Wind Speed (m/s)')
cbar.set_ticks([0, 4, 8, 12, 16, 20])
cbar.set_ticklabels([0, 4, 8, 12, 16, 20])

# Add additional map features
ax.gridlines(draw_labels=True)
ax.set_title('Global Oceans Wind Velocity with Speed Gradient')

# Show the plot
plt.show()

# Close the dataset
dataset.close()