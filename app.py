from fastapi import FastAPI, UploadFile, File, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import pdfplumber
import os
GT_VARIANT_DB = {
    "rs1815739": {
        "TT": "Sprint/Patlayıcı kas tipi avantajı (ACTN3 yokluğu)",
        "CT": "Karma kas tipi, hem dayanıklılık hem patlayıcılık",
        "CC": "Dayanıklılık kas tipi baskın, ACTN3 var"
    },
    "rs4680": {
        "GG": "Dopamin yıkımı hızlı, stres toleransı düşük (COMT)",
        "AG": "Dengeli dopamin seviyesi",
        "AA": "Dopamin yıkımı yavaş, odaklanma ve hafıza güçlü"
    },
    "rs1042713": {
        "GG": "Beta-adrenerjik reseptör duyarlılığı düşük",
        "AG": "Orta düzey reseptör yanıtı",
        "AA": "Egzersize yüksek kardiyovasküler yanıt"
    }
}
app = FastAPI()
templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
async def upload_form(request: Request):
    return templates.TemplateResponse("upload.html", {"request": request})

@app.post("/upload", response_class=HTMLResponse)
async def upload_file(request: Request, file: UploadFile = File(        results = {}
       GT_VARIANT_DB.get(rs_id)
                    if variant_info:
                        explanation = variant_info.get(genotype)
                        if explanation:
                            results[rs_id] = explanation
..)):
    contents = await file.read()

    if file.filename.endswith(".pdf"):
        with open("temp.pdf", "wb") as f:
            f.write(contents)

        extracted_text = ""
        with pdfplumber.open("temp.pdf") as pdf:
            for page in pdf.pages:
                extracted_text += page.extract_text() or ""
        results = {}
        for line in extracted_text.split("\n"):
            parts = line.strip().split()
            for part in parts:
                if part.startswith("rs") and len(parts) >= 2:
                    rs_id = part
                    genotype = parts[-1]
                    variant_info = GT_VARIANT_DB.get(rs_id)
                    if variant_info:
                        explanation = variant_info.get(genotype)
                        if explanation:
                            results[rs_id] = explanation
        os.remove("temp.pdf")
        preview = extracted_text[:2000]
    else:
        preview = "Lütfen sadece PDF dosyası yükleyin."

    return templates.TemplateResponse("result.html", {"request": request, "result": preview})
