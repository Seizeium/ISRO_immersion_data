import netCDF4 as nc
import numpy as np
import rasterio
from rasterio.transform import from_origin
import matplotlib.pyplot as plt

# Load the netCDF file
dataset = nc.Dataset(r"D:\Athar\Terra_spatial\ISRO_immersion_data\nices_ssm2_20240726\LPRM-AMSR2_01T_L3_SM_D20240711.nc")

# Extract the data
lat = dataset.variables['latitude'][:]
lon = dataset.variables['longitude'][:]
soil_moisture = dataset.variables['soil_moisture'][:]
# print(soil_moisture[60][70])

# Replace fill values with NaN
soil_moisture = np.where(soil_moisture == -9999.0, np.nan, soil_moisture)

# Rotate the soil moisture data 90 degrees counterclockwise
soil_moisture = np.rot90(soil_moisture, k=1)  # Rotate 90 degrees counterclockwise

# Define transform for rasterio
transform = from_origin(lon.min(), lat.max(), lon[1] - lon[0], lat[1] - lat[0])

# Create a new raster
with rasterio.open(
    'soil_moisture.tif',
    'w',
    driver='GTiff',
    height=soil_moisture.shape[0],
    width=soil_moisture.shape[1],
    count=1,
    dtype=soil_moisture.dtype,
    crs='+proj=latlong',
    transform=transform,
) as dst:
    dst.write(soil_moisture, 1)

# Plot the data with a blue gradient
fig, ax = plt.subplots(figsize=(8, 10))
cmap = plt.cm.Blues
cmap.set_bad('white', 1.0)  # Set the background color for NaN values
cax = ax.imshow(soil_moisture, cmap=cmap, extent=(lon.min(), lon.max(), lat.min(), lat.max()), vmin=0, vmax=0.5)
cbar = fig.colorbar(cax, orientation='horizontal', pad=0.05)
cbar.set_label('Surface Soil Moisture (m^3/m^3)')
plt.xlabel('Longitude')
plt.ylabel('Latitude')
plt.title('Surface Soil Moisture')
plt.show()
