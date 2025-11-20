import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src")))
from pdf_extractor import extract_text_from_pdf, get_preview_300_words
from qa_engine import answer_question


if __name__ == "__main__":
    # 1) Load a sample PDF (relative path as requested)
    pdf_path = "sample_pdfs\Sample pdf.pdf"

    # 2) Extract full text
    print("[1] Extracting text...")
    try:
        full_text = extract_text_from_pdf(pdf_path)
    except FileNotFoundError:
        print(f"PDF not found at: {pdf_path}")
        raise SystemExit(1)
    except Exception as exc:
        print(f"Failed to extract text from PDF: {exc}")
        raise SystemExit(1)

    # 3) Show preview (first 300 words)
    preview = get_preview_300_words(full_text)
    print("=== PDF Preview (300 words) ===")
    print(preview)
    print()

    # 4) Hardcode a question
    question = "What is the document mainly about?"
    print("=== Question ===")
    print(question)
    print()

    # 5) Call answer_question
    result = answer_question(question, full_text)

    # 6) Print fields cleanly
    print(f"Detected language: {result.get('detected_language', '')}")
    print(f"Translated question: {result.get('translated_question', '')}")
    print(f"Answer (English): {result.get('answer_en', '')}")
    print(f"Final answer: {result.get('final_answer', '')}")
