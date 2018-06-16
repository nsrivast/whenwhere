import cartopy
import cartopy.crs as ccrs
import matplotlib as mpl
mpl.use('TkAgg')
import matplotlib.pyplot as plt

crs = ccrs.PlateCarree()

ax = plt.axes(projection=crs)
ax.set_global()
#ax.set_extent((-80.0, 20.0, 10.0, 80.0), crs=crs)
ax.coastlines()

ax.scatter([-74], [41], s=[4], transform=crs)

plt.show()