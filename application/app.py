from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from application.routers import validation_router, home

# test change

app = FastAPI()

# add static files
app.mount(
    "/static",
    StaticFiles(directory="application/static"),
    name="static",
)

cmsUrl = "http://localhost:8000/api/v2/pages/4/?format=json"
conservationAreaUrl = "https://www.planning.data.gov.uk/dataset/conservation-area.json"

app.include_router(home.router)
app.include_router(validation_router.router, prefix="/validation")
