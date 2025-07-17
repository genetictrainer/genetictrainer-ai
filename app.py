from fastapi import FastAPI, UploadFile, File, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import pdfplumber
import os

app = FastAPI()
templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
async def upload_form(request: Request):
    return templates.TemplateResponse("upload.html", {"request": request})

@app.post("/upload", response_class=HTMLResponse)
async def upload_file(request: Request, file: UploadFile = File(...)):
    contents = await file.read()

    if file.filename.endswith(".pdf"):
        with open("temp.pdf", "wb") as f:
            f.write(contents)

        extracted_text = ""
        with pdfplumber.open("temp.pdf") as pdf:
            for page in pdf.pages:
                extracted_text += page.extract_text() or ""

        os.remove("temp.pdf")
        preview = extracted_text[:2000]
    else:
        preview = "Lütfen sadece PDF dosyası yükleyin."

    return templates.TemplateResponse("result.html", {"request": request, "result": preview})
