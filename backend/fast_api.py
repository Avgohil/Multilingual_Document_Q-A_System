import sys
import os
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse
from pathlib import Path
from backend.question_api import router as question_router

import shutil
import uuid

# Add src folder to import path
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
SRC_DIR = os.path.join(CURRENT_DIR, "..", "src")
sys.path.append(SRC_DIR)

from pdf_extractor import extract_text_from_pdf, get_preview_300_words

app = FastAPI()
app.include_router(question_router)


UPLOAD_DIR = Path("data/uploads")
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)


@app.post("/upload-preview")
async def upload_preview(file: UploadFile = File(...)):
    """Upload PDF → save → extract → return 300-word preview"""

    if not file.filename.lower().endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files allowed")

    unique_name = f"{uuid.uuid4().hex}_{file.filename}"
    dest_path = UPLOAD_DIR / unique_name

    # Save file
    with dest_path.open("wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # Extract text
    full_text = extract_text_from_pdf(str(dest_path))
    preview = get_preview_300_words(full_text)

    return JSONResponse({
        "filename": unique_name,
        "preview": preview,
        "message": "ok"
    })
