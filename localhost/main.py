from fastapi import FastAPI, File, UploadFile
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
import os
from startJVM import start_jvm

app = FastAPI()

data_dir = "D:/user_pa1n/VSCode/projects/Pyneapple/testData"


@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    file_name = file.filename
    file_path = os.path.join(data_dir, file_name)

    with open(file_path, "wb") as f:
        contents = await file.read()
        f.write(contents)

    return {"Successfully uploaded : ", file_name}


@app.get("/listFiles")
async def list_files():
    files = []
    for filename in os.listdir(data_dir):
        files.append(filename)
    return files


start_jvm()


@app.get("/api/endpoint")
def empEndPoint(file_name: str, disname: str,
                minName: str, minLow: float, minHigh: float,
                maxName: str, maxLow: float, maxHigh: float,
                avgName: str, avgLow: float, avgHigh: float,
                sumName: str, sumLow: float, sumHigh: float,
                countLow: float, countHigh: float):
    
    df = read_shapefile(data_dir, file_name)
    w = rook(df)

    max_p, labels = emp(df, w, disname, minName, minLow, minHigh,
                        maxName, maxLow, maxHigh, avgName, avgLow, avgHigh,
                        sumName, sumLow, sumHigh, countLow, countHigh)
    labels = labels.tolist()
    empResult = {"max_p": max_p, "labels": labels}
    return empResult


if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8000)
