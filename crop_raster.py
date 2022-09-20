import matplotlib.pyplot as plt
import seaborn as sns
from shapely.geometry import mapping
import rioxarray as rxr
import geopandas as gpd

# set plot scale in seaborn
sns.set(font_scale=1.5)

# Open raster layer        
dem = rxr.open_rasterio("data/hyd_sa_dem_15s.tif", masked=True).squeeze()

fig, ax = plt.subplots(figsize = (10, 5))
im = ax.imshow(dem.squeeze())
ax.set(title='South America DEM')
ax.set_axis_off()
plt.show()

# Open shapefile
# Set filepath
fp = "data/hybas_sa_lev01-12_v1c/hybas_sa_lev02_v1c.shp"
basins = gpd.read_file(fp)
type(basins) # geopandas.geodataframe.GeoDataFrame
basins.plot()
# Check data
print(basins.head(2))
print(basins['geometry'].head())

# Set filepath to output polygon
out_fp = "data/hybas_sa_lev01-12_v1c/SELECTION.shp"
# Select polygon and write to file
selection = basins[0:1]
selection.to_file(out_fp)
fp_subbasin = "data/hybas_sa_lev01-12_v1c/SELECTION.shp"

# Read newly created shapefile
subbasin = gpd.read_file(fp_subbasin)

# Plot subbasin
fig, ax = plt.subplots(figsize=(6, 6))
subbasin.plot(ax=ax)
ax.set_title("Shapefile Crop Extent", fontsize=16)
plt.show()

# Create list of subbasin geometries
g = [i for i in subbasin.geometry]
basin = g[0][0]

# View the coordinate reference system (CRS) of both of your datasets
print('subbasin crs: ', basins.crs) # crop extent crs:  epsg:4326
print('dem crs: ', dem.rio.crs) # lidar crs:  EPSG:4326

# Plot subbasin over dem
f, ax = plt.subplots(figsize=(10, 5))
dem.plot.imshow(ax=ax)
subbasin.plot(ax=ax, alpha=.8)
ax.set(title="DEM with watershed polygon overlayed")
ax.set_axis_off()
plt.show()

# Crop raster data set with polygon
dem_clipped = dem.rio.clip(subbasin.geometry.apply(mapping))
            #   # This is needed if your GDF is in a diff CRS than the raster data
            #   polygon d.crs)

# Plot clipped raster
f, ax = plt.subplots(figsize=(10, 4))
dem_clipped.plot(ax=ax)
ax.set(title="DEM cropped to Geodataframe")
ax.set_axis_off()
plt.show()

# Export clipped raster to a new geotiff file
out_fp_raster = "data/dem_chm_cropped.tif"
dem_clipped.rio.to_raster(out_fp_raster)

# Read new geotiff
watershed = rxr.open_rasterio(out_fp_raster)

# Plot new geotiff
f, ax = plt.subplots(figsize=(10, 4))
watershed.plot(ax=ax, cmap='Greys')
ax.set(title="Final Clipped Watershed")
ax.set_axis_off()
plt.show()
