import sys
import os

project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)

from fastapi import FastAPI, File, UploadFile
from typing import List
import numpy as np
from Pyneapple.pyneapple.regionalization.expressive_maxp import expressive_maxp
import geopandas as gpd
import uvicorn
#from pydantic import BaseModel
from Pyneapple.notebooks.data.LACity.read_shapefile import read_shapefile
from Pyneapple.pyneapple.weight.rook import from_dataframe as rook
import jpype
import os
from startJVM import start_jvm
from Pyneapple.pyneapple.regionalization.generalized_p import generalized_p
import time

app = FastAPI()

data_dir = "D:/user_pa1n/VSCode/projects/pyneapple_v2/testData"
weights_dir = "D:/user_pa1n/VSCode/projects/pyneapple_v2/Pyneapple/pyneapple/weight"

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


@app.get("/listWeights")
async def list_weights():
    weights = []
    for weight in os.listdir(weights_dir):
        weights.append(weight)
    return weights   


@app.get("/api/endpoint/emp")
def empEndPoint(file_name: str, disname: str,
                minName: str, minLow: float, minHigh: float,
                maxName: str, maxLow: float, maxHigh: float,
                avgName: str, avgLow: float, avgHigh: float,
                sumName: str, sumLow: float, sumHigh: float,
                countLow: float, countHigh: float):

    df = read_shapefile(data_dir, file_name)
    w = rook(df)

    max_p, labels = expressive_maxp(df, w, disname, minName, minLow, minHigh,
                                    maxName, maxLow, maxHigh, avgName, avgLow, avgHigh,
                                    sumName, sumLow, sumHigh, countLow, countHigh)

    labels = labels.tolist()
    empResult = {"max_p": max_p, "labels": labels}
    return empResult


@app.get("/api/endpoint/generalizedMaxP")
def gmpEndPoint(file_name: str, sim_attr: str, ext_attr: str,
                 threshold: float, p: int):

    df = read_shapefile(data_dir, file_name)
    w = rook(df)

    prucResult = generalized_p(df, w, sim_attr, ext_attr, threshold, p)

    return prucResult


if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8000)
