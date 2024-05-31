import uvicorn
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

app = FastAPI()

app.mount("/", StaticFiles(directory="dist", html=True), name="app")

if __name__ == "__main__":
    uvicorn.run(app)
