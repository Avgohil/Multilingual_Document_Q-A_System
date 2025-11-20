"""
FAST QA Engine using FLAN-T5-SMALL (Free, Fast, No Login Required)
Handles:
 - Language detection
 - Translation
 - PDF text chunking
 - FAISS retrieval
 - LLM answer generation (flan-t5-small)
"""

import os
from typing import List, Dict, Tuple

from language_utils import (
    detect_language,
    translate_to_english,
    translate_to_language,
)
from retrieval_utils import (
    split_into_chunks,
    build_vector_store,
    retrieve_top_chunks,
)

# HF flan-t5-small pipeline
try:
    from transformers import pipeline
except Exception:
    pipeline = None


# ⭐ Load FLAN-T5-SMALL only once → super fast QAS
LLM = pipeline(
    "text2text-generation",
    model="google/flan-t5-small",
    device_map="cpu"
)

def prepare_prompt(question_en: str, retrieved_chunks: List[str]) -> str:
    """Prepare prompt for flan-t5 model."""

    instructions = (
        "Answer the question ONLY using the PDF excerpts.\n"
        "If the answer is not present, reply: 'Answer not found in document.'\n"
        "Give short, factual answers."
    )

    numbered = [f"[{i}] {c}" for i, c in enumerate(retrieved_chunks, start=1)]
    chunks_block = "\n\n".join(numbered)

    prompt = (
        f"{instructions}\n\n"
        f"Question: {question_en}\n\n"
        f"PDF Excerpts:\n{chunks_block}\n\n"
        f"Answer:"
    )

    return prompt


# ----------------------------------------------------------
# 🚀 USE FLAN-T5-SMALL (FASTEST FREE MODEL)
# ----------------------------------------------------------
def _call_llm(prompt:str) -> Tuple[bool, str]:
    """Generate answer using preloaded FLAN-T5."""
    try:
        output = LLM(
            prompt,
            max_new_tokens=100,
        )
        text = output[0]["generated_text"].strip()
        return True, text or "Answer not found"
    except Exception as e:
        print("HF Error:", e)
        return False, "Answer not found"

# ----------------------------------------------------------
# 🔥 MAIN QA FUNCTION
# ----------------------------------------------------------
def answer_question(question: str, full_text: str) -> Dict[str, str]:

    detected = "unknown"
    translated_q = ""
    answer_en = "Answer not found"
    final_answer = "Answer not found"

    try:
        detected = detect_language(question)
        translated_q = translate_to_english(question)

        chunks = split_into_chunks(full_text)
        if not chunks:
            return {
                "detected_language": detected,
                "translated_question": translated_q,
                "answer_en": answer_en,
                "final_answer": final_answer,
            }

        try:
            index, embeddings = build_vector_store(chunks)
        except Exception:
            return {
                "detected_language": detected,
                "translated_question": translated_q,
                "answer_en": answer_en,
                "final_answer": final_answer,
            }

        retrieved = retrieve_top_chunks(translated_q, index, embeddings, chunks, top_k=5)
        retrieved_texts = [t for t, _ in retrieved]

        prompt = prepare_prompt(translated_q, retrieved_texts)

        ok, llm_text = _call_llm(prompt)
        if not ok:
            return {
                "detected_language": detected,
                "translated_question": translated_q,
                "answer_en": answer_en,
                "final_answer": final_answer,
            }

        answer_en = llm_text.strip()

        if detected != "unknown" and detected != "en":
            final_answer = translate_to_language(answer_en, detected)
        else:
            final_answer = answer_en

        return {
            "detected_language": detected,
            "translated_question": translated_q,
            "answer_en": answer_en,
            "final_answer": final_answer,
        }

    except Exception:
        return {
            "detected_language": detected,
            "translated_question": translated_q,
            "answer_en": "Answer not found",
            "final_answer": "Answer not found",
        }
