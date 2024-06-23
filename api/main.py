from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from api.routers.agg import router as router_agg
from api.routers.sunspot_number import router as router_sunspot_number
from api.routers.utils import router as router_utils

app = FastAPI()

app.include_router(router_agg, prefix="/api")
app.include_router(router_sunspot_number, prefix="/api")
app.include_router(router_utils, prefix="/api")
app.mount("/", StaticFiles(directory="dist", html=True), name="app")
