import time
import io
import uvicorn
import os
from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from pydantic import BaseModel, Field
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from starlette.responses import StreamingResponse
from starlette.concurrency import run_in_threadpool
import subprocess


# run with
# python -m uvicorn server:app --host 0.0.0.0 --port 8080 --reload


# CORS stuff
app = FastAPI()
origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# mount static and template folder
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")


@app.get("/", response_class=HTMLResponse)
async def read_items(request: Request):
    return templates.TemplateResponse("map.html", {"request": request, })

# /sonify, accepts an int array as request body
class SonifyRequest(BaseModel):
    data: list = Field(..., example=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10])

@app.post("/sonify")
def sonify(request: SonifyRequest):
    data = ','.join([str(x) for x in request.data])
    name = str(int(round(time.time() * 1000)))
    subprocess.run("python sonify.py " + name + " " + data, shell=True)
    with open(name + "/final.mp4", "rb") as f:
        data = f.read()
    subprocess.run("rd /s /q " + name, shell=True)
    return StreamingResponse(io.BytesIO(data), media_type="video/mp4")



