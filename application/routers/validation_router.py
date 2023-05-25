from io import StringIO
from fastapi.templating import Jinja2Templates
from fastapi import APIRouter, Request, File, UploadFile
from application.core.utils import getPageContent, getPageApiFromTitle
import json
import pandas as pd
import shapely.wkt
from shapely.geometry import mapping
from main.main import validate_endpoint
import os


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
    response = await validate_endpoint(file)
    return response


@router.get("/")
@router.get("/upload")
async def upload(request: Request):
    content = await getPageApiFromTitle('upload')

    template = "validation/upload.html"
    context = {
        "request": request,
        "content": content,
    }
    return templates.TemplateResponse(template, context)


# Get the data
# format the data
# validate the file
# add errors to data
# add additional map data to data
# return the template
@router.post("/report")
async def uploadFile(request: Request, file: UploadFile = File(...)):
    content = await getPageApiFromTitle('report')

    data = parseCsv(file)

    data = formatData(data)

    response = await validateFile(file)

    response_text = response[0]
    responseData = json.loads(response_text)

    if (
        len(responseData["errors"]) == 1
        and responseData["errors"][0]["scope"] == "File"
    ):
        return responseData["errors"][0]

    for error in responseData["errors"]:
        data[error["rowNumber"] - 1]["errors"].append(error)
        if error["errorCode"] == "F003":
            data[error["rowNumber"] - 1]["mapData"]["outsideUk"] = "true"

    if responseData["status"] == "FAILED":
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


@router.get("/testbench")
async def testbench(request: Request):
    print(os.getcwd())
    testdata = open('./application/assets/mockdata/testbench.json')
    template = "validation/testbench.html"
    context = {
        "request": request,
        "dataPoints": json.loads(testdata.read())
    }
    return templates.TemplateResponse(template, context)
