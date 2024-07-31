import matplotlib.pyplot as plt
import numpy as np
import rasterio
from rasterio.plot import show
from mpl_toolkits.basemap import Basemap
from matplotlib.colors import Normalize
from matplotlib.cm import get_cmap

# Create figure with high DPI
fig = plt.figure(figsize=(12, 10), dpi=150)  # Adjust dpi as needed
ax = fig.add_subplot(111)

# Set up Basemap for India
m = Basemap(projection='merc',
            llcrnrlat=5, urcrnrlat=37,
            llcrnrlon=65, urcrnrlon=95,
            resolution='i', ax=ax)

m.drawcoastlines()
m.drawcountries()
m.drawmapboundary(fill_color='lightgrey')
m.fillcontinents(color='lightgrey', lake_color='lightblue')
m.drawparallels(np.arange(0., 90., 10.), labels=[1,0,0,0])
m.drawmeridians(np.arange(0., 360., 10.), labels=[0,0,0,1])

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
    cmap = get_cmap('Blues')
    norm = Normalize(vmin=np.min(data), vmax=np.max(data))
    im = ax.pcolormesh(x, y, data, cmap=cmap, norm=norm, alpha=0.6)

# Optionally, add city/village locations
# ...

# Add plot settings
plt.xlabel('Longitude')
plt.ylabel('Latitude')
plt.title('Surface Soil Moisture with Map of India Background')
plt.show()

# import matplotlib.pyplot as plt
# import numpy as np
# import rasterio
# import geopandas as gpd
# from matplotlib.colors import Normalize
# from matplotlib.cm import get_cmap
# import geodatasets

# # Create figure with high DPI
# fig, ax = plt.subplots(figsize=(12, 10), dpi=150)  # Adjust dpi as needed

# # Load the India shapefile from geodatasets
# # Use 'naturalearth_countries' for country boundaries
# countries = gpd.read_file(geodatasets.get_path('naturalearth_countries'))
# india = countries[countries.name == 'India']

# # Plot the base map of India
# india.plot(ax=ax, color='lightgrey', edgecolor='black')

# # Set up axis limits
# ax.set_xlim(65, 95)  # Longitude range
# ax.set_ylim(5, 37)   # Latitude range

# # Add soil moisture raster
# with rasterio.open('soil_moisture.tif') as src:
#     data = src.read(1)
#     transform = src.transform

#     # Create a grid of coordinates in the raster's coordinate system
#     lon, lat = np.meshgrid(
#         np.arange(src.bounds.left, src.bounds.right, (src.bounds.right - src.bounds.left) / src.width),
#         np.arange(src.bounds.bottom, src.bounds.top, (src.bounds.top - src.bounds.bottom) / src.height)
#     )

#     # Convert raster coordinates to map coordinates
#     x, y = transform * (lon.flatten(), lat.flatten())
#     x = x.reshape(lon.shape)
#     y = y.reshape(lat.shape)

#     # Plot raster data
#     cmap = get_cmap('Blues')
#     norm = Normalize(vmin=np.min(data), vmax=np.max(data))
#     im = ax.pcolormesh(x, y, data, cmap=cmap, norm=norm, alpha=0.6, shading='auto')

# # Optionally, add city/village locations
# # ...

# # Add plot settings
# plt.xlabel('Longitude')
# plt.ylabel('Latitude')
# plt.title('Surface Soil Moisture with Map of India Background')
# plt.show()
# import geodatasets

