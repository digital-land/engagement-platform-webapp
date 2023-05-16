from fastapi.templating import Jinja2Templates
from fastapi import APIRouter, Request

templates = Jinja2Templates("application/templates")
router = APIRouter()


@router.get("/")
async def f(request: Request):
    template = "home/home.html"
    context = {
        "request": request,
    }
    return templates.TemplateResponse(template, context)
