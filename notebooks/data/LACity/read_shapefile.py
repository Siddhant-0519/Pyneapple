import geopandas as gpd
import os

os.environ["SHAPE_RESTORE_SHX"] = "YES"


def read_shapefile():
    shapefile_path = "D:/user_pa1n/VSCode/projects/Pyneapple/notebooks/data/LACity/LACity.shp"
    gdf = gpd.read_file(shapefile_path)
    return gdf


#print(read_shapefile())
