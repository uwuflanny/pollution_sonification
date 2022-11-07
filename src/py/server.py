import time
import io
import uvicorn
import os
import json
from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from pydantic import BaseModel, Field
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from starlette.responses import StreamingResponse
from fastapi.responses import FileResponse
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

@app.get('/favicon.ico', include_in_schema=False)
async def favicon():
    return FileResponse('favicon.ico')

@app.get("/video", response_class=HTMLResponse)
async def read_items(request: Request):
    return templates.TemplateResponse("video.html", {"request": request, })

@app.get("/", response_class=HTMLResponse)
async def read_items(request: Request):
    return templates.TemplateResponse("map.html", {"request": request, })




# /sonify, accepts an int array as request body
class SonifyRequest(BaseModel):
    data:   list = Field(..., example=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
    days:   list = Field(..., example=["2021-01-01T00:00:00", "2021-01-01T00:00:01", "2021-01-01T00:00:02"])
    idx:    str

@app.post("/sonify")
def sonify(request: SonifyRequest):

    dir = str(int(round(time.time() * 1000)))
    payload = json.dumps({
        '"dir"': '"' + dir + '"',
        '"index"': '"' + request.idx + '"',
        '"data"': request.data,
        '"days"': ['"'+str(d)+'"' for d in request.days]
    })

    subprocess.run("python sonify.py " + '"' + payload +'"', shell=True)

    filename = dir + "/final.mp4"
    if os.path.exists(filename):
        with open(filename, "rb") as f:
            data = f.read()
        subprocess.run("rd /s /q " + dir, shell=True)
        return StreamingResponse(io.BytesIO(data), media_type="video/mp4")
    else:
        subprocess.run("rd /s /q " + dir, shell=True)
        raise HTTPException(status_code=404, detail="File not found")
