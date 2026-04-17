# 🔬 Multilingual Document Q&A Research Assistant

A production-ready AI-powered research assistant that allows users to upload multiple PDFs and ask questions in any language — with cited answers and document summaries.

## 🚀 Features

- **Multi-Document Search** — Upload multiple PDFs and search across all of them simultaneously
- **Multilingual Support** — Ask questions in Hindi, Gujarati, English, Spanish, or any language
- **Source Citations** — Every answer mentions which document it came from
- **Chat Memory** — Ask follow-up questions with conversation context
- **Document Summarizer** — Generate structured summaries with key points
- **Powered by Groq LLaMA3** — Fast, accurate, GPT-4 level answers (free API)

## 🛠️ Tech Stack

| Layer | Technology |
|-------|-----------|
| LLM | Groq LLaMA 3.3 70B |
| Embeddings | sentence-transformers (all-MiniLM-L6-v2) |
| Vector Store | FAISS |
| Backend | FastAPI |
| Frontend | Streamlit |
| PDF Extraction | pdfplumber + PyMuPDF |
| Translation | deep-translator |
| Language Detection | langdetect |

## 📁 Project Structure

Multilingual_Document_Q-A_System/
├── backend/
│   ├── fast_api.py         # FastAPI app
│   ├── question_api.py     # QA + Summarize endpoints
│   
├── src/
│   ├── qa_engine.py        # Groq LLM integration
│   ├── retrieval_utils.py  # FAISS vector store
│   ├── pdf_extractor.py    # PDF text extraction
│   └── language_utils.py   # Translation & detection
├── frontend/
│   └── app.py              # Streamlit UI
├── data/uploads/           # Uploaded PDFs
└── requirements.txt

## ⚙️ Setup & Run

### 1. Clone & Setup
```bash
git clone https://github.com/Avgohil/Multilingual_Document_Q-A_System
cd Multilingual_Document_Q-A_System
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Add Groq API Key
Create `.env` file in root:
GROQ_API_KEY=your_groq_api_key_here

Get free key at: https://console.groq.com

### 3. Run Backend
```bash
uvicorn backend.fast_api:app --reload --port 8000
```

### 4. Run Frontend
```bash
streamlit run frontend/app.py
```

### 5. Open Browser
- Frontend: http://localhost:8501
- API Docs: http://127.0.0.1:8000/docs

## 🎯 How to Use

1. Upload one or more PDF documents
2. Ask questions in any language
3. Get cited answers showing which document answered
4. Use "Summarize" to get structured document summary
5. Ask follow-up questions — system remembers context

## 🏆 Project Highlights

- **RAG Pipeline** — Retrieval Augmented Generation for accurate answers
- **Semantic Search** — FAISS vector similarity search
- **Cross-lingual QA** — Detect → Translate → Answer → Translate back
- **Production Ready** — Clean API structure, error handling, modular code

## 📊 Architecture

User Question → Language Detection → English Translation
↓
FAISS Semantic Search across all uploaded PDFs
↓
Top-K relevant chunks retrieved with source info
↓
Groq LLaMA3 generates cited answer
↓
Answer translated back to user's language

