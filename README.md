PDF Question Answering System — Mini Project

**A fast and lightweight Retrieval-Augmented PDF Question Answering system built using FastAPI, Streamlit, FAISS and FLAN-T5.**

A lightweight system that can extract text from PDFs, preview content, and answer user questions using a retrieval-augmented small LLM.

⭐ Features

Upload any PDF and view a 300-word preview.

Automatically extract text using pdfplumber.

Split PDF into chunks and search relevant sections with:

- Sentence-Transformers embeddings
- FAISS vector search

Answer questions using google/flan-t5-small (fast + free).

Multilingual questions supported (auto-translate).

Clean Streamlit UI + FastAPI backend.

📁 Project Structure
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
│   ├── pdf_extractor.py      # PDF text extraction + preview
│   ├── language_utils.py     # Language detection + translation
│   ├── retrieval_utils.py    # Chunking + embeddings + FAISS retrieval
│   └── qa_engine.py          # Complete QA pipeline
│
├── data/uploads/             # Uploaded PDFs stored here
└── requirements.txt

🔧 Installation (Windows)
1️⃣ Create and activate virtual environment
```bat
python -m venv venv
venv\Scripts\activate
```

2️⃣ Install dependencies
```bat
pip install -r requirements.txt
```

🚀 Running the Project
▶️ Start backend (FastAPI)
```bat
uvicorn backend.fast_api:app --reload --port 8000
```

▶️ Start frontend (Streamlit)
```bat
streamlit run frontend/app.py
```

🔥 How it Works
1) PDF Upload

User uploads PDF → server saves it → extracts text → sends 300-word preview.

2) Question Answering

- Detect language
- Translate (if needed)
- Chunk PDF → embed → FAISS search
- Prepare prompt with top chunks
- Run FLAN-T5-small
- Return answer

📝 Notes

- First run downloads models → takes time.
- FLAN-T5-small loads only once (fast after that).
- System works without GPU.
- Tested on Windows 10/11.

📌 Optional Future Improvements

- Better UI with expandable preview
- GPU acceleration
- History of questions
- Multi-PDF library search


🧰 Tech Stack Used

🧠 LLM: google/flan-t5-small
🔍 Retrieval: Sentence-Transformers + FAISS
📄 Extraction: pdfplumber
⚙️ Backend: FastAPI + Uvicorn
🎨 Frontend: Streamlit

**Screenshots**

<details>
<summary>📸 Click to View Screenshots</summary>

Below are screenshots of the running Streamlit frontend and sample QA outputs.

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


