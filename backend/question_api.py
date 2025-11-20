import sys, os
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from pathlib import Path

# ⭐ First fix src path
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
SRC_DIR = os.path.join(CURRENT_DIR, "..", "src")
sys.path.append(SRC_DIR)

# ⭐ Then import modules
from pdf_extractor import extract_text_from_pdf
from qa_engine import answer_question

router = APIRouter()

class AskRequest(BaseModel):
    filename: str
    question: str

@router.post("/ask-question")
def ask_question(req: AskRequest):
    uploads_dir = Path("data/uploads")
    pdf_path = uploads_dir / req.filename

    if not pdf_path.is_file():
        raise HTTPException(status_code=404, detail="File not found")

    try:
        full_text = extract_text_from_pdf(str(pdf_path))
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Text extraction failed: {exc}")

    try:
        result = answer_question(req.question, full_text)
        final = result.get("final_answer", "Answer not found")
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"QA failed: {exc}")

    return {"answer": final, "message": "ok"}
