import numpy as np
import matplotlib.pyplot as plt

# Load the .dat file
file_path = 'ISRO_immersion_data\c.dat'
data = np.loadtxt(file_path)

# Extract the relevant columns
latitudes = data[:, 3]
longitudes = data[:, 4]
tchp_values = data[:, 5]

# Filter out invalid TCHP values
valid_mask = np.isfinite(tchp_values)
latitudes = latitudes[valid_mask]
longitudes = longitudes[valid_mask]
tchp_values = tchp_values[valid_mask]

# Create a grid for latitudes and longitudes
lat_unique = np.unique(latitudes)
lon_unique = np.unique(longitudes)
lat_grid, lon_grid = np.meshgrid(lat_unique, lon_unique, indexing='ij')

# Initialize a grid with NaNs
tchp_grid = np.full(lat_grid.shape, np.nan)

# Populate the grid with TCHP values
for lat, lon, tchp in zip(latitudes, longitudes, tchp_values):
    lat_idx = np.where(lat_unique == lat)[0][0]
    lon_idx = np.where(lon_unique == lon)[0][0]
    tchp_grid[lat_idx, lon_idx] = tchp

# Replace NaN values with 0
tchp_grid = np.nan_to_num(tchp_grid, nan=0.0)

# Plotting
plt.figure(figsize=(10, 8))
contour = plt.contourf(lon_grid, lat_grid, tchp_grid, levels=[0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100, np.inf], cmap='jet')

# Adding color bar
cbar = plt.colorbar(contour, ticks=[0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100])
cbar.set_label('TCHP (kJ/cm^2)')

# Adding labels and title
plt.title('TCHP (kJ/cm^2) - 2024-02-14')
plt.xlabel('Longitudes')
plt.ylabel('Latitudes')

# Set x and y axis limits
plt.xlim(40, 120)
plt.ylim(-30, 30)

# Show the plot
plt.show()
