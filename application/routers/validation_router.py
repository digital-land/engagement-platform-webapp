from fastapi.templating import Jinja2Templates
from fastapi import APIRouter, Request, File, UploadFile
from application.core.utils import getPageApiFromTitle
import json
import shapely.wkt
from shapely.geometry import mapping
from components.main import validate_endpoint, utils
from components.models.entity import Entity
import os
from application.logging.logger import get_logger

logger = get_logger(__name__)


templates = Jinja2Templates("application/templates")
router = APIRouter()


def formatData(data):
    try:
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
    except Exception as e:
        logger.error("Unable to format data: %s", str(e))

    return data


@router.get("/")
@router.get("/upload")
async def upload(request: Request):
    try:
        content = await getPageApiFromTitle("upload")
    except Exception as e:
        return str(e)

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
    logger.info("Enter uploadFile method.")
    try:
        content = await getPageApiFromTitle("report")
    except Exception as e:
        return str(e)

    filepath: str = utils.save_uploaded_file(file)

    entity = Entity()
    data = entity.fetch_data_from_csv(filepath)

    response = await validate_endpoint(data)

    try:
        response_text = response[0]
        responseData = json.loads(response_text)
    except Exception as e:
        logger.error("Error in loading response data: " + e)

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
    try:
        content = await getPageApiFromTitle(errorNumber)
    except Exception as e:
        return str(e)

    template = "validation/error.html"
    context = {
        "request": request,
        "content": content,
    }
    return templates.TemplateResponse(template, context)


@router.get("/testbench")
async def testbench(request: Request):
    print(os.getcwd())
    testdata = open("./application/assets/mockdata/testbench.json")
    template = "validation/testbench.html"
    context = {"request": request, "dataPoints": json.loads(testdata.read())}
    return templates.TemplateResponse(template, context)
