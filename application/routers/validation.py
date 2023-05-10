from fastapi.templating import Jinja2Templates
from fastapi import APIRouter, Request, File, UploadFile
from application.core.utils import makeRequest
from fastapi.responses import RedirectResponse
import httpx

templates = Jinja2Templates("application/templates")
router = APIRouter()

@router.get('/upload')
async def upload(request: Request):
    # cmsResponse = await makeRequest(cmsUrl)
    # conservationAreaDetailResponse = await makeRequest(conservationAreaUrl)
    template = 'validation/upload.html'
    context = {
        'request': request, 
    }
    return templates.TemplateResponse(template,context)

@router.post('/uploadFile')
async def uploadFile(file: UploadFile = File(...)):
    return RedirectResponse('/validation/report?filename='+file.filename, status_code=303)

    # async with httpx.AsyncClient() as client:
    #     response = await client.post('URL')
        
    # if(response.code == 200):
    #     return RedirectResponse('/validation/report?filename='+file.filename, status_code=303)
    # else:
    #     return response.message

@router.get('/report')
async def report(request: Request):
    template = 'validation/report.html'
    context = {
        'request': request, 
    }
    return templates.TemplateResponse(template,context)