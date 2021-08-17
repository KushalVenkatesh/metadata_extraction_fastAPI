from typing import Optional

from fastapi import FastAPI

from metadata import eModul_metadata

app = FastAPI()


@app.get("/")
def read_root():
    return {"RESTful API": "metadata"}


@app.get("/dataFile")
def create_json_metadata(filePath: str, fileName: str):
    jsonList = eModul_metadata(filePath,fileName)
    return jsonList
