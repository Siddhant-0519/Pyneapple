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
from read_shapefile import read_shapefile
from Pyneapple.pyneapple.weight.rook import from_dataframe as rook
import jpype
import os
from startJVM import start_jvm
from Pyneapple.pyneapple.regionalization.generalized_p import generalized_p
import time
from spopt.region.maxp import maxp as libMaxP
from Pyneapple.pyneapple.regionalization.scalable_maxp import scalable_maxp
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
        if filename.endswith(".shp"):
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

    empStartTime = time.time()
    max_p, labels = expressive_maxp(df, w, disname, minName, minLow, minHigh,
                                    maxName, maxLow, maxHigh, avgName, avgLow, avgHigh,
                                    sumName, sumLow, sumHigh, countLow, countHigh)
    empEndTime = time.time()
    empExecTime = empEndTime - empStartTime
    labels = labels.tolist()
    empResult = {"execution_time": empExecTime, "max_p": max_p, "labels": labels}

    return empResult


@app.get("/api/endpoint/generalizedP")
def gmpEndPoint(file_name: str, sim_attr: str, ext_attr: str,
                threshold: float, p: int):

    df = read_shapefile(data_dir, file_name)
    w = rook(df)
    prucStartTime = time.time()
    prucLabels = generalized_p(df, w, sim_attr, ext_attr, threshold, p)
    prucEndTime = time.time()
    prucExecTime = prucEndTime - prucStartTime
    prucResult = {"execution_time": prucExecTime, "labels": prucLabels}

    return prucResult


@app.get("/api/endpoint/libraryMaxP")
def libraryMaxP(file_name: str, attr_name: str, threshold_name: str, threshold: float):

    df = read_shapefile(data_dir, file_name)
    w = rook(df)
    lmpStartTime = time.time()
    lmpLabels = libMaxP(df, w, attr_name, threshold_name, threshold, 2)
    lmpEndTime = time.time()
    lmpExecTime = lmpEndTime - lmpStartTime
    lmpResult = {"execution_time": lmpExecTime, "labels": lmpLabels}

    return lmpResult


@app.get("/api/endpoint/ScalableMaxP")
def scalable_p(file_name: str, sim_attr: str, ext_attr: str, threshold: float):

    df = read_shapefile(data_dir, file_name)
    w = rook(df)
    smpStartTime = time.time()
    smpLabels = scalable_maxp(df, w, sim_attr, ext_attr, threshold)
    smpEndTime = time.time()
    smpExecTime = smpEndTime - smpStartTime
    smpResult = {"execution_time": smpExecTime, "labels": smpLabels}

    return smpResult


@app.get("/api/enpoint/compareMaxP")
def compareMaxP(file_name: str, sim_attr: str, ext_attr: str,
                threshold: float):
    
    lmpResult = libraryMaxP(file_name, sim_attr, ext_attr, threshold)
    lmpTime = lmpResult["execution_time"]
    smpResult = scalable_p(file_name, sim_attr, ext_attr, threshold)
    smpTime = smpResult["execution_time"]
    speedup = lmpTime/smpTime

    comparisionResult = {"ScalableMaxP_ExecutionTime": smpTime,
                         "LibraryMaxP_ExecutionTime": lmpTime,
                         "Total_SpeedUp(Percentage)": speedup*100,
                         "ScalableMaxP_Labels": smpResult["labels"],
                         "LibraryMaxP_Labels": lmpResult["labels"]}
    return comparisionResult


if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8000)
