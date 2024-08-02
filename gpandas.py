import netCDF4 as nc
import numpy as np
import rasterio
from rasterio.transform import from_origin
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap
import shapefile  # pyshp library for reading shapefiles

# Load the netCDF file
dataset = nc.Dataset(r"C:\Terra_spatial\nices_ssm2_20240726\LPRM-AMSR2_01T_L3_SM_D20240711.nc")

# Extract the data
lat = dataset.variables['latitude'][:]
lon = dataset.variables['longitude'][:]
soil_moisture = dataset.variables['soil_moisture'][:]

# Replace fill values with NaN
soil_moisture = np.where(soil_moisture == -9999.0, np.nan, soil_moisture)

# Rotate the soil moisture data 90 degrees counterclockwise
soil_moisture = np.rot90(soil_moisture, k=1)  # Rotate 90 degrees counterclockwise

# Flip the data vertically
soil_moisture = np.flipud(soil_moisture)

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

# Create the plot
fig, ax = plt.subplots(figsize=(8, 10))

# Set up Basemap for India
m = Basemap(projection='merc',
            llcrnrlat=5, urcrnrlat=37,
            llcrnrlon=65, urcrnrlon=100,
            resolution='i', ax=ax)

m.drawcoastlines()
# m.drawcountries()
m.drawmapboundary(fill_color='lightgrey')
m.fillcontinents(color='lightgrey', lake_color='lightblue')
m.drawparallels(np.arange(0., 90., 10.), labels=[1, 0, 0, 0])
m.drawmeridians(np.arange(0., 360., 10.), labels=[0, 0, 0, 1])

# Add soil moisture raster
with rasterio.open('soil_moisture.tif') as src:
    # Read the raster data
    data = src.read(1)
    transform = src.transform
    
    # Create a new grid of coordinates in the map projection
    lon, lat = np.meshgrid(
        np.arange(src.bounds.left, src.bounds.right, (src.bounds.right - src.bounds.left) / src.width),
        np.arange(src.bounds.bottom, src.bounds.top, (src.bounds.top - src.bounds.bottom) / src.height)
    )
    
    x, y = m(lon, lat)

    # Plot raster data
    cmap = plt.cm.Blues
    cmap.set_bad('white', 1.0)  # Set the background color for NaN values
    cax = ax.pcolormesh(x, y, data, cmap=cmap, vmin=0, vmax=0.5)

# Load and plot the shapefile
sf = shapefile.Reader("C:\Terra_spatial\ISRO_immersion_data\India3A_State_Boundary_2021_.shp")  # Update with the path to your shapefile

# Plot shapefile boundaries
for shape in sf.shapeRecords():
    # Convert shape to map projection
    parts = shape.shape.parts
    points = shape.shape.points
    for i in range(len(parts)):
        start = parts[i]
        end = parts[i + 1] if i + 1 < len(parts) else len(points)
        coords = np.array(points[start:end])
        x, y = m(coords[:, 0], coords[:, 1])
        m.plot(x, y, marker=None, color='black', linewidth=2)

# Add color bar
cbar = fig.colorbar(cax, orientation='horizontal', pad=0.05)
cbar.set_label('Surface Soil Moisture (m^3/m^3)')

# Add labels and title
# plt.xlabel('Longitude')
# plt.ylabel('Latitude')
plt.title('Surface Soil Moisture with Map of India Background')
plt.show()
