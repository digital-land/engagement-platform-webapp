from io import StringIO
from fastapi.templating import Jinja2Templates
from fastapi import APIRouter, Request, File, UploadFile
from application.core.utils import makeRequest, getPageContent, getPageApiFromTitle
from application.core.polygonHelp import points
import httpx
import os
import json
import pandas as pd
import shapely.wkt
from shapely.geometry import mapping
# from validators import validate

templates = Jinja2Templates("application/templates")
router = APIRouter()

def parseCsv(file):
    file.file.seek(0)
    contents = file.file.read().decode("utf-8")

    csvStringIO = StringIO(contents)
    dataColumns = pd.read_csv(csvStringIO, sep=",", header=None)

    data = []

    for index in dataColumns:
        column = dataColumns[index]
        for row_i, row_v in enumerate(column):
            if row_i == 0:
                continue
            if len(data) < row_i:
                data.append({"attributes": {}, "mapData": {}, "errors": []})
            data[row_i - 1]["attributes"][column[0]] = row_v

    return data


def formatData(data):
    for index, row in enumerate(data):
        polygon = shapely.wkt.loads(row["attributes"]["Geometry"])
        polygons = mapping(polygon)["coordinates"]
        data[index]["attributes"]["Geometry"] = json.dumps(polygons)
        point = shapely.wkt.loads(row["attributes"]["Point"])
        data[index]["attributes"]["Point"] = [point.x, point.y]
        data[index]["mapData"]["bounds"] = [
            [polygon.bounds[1], polygon.bounds[0]],
            [polygon.bounds[3], polygon.bounds[2]],
        ]
    return data


async def validateFile(file):
    async with httpx.AsyncClient() as client:
        response = await client.post(
            "http://127.0.0.1:5000/validate", files={"file": (file.filename, file.file)}
        )
        return response


@router.get("/")
@router.get("/upload")
async def upload(request: Request):
    content = await getPageContent(6)

    template = "validation/upload.html"
    context = {
        "request": request,
        "content": content,
    }
    return templates.TemplateResponse(template, context)


@router.post("/report")
async def uploadFile(request: Request, file: UploadFile = File(...)):
    content = await getPageContent(7)

    data = parseCsv(file)

    data = formatData(data)

    response = await validateFile(file)

    responseData = response.json()

    for error in responseData['errors']:
        data[error["rowNumber"] - 1]["errors"].append(error)

    if(responseData['status'] == 'FAILED'):
        template = "validation/report.html"
        context = {
            "request": request,
            "data": data,
            "content": content,
        }
        return templates.TemplateResponse(template, context)
    else:
        return "File Ok"


@router.get("/errors/{errorNumber}")
async def error(request: Request, errorNumber: str):
    data = await getPageApiFromTitle(errorNumber)
    template = "validation/error.html"
    context = {
        "request": request,
        "content": data,
    }
    return templates.TemplateResponse(template, context)
