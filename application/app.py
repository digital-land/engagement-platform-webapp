from fastapi import FastAPI, Request
from time import time
import httpx
import asyncio
import json
from fastapi.templating import Jinja2Templates

templates = Jinja2Templates("application/templates")

app = FastAPI()

cmsUrl = "http://localhost:8000/api/v2/pages/4/?format=json"
conservationAreaUrl = "https://www.planning.data.gov.uk/dataset/conservation-area.json"


async def makeRequest(url):
    async with httpx.AsyncClient() as client:
        response = await client.get(url)
        print
        return response.text


@app.get('/')
async def f(request: Request):
    cmsResponse = await makeRequest(cmsUrl)
    conservationAreaDetailResponse = await makeRequest(conservationAreaUrl)
    template = 'prototype.html'
    context = {
        'request': request, 
        'cmsData': json.loads(cmsResponse), 
        'conservationAreaDetail': json.loads(conservationAreaDetailResponse),
    }
    return templates.TemplateResponse(template,context)