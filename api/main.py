from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from api.routers.agg import router as router_agg
from api.routers.butterfly import router as router_butterfly
from api.routers.check import router as router_check
from api.routers.observations import router as router_observations
from api.routers.sunspot_number import router as router_sunspot_number
from api.routers.sunspot_number_with_flare import (
    router as router_sunspot_number_with_flare,
)
from api.routers.sunspot_number_with_silso import (
    router as router_sunspot_number_with_silso,
)
from api.routers.utils import router as router_utils

app = FastAPI()

app.include_router(router_agg, prefix="/api")
app.include_router(router_butterfly, prefix="/api")
app.include_router(router_check, prefix="/api")
app.include_router(router_observations, prefix="/api")
app.include_router(router_sunspot_number, prefix="/api")
app.include_router(router_sunspot_number_with_flare, prefix="/api")
app.include_router(router_sunspot_number_with_silso, prefix="/api")
app.include_router(router_utils, prefix="/api")
app.mount("/", StaticFiles(directory="dist", html=True), name="app")
