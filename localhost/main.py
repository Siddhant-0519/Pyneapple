from fastapi import FastAPI
from typing import List
import numpy as np
from pyneapple.regionalization.emp import emp
import geopandas as gpd
from libpysal import weights
import uvicorn
#from pydantic import BaseModel
from notebooks.data.LACity.read_shapefile import read_shapefile
from pyneapple.weight.rook import from_dataframe as rook
import jpype

# Rest of your code


app = FastAPI()



@app.get("/api/endpoint")
def empEndPoint(disname: str,
                minName: str, minLow: float, minHigh: float,
                maxName: str, maxLow: float, maxHigh: float,
                avgName: str, avgLow: float, avgHigh: float,
                sumName: str, sumLow: float, sumHigh: float,
                countLow: float, countHigh: float):
    
    df = read_shapefile()
    w = rook(df)

    max_p, labels = emp(df, w, disname, minName, minLow, minHigh,
                        maxName, maxLow, maxHigh, avgName, avgLow, avgHigh,
                        sumName, sumLow, sumHigh, countLow, countHigh)
    labels = labels.tolist()
    empResult = {"max_p": max_p, "labels": labels}
    return empResult


if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8000)
