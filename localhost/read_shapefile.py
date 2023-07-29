import geopandas as gpd
import os
# import libpysal

os.environ["SHAPE_RESTORE_SHX"] = "YES"

# filename = "mexicojoin.shp"
# data_dir = "D:/user_pa1n/VSCode/projects/Pyneapple/testData"


def read_shapefile(data_dir,  filename):
    file_path = os.path.join(data_dir, filename)
    gdf = gpd.read_file(file_path)
    return gdf

# pth = libpysal.examples.get_path("mexicojoin.shp")
# mexico = gpd.read_file(pth)

# print(mexico.head())


# print(read_shapefile(data_dir, filename))
