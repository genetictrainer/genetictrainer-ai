from fastapi import FastAPI, UploadFile, File, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import shutil
import os

app = FastAPI()
templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
async def upload_form(request: Request):
    return templates.TemplateResponse("upload.html", {"request": request})

@app.post("/upload", response_class=HTMLResponse)
async def handle_upload(request: Request, file: UploadFile = File(...)):
    contents = await file.read()
    decoded = contents.decode("utf-8")

    # Basit örnek işlem: İlk 10 satırı göster
    lines = decoded.splitlines()
    preview = "\n".join(lines[:10])

    return templates.TemplateResponse("result.html", {"request": request, "result": preview})
