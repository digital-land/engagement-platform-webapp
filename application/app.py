from fastapi import FastAPI, Request
from time import time
import asyncio
import json
from application.routers import (
    validation,
    home
)

app = FastAPI()

cmsUrl = "http://localhost:8000/api/v2/pages/4/?format=json"
conservationAreaUrl = "https://www.planning.data.gov.uk/dataset/conservation-area.json"

app.include_router(home.router)
app.include_router(validation.router, prefix="/validation")





