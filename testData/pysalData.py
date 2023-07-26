import geopandas as gpd
import libpysal as lp

name = 'mexicojoin.shp'

df = lp.examples.get_path(name)
print(df)
