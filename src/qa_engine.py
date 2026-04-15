"""
QA Engine using GROQ API (LLaMA3) - Fast, Powerful, Free
Handles:
 - Language detection
 - Translation
 - PDF text chunking
 - FAISS retrieval
 - LLM answer generation (Groq LLaMA3)
"""

import os
from typing import List, Dict, Tuple
from groq import Groq
from dotenv import load_dotenv

from language_utils import detect_language, translate_to_english, translate_to_language
from retrieval_utils import split_into_chunks, build_vector_store, retrieve_top_chunks

load_dotenv()

# ⭐ Groq client - loads once
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def prepare_prompt(question_en: str, retrieved_chunks: List[str]) -> str:
    """Prepare prompt for Groq LLaMA3."""
    numbered = [f"[{i}] {c}" for i, c in enumerate(retrieved_chunks, start=1)]
    chunks_block = "\n\n".join(numbered)

    return f"""You are a helpful research assistant. Answer the question ONLY using the PDF excerpts below.
If the answer is not present, say: "Answer not found in document."
Give clear, factual, concise answers.

PDF Excerpts:
{chunks_block}

Question: {question_en}

Answer:"""


def _call_llm(prompt: str) -> Tuple[bool, str]:
    """Generate answer using Groq LLaMA3."""
    try:
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=512,
            temperature=0.2
        )
        text = response.choices[0].message.content.strip()
        return True, text or "Answer not found"
    except Exception as e:
        print("Groq Error:", e)
        return False, "Answer not found"


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

        index, embeddings = build_vector_store(chunks)
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
        final_answer = translate_to_language(answer_en, detected) if detected not in ["unknown", "en"] else answer_en

        return {
            "detected_language": detected,
            "translated_question": translated_q,
            "answer_en": answer_en,
            "final_answer": final_answer,
        }

    except Exception as e:
        print("QA Error:", e)
        return {
            "detected_language": detected,
            "translated_question": translated_q,
            "answer_en": "Answer not found",
            "final_answer": "Answer not found",
        }