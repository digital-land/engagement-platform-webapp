from fastapi.templating import Jinja2Templates
from fastapi import APIRouter, Request
from application.core.utils import makeRequest

templates = Jinja2Templates("application/templates")
router = APIRouter()

@router.get('/upload')
async def f(request: Request):
    # cmsResponse = await makeRequest(cmsUrl)
    # conservationAreaDetailResponse = await makeRequest(conservationAreaUrl)
    template = 'validation/upload.html'
    context = {
        'request': request, 
    }
    return templates.TemplateResponse(template,context)

@router.get('/uploadFile')
async def f(request: Request):
    # cmsResponse = await makeRequest(cmsUrl)
    # conservationAreaDetailResponse = await makeRequest(conservationAreaUrl)
    template = 'validation/upload.html'
    context = {
        'request': request, 
    }
    return templates.TemplateResponse(template,context)

@router.get('/report')
async def f(request: Request):
    cmsResponse = await makeRequest(cmsUrl)
    conservationAreaDetailResponse = await makeRequest(conservationAreaUrl)
    template = 'validation/upload.html'
    context = {
        'request': request, 
    }
    return templates.TemplateResponse(template,context)