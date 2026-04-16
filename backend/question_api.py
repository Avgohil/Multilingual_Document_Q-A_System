import sys, os
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from pathlib import Path
from typing import List

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
SRC_DIR = os.path.join(CURRENT_DIR, "..", "src")
sys.path.append(SRC_DIR)

from pdf_extractor import extract_text_from_pdf
from qa_engine import answer_question_multi
from retrieval_utils import build_multi_doc_store, retrieve_from_multi_doc

router = APIRouter()

class AskRequest(BaseModel):
    filenames: List[str]   # ← ab list hai, single nahi!
    question: str

@router.post("/ask-question")
def ask_question(req: AskRequest):
    uploads_dir = Path("data/uploads")

    # Step 1: Sab PDFs ka text extract karo
    doc_texts = {}
    for filename in req.filenames:
        pdf_path = uploads_dir / filename
        if not pdf_path.is_file():
            raise HTTPException(status_code=404, detail=f"File not found: {filename}")
        try:
            doc_texts[filename] = extract_text_from_pdf(str(pdf_path))
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Text extraction failed: {e}")

    # Step 2: Multi-doc vector store banao
    try:
        index, embeddings, metadata = build_multi_doc_store(doc_texts)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Vector store failed: {e}")

    # Step 3: Answer generate karo
    try:
        result = answer_question_multi(req.question, index, embeddings, metadata)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"QA failed: {e}")

    return {
        "answer": result["final_answer"],
        "sources": result["sources"],   # ← ye naya hai!
        "detected_language": result["detected_language"],
        "message": "ok"
    }