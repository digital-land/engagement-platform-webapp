from fastapi.templating import Jinja2Templates
from fastapi import APIRouter, Request, File, UploadFile, Form
from application.core.utils import getPageApiFromTitle
from components.validation import validate_endpoint
from components import utils
from components.models.entity import Entity
import components.plugins.arcgis as arcgis
from application.models.entity_MapData import Entity_MapData
from application.logging.logger import get_logger

logger = get_logger(__name__)


templates = Jinja2Templates("application/templates")
router = APIRouter()


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
async def uploadFile(
    request: Request, file: UploadFile = File(None), link: str = Form(None)
):
    logger.info("Enter uploadFile method.")

    if file:
        userContent: str = utils.save_uploaded_file(file)

    if link:
        arcgisData = arcgis.arcgis_get(link)
        extracted_file = utils.save_contents_to_file(arcgisData)

        encoding = utils.detect_file_encoding(extracted_file)
        if encoding:
            logger.debug("encoding detected: %s", encoding)
            charset = ";charset=" + encoding
            userContent = utils._read_text_file(extracted_file, encoding, charset)

    entity = Entity()
    dataRaw = entity.fetch_data_from_csv(userContent)

    try:
        data = validate_endpoint(dataRaw)
    except Exception as e:
        # catch file level errors here and render the file level error page
        logger.error("Error validating data: " + e)

    data = list(map(lambda entry: Entity_MapData(entry), data))
    # render the report page
    try:
        content = await getPageApiFromTitle("report")
    except Exception as e:
        return str(e)
    template = "validation/report.html"
    context = {
        "request": request,
        "data": list(map(lambda entry: entry.serialize(), data)),
        "content": content,
    }
    return templates.TemplateResponse(template, context)


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
