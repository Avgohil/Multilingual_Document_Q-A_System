# Multilingual PDF Question Answering System

**A fast, lightweight Retrieval-Augmented PDF Question Answering system built with FastAPI, Streamlit, FAISS & FLAN-T5.**

---

## Overview

This project allows users to:

- Upload any PDF
- View a 300-word preview
- Ask questions in any language (Gujarati, Hindi, English, etc.)
- Get answers using Retrieval-Augmented Generation (RAG)
- Use a clean Streamlit UI + FastAPI backend

All processing runs locally — no paid API required.

## Features

- PDF text extraction (`pdfplumber`)
- 300-word preview generator
- Sentence-Transformers embeddings (`all-MiniLM-L6-v2`)
- FAISS vector similarity search
- FLAN-T5-Small LLM for answer generation
- Multilingual question support (auto-translate)
- Streamlit UI for interaction
- FastAPI backend API
- Works offline after model download (CPU-friendly)

## Project Structure

```
DSAProject/
│
├── backend/
│   ├── fast_api.py           # /upload-preview endpoint
│   └── question_api.py       # /ask-question endpoint
│
├── frontend/
│   └── app.py                # Streamlit UI
│
├── src/
│   ├── pdf_extractor.py      # PDF extraction + preview
│   ├── language_utils.py     # Language detection + translation
│   ├── retrieval_utils.py    # Chunking + embeddings + FAISS
│   └── qa_engine.py          # Full QA pipeline
│
├── data/uploads/             # Uploaded PDFs
├── sample_pdfs/              # Sample test PDFs
└── requirements.txt
```

## System Architecture (RAG Pipeline)
```
Streamlit UI→ FastAPI → PDF Extraction → Chunking & Embeddings → FAISS Retrieval → FLAN-T5 Answer Generation
```
## Installation (Windows)

1. Create virtual environment

```bat
python -m venv venv
venv\Scripts\activate
```

2. Install dependencies

```bat
pip install -r requirements.txt
```

## Running the Project

Start the backend (FastAPI + Uvicorn):

```bat
uvicorn backend.fast_api:app --reload --port 8000
```

Start the frontend (Streamlit):

```bat
streamlit run frontend/app.py
```

## How It Works

1) PDF Upload

- User uploads a PDF via Streamlit
- Backend saves it to `data/uploads/`
- Extracts text using `pdfplumber`
- Returns 300-word preview

2) Question Answering Process

- Detect input language
- Translate → English (if needed)
- Split PDF into chunks
- Create embeddings with Sentence-Transformers
- Search relevant chunks via FAISS
- Build prompt with top-k chunks
- FLAN-T5 generates the answer
- Translate back to original language (if needed)
- Return final answer

## Tech Stack:

- **LLM / Answer Generator:** `google/flan-t5-small` (via `transformers` + `torch`) — lightweight and CPU-friendly.
- **Retrieval & Embeddings:** `sentence-transformers` (`all-MiniLM-L6-v2`) and `faiss-cpu`.
- **PDF Processing:** `pdfplumber`, `pymupdf` (optional).
- **Language Processing:** `langdetect` / `langid` (fallback), `deep-translator` (GoogleTranslator).
- **Backend:** `FastAPI`, `uvicorn`.
- **Frontend:** `Streamlit` (UI) + `requests` (client calls).
- **Utilities:** `numpy`, `scikit-learn`, and other dependencies listed in `requirements.txt`.

## Screenshots

<details>
<summary>📷 Click to view screenshots</summary>

<p align="center">
	<img src="Screenshots/Screenshot%202025-11-20%20171403.png" width="700"/>
	<br/>
	<img src="Screenshots/Screenshot%202025-11-20%20171524.png" width="700"/>
	<br/>
	<img src="Screenshots/Screenshot%202025-11-20%20170124.png" width="700"/>
	<br/>
	<img src="Screenshots/Screenshot%202025-11-20%20171354.png" width="700"/>
	<br/>
	<img src="Screenshots/Screenshot%202025-11-20%20171741.png" width="700"/>
	<br/>
	<img src="Screenshots/Screenshot%202025-11-20%20172039.png" width="700"/>
	<br/>
	<img src="Screenshots/Screenshot%202025-11-20%20172119.png" width="700"/>
	<br/>
	<img src="Screenshots/Screenshot%202025-11-20%20172646.png" width="700"/>
</p>

</details>


**Submitted By**

Name: Ankita Gohil
Project: Multilingual PDF Document QA System
Role: Engineering Student (7th Sem)


