import geopandas as gpd
import os

os.environ["SHAPE_RESTORE_SHX"] = "YES"

#filename = "LACity.shp"
#data_dir = "D:/user_pa1n/VSCode/projects/Pyneapple/testData"


def read_shapefile(data_dir,  filename):
    file_path = os.path.join(data_dir, filename)
    gdf = gpd.read_file(file_path)
    return gdf


#print(read_shapefile(data_dir, filename))
