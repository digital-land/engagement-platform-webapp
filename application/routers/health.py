from fastapi.templating import Jinja2Templates
from fastapi import APIRouter, Request

templates = Jinja2Templates("application/templates")
router = APIRouter()

@router.get("/health")
async def f(request: Request):
    template = "health/index.html"
    context = {
        "request": request,
    }
    return templates.TemplateResponse(template, context)
