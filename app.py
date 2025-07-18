from fastapi import FastAPI, UploadFile, File, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import pdfplumber
import os

# Genetik varyant açıklama veritabanı
GT_VARIANT_DB = {
    "rs1815739": {
        "RR": "Sprint/patlayıcı kas tipi avantajı (ACTN3 yokluğu)",
        "RX": "Karma kas tipi, hem dayanıklılık hem patlayıcılık",
        "XX": "Dayanıklılık kas tipi baskın, ACTN3 var"
    },
    "rs4340": {
        "II": "Dayanıklılık performansı yüksek (ACE)",
        "ID": "Karma özellik (ACE)",
        "DD": "Patlayıcı güç performansı (ACE)"
    },
    "rs1800012": {
        "GG": "Doku onarımı daha yavaş, sakatlık riski artabilir (COL1A1)",
        "GT": "Orta seviye risk",
        "TT": "Doku onarımı avantajlı, sakatlık riski düşük (COL1A1)"
    },
    "rs143383": {
        "TT": "Eklem esnekliği düşük olabilir, sakatlık riski artabilir (GDF5)",
        "CT": "Orta düzey esneklik",
        "CC": "Eklem esnekliği iyi, yaralanma riski düşük (GDF5)"
    },
    "rs4880": {
        "GG": "Antioksidan koruma düşük, toparlanma süresi uzayabilir (SOD2)",
        "AG": "Orta düzey koruma",
        "AA": "Antioksidan koruma yüksek, toparlanma süresi kısalabilir (SOD2)"
    },
    "rs1800795": {
        "GG": "Düşük iltihaplanma yanıtı, toparlanma avantajlı olabilir (IL-6)",
        "GC": "Orta düzey iltihap yanıtı",
        "CC": "Yüksek iltihap yanıtı, toparlanma gecikebilir (IL-6)"
    },
    "rs2228145": {
        "AA": "İnflamasyon kontrolü zayıf olabilir (IL-6R)",
        "AC": "Orta düzey kontrol",
        "CC": "İnflamasyon kontrolü güçlü (IL-6R)"
    },
    "rs1800629": {
        "GG": "Normal bağışıklık ve toparlanma (TNF)",
        "GA": "Orta düzey toparlanma",
        "AA": "Yüksek inflamasyon riski, toparlanma gecikebilir (TNF)"
    },
    "rs3093066": {
        "CC": "Sürantrenman riski yüksek, toparlanma zayıf, katabolizma artabilir (CRP)",
        "CA": "Orta düzey toparlanma",
        "AA": "Toparlanma avantajlı, sürantrenman riski düşüktür (CRP)"
    }
}

app = FastAPI()
templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
async def upload_form(request: Request):
    return templates.TemplateResponse("upload.html", {"request": request})

@app.post("/upload", response_class=HTMLResponse)
async def upload_file(
    request: Request,
    file: UploadFile = File(...),
    age: int = Form(...),
    gender: str = Form(...),
    sport_branch: str = Form(...),
    fitness_goal: str = Form(...)
):
    results = {}
    try:
        with pdfplumber.open(file.file) as pdf:
            for page in pdf.pages:
                text = page.extract_text()
                lines = text.split("\n")
                for line in lines:
                    parts = line.strip().split()
                    if len(parts) >= 3:
                        rs_id = parts[1]
                        genotype = parts[-1]
                        variant_info = GT_VARIANT_DB.get(rs_id)
                        if variant_info:
                            explanation = variant_info.get(genotype)
                            if explanation:
                                results[rs_id] = explanation
    except Exception as e:
        results = {"error": f"Dosya okunamadı: {str(e)}"}

    # Yaş mantığı (antrenman/supplement tavsiyesi verilecek mi)
    show_plan = age >= 14
    age_warning = ""
    if age < 14:
        age_warning = "Antrenman, beslenme ve supplement önerileri için lütfen antrenörünüze danışın."

    return templates.TemplateResponse("result.html", {
        "request": request,
        "results": results,
        "age": age,
        "gender": gender,
        "sport_branch": sport_branch,
        "fitness_goal": fitness_goal,
        "show_plan": show_plan,
        "age_warning": age_warning
    })
