import matplotlib.pyplot as plt
import numpy as np
import rasterio
from rasterio.plot import show
import geopandas as gpd

# Load data and prepare the raster as before
# ...

# Load the map of India
world = gpd.read_file(gpd.datasets.get_path('naturalearth_lowres'))
india = world[world.name == 'India']

# Create figure with high DPI
fig = plt.figure(figsize=(12, 10), dpi=150)  # Adjust dpi as needed
ax = fig.add_subplot(111)

india.plot(ax=ax, color='lightgrey')

# Add soil moisture raster
with rasterio.open('soil_moisture.tif') as src:
    show(src, ax=ax, cmap='Blues', interpolation='none', alpha=0.6)

# Optionally, add city/village locations
# ...

# Add plot settings
plt.xlabel('Longitude')
plt.ylabel('Latitude')
plt.title('Surface Soil Moisture with Map of India Background')
plt.show()
