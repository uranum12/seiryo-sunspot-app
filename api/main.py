import uvicorn
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from routers.agg import router as router_agg

app = FastAPI()

app.include_router(router_agg, prefix="/api")
app.mount("/", StaticFiles(directory="dist", html=True), name="app")

if __name__ == "__main__":
    uvicorn.run(app)
