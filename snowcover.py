import rasterio
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import cartopy.io.shapereader as shpreader
from rasterio.plot import show

# Paths to the files
rst_file_path = r'C:\Users\ASUS\Desktop\terraspatial\ISRO_immersion_data\aw_scf_jan01to152024_03min_v01.rst'
shapefile_path = r'C:\Users\ASUS\Desktop\terraspatial\ISRO_immersion_data\India3A_State_Boundary_2021_.shp'

# Open and read the RST file
with rasterio.open(rst_file_path) as src:
    data = src.read(1)  # Read the first band

    # Get data bounds
    bounds = src.bounds

    # Set up the plot
    fig, ax = plt.subplots(figsize=(14, 12), subplot_kw={'projection': ccrs.PlateCarree()})
    
    # Use data bounds for extent
    ax.set_extent([bounds.left, bounds.right, bounds.bottom, bounds.top], crs=ccrs.PlateCarree())

    # Plot the snow cover data
    show(data, transform=src.transform, ax=ax, cmap='viridis', interpolation='none')

    # Add features to the map
    ax.add_feature(cfeature.LAND, edgecolor='black')
    ax.add_feature(cfeature.COASTLINE)
    ax.add_feature(cfeature.LAKES, edgecolor='black')
    ax.add_feature(cfeature.RIVERS)

    # Add custom border from shapefile
    reader = shpreader.Reader(shapefile_path)
    for shape in reader.geometries():
        ax.add_geometries([shape], crs=ccrs.PlateCarree(), edgecolor='black', facecolor='none', linewidth=2)

    # Add a colorbar
    cbar = plt.colorbar(ax.images[0], ax=ax, orientation='horizontal', pad=0.05, aspect=50)
    cbar.set_label('Snow Cover Fraction (%)')

    # Add title
    plt.title('Snow Cover Over South Asia')

    # Show the plot
    plt.show()
