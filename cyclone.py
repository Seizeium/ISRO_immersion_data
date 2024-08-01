import numpy as np
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cfeature
from scipy.interpolate import griddata
from matplotlib.colors import ListedColormap, BoundaryNorm

# Load the data
file_path = '/mnt/c/Users/ASUS/Desktop/terraspatial/ISRO_immersion_data/c.dat'
data = np.loadtxt(file_path)

# Extract latitude, longitude, and TCHP values
lats = data[:, 3]
lons = data[:, 4]
tchp = data[:, 5]

# Remove missing values indicated by -999.000
valid_mask = tchp != -999.000
lats = lats[valid_mask]
lons = lons[valid_mask]
tchp = tchp[valid_mask]

# Create a grid of latitude and longitude values
lat_grid, lon_grid = np.meshgrid(np.unique(lats), np.unique(lons))

# Interpolate TCHP values onto the grid
tchp_grid = griddata((lats, lons), tchp, (lat_grid, lon_grid), method='linear')

# Define custom levels and colormap
tchp_levels = [0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100, np.nanmax(tchp_grid)]

# Define custom colors for each level range
colors = [
    '#0000FF', '#0064FF', '#00BFFF',      # 0-20
    '#05FF50', '#05DC00', '#7CFC00',   # 30-50
    '#FFFF00', '#FFD700',              # 60-70
    '#FFA500', '#FA7800',               # 80-90
    '#FF0A64', '#E60000', 'RED'                       # 100, >100
]

cmap = ListedColormap(colors)
norm = BoundaryNorm(tchp_levels, cmap.N)

# Create the plot
fig, ax = plt.subplots(subplot_kw={'projection': ccrs.PlateCarree()})
ax.set_extent([30, 120, -30, 30], crs=ccrs.PlateCarree())

# Create a contour plot for TCHP
contour = ax.contourf(lon_grid, lat_grid, tchp_grid, levels=tchp_levels, cmap=cmap, norm=norm, transform=ccrs.PlateCarree(), zorder=1)

# Add features to the map (with a higher zorder to ensure they are on top)
ax.add_feature(cfeature.LAND, edgecolor='black', zorder=2)
ax.add_feature(cfeature.COASTLINE, zorder=3)

# Add colorbar
cbar = plt.colorbar(contour, ax=ax, orientation='horizontal', pad=0.05, aspect=50)
cbar.set_label('TCHP (kJ/cm²)')

# Add title
plt.title('TCHP (kJ/cm²) - 2024-02-14')

# Save and show the plot
# plt.savefig('/mnt/data/tchp_visualization.png')
plt.show()
