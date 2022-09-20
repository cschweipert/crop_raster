import matplotlib.pyplot as plt
import earthpy.spatial as es
import earthpy.plot as ep
import rioxarray as rxr

   
dtm = rxr.open_rasterio("data/dem_chm_cropped.tif", masked=True).squeeze()

# Plot the data
ep.plot_bands(
    dtm,
    cmap="gist_earth",
    title="DTM Without Hillshade",
    figsize=(10, 6),
)
plt.show()

# Create and plot the hillshade with earthpy
hillshade = es.hillshade(dtm)

ep.plot_bands(
    hillshade,
    cbar=False,
    title="Hillshade made from DTM",
    figsize=(10, 6),
)
plt.show()

# Change the azimuth of the hillshade layer
hillshade_azimuth_210 = es.hillshade(dtm, azimuth=210)

# Plot the hillshade layer with the modified azimuth
ep.plot_bands(
    hillshade_azimuth_210,
    cbar=False,
    title="Hillshade with Azimuth set to 210 Degrees",
    figsize=(10, 6),
)
plt.show()

# Adjust the azimuth value
hillshade_angle_10 = es.hillshade(dtm, altitude=10)

# Plot the hillshade layer with the modified angle altitude
ep.plot_bands(
    hillshade_angle_10,
    cbar=False,
    title="Hillshade with Angle Altitude set to 10 Degrees",
    figsize=(10, 6),
)
plt.show()

# Plot the DEM and hillshade at the same time
# sphinx_gallery_thumbnail_number = 5
fig, ax = plt.subplots(figsize=(10, 6))
ep.plot_bands(
    dtm,
    ax=ax,
    cmap="terrain",
    title="DTM overlayed on top of a hillshade",
)
ax.imshow(hillshade, cmap="Greys", alpha=0.5)
plt.show()