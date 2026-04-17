import streamlit as st
import requests

st.set_page_config(
    page_title="Research Assistant",
    page_icon="🔬",
    layout="wide",
)

st.markdown(
    """
    <style>
    html, body, [class*="css"] {
        font-size: 17px;
    }

    .main .block-container {
        max-width: 1200px;
        padding-top: 1.2rem;
        padding-bottom: 1.2rem;
    }

    h1 {
        font-size: 2rem !important;
        font-weight: 700 !important;
    }

    h2, h3 {
        font-size: 1.3rem !important;
    }

    p, li, label, .stMarkdown, .stText {
        font-size: 1rem !important;
        line-height: 1.55;
    }

    .stButton > button {
        font-size: 1rem !important;
        border-radius: 8px;
    }

    .stChatMessage {
        border-radius: 10px;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

UPLOAD_URL = "http://127.0.0.1:8000/upload-preview"
ASK_URL = "http://127.0.0.1:8000/ask-question"
SUMMARY_URL = "http://127.0.0.1:8000/summarize"


def post_with_error_handling(url: str, *, files=None, json_payload=None, timeout: int = 45):
    """Call backend safely and return (ok, response_or_message)."""
    try:
        if files is not None:
            res = requests.post(url, files=files, timeout=timeout)
        else:
            res = requests.post(url, json=json_payload, timeout=timeout)
        return True, res
    except requests.exceptions.ConnectionError:
        return False, "Backend is not running on http://127.0.0.1:8000. Start FastAPI first."
    except requests.exceptions.Timeout:
        return False, "Backend request timed out. Please try again."
    except requests.exceptions.RequestException as exc:
        return False, f"Request failed: {exc}"

# ── Session State Init ──
if "uploaded_files" not in st.session_state:
    st.session_state["uploaded_files"] = {}  # {filename: preview}

if "chat_history" not in st.session_state:
    st.session_state["chat_history"] = []  # [{question, answer, sources}]

# ── Title ──
st.markdown("<h1 style='text-align:center;'>🔬 Multilingual Research Assistant</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center; color:gray;'>Upload multiple PDFs • Ask questions • Get cited answers</p>", unsafe_allow_html=True)
st.divider()

col1, col2 = st.columns([1, 1.4])

# ─────────────────────────────
# LEFT → Upload PDFs
# ─────────────────────────────
with col1:
    st.subheader("📂 Step 1: Upload PDFs")

    uploaded_file = st.file_uploader(
        "Upload a PDF (upload multiple one by one)",
        type=["pdf"]
    )

    if uploaded_file:
        already_uploaded = any(
            uploaded_file.name in fname
            for fname in st.session_state["uploaded_files"]
        )
        if not already_uploaded:
            with st.spinner(f"Uploading {uploaded_file.name}..."):
                files = {"file": (uploaded_file.name, uploaded_file, "application/pdf")}
                ok, response = post_with_error_handling(UPLOAD_URL, files=files)

            if not ok:
                st.error(response)
            elif response.status_code == 200:
                data = response.json()
                st.session_state["uploaded_files"][data["filename"]] = data["preview"]
                st.success(f"✅ {uploaded_file.name} uploaded!")
            else:
                st.error(f"Upload failed: {response.text}")

    # Show uploaded docs
    if st.session_state["uploaded_files"]:
        st.markdown("### 📑 Uploaded Documents")
        for fname, preview in st.session_state["uploaded_files"].items():
            short_name = fname.split("_", 1)[-1]  # remove hash prefix
            with st.expander(f"📄 {short_name}"):
                st.write(preview[:300] + "...")

        # Summarizer
        st.markdown("### 📝 Summarize")
        selected_for_summary = st.selectbox(
            "Choose a document to summarize",
            options=list(st.session_state["uploaded_files"].keys()),
            format_func=lambda x: x.split("_", 1)[-1]
        )

        if st.button("📝 Summarize This Document"):
            with st.spinner("Generating summary..."):
                ok, res = post_with_error_handling(
                    SUMMARY_URL, json_payload={"filename": selected_for_summary}
                )
            if not ok:
                st.error(res)
            elif res.status_code == 200:
                summary = res.json().get("summary", "No summary found")
                st.markdown("#### 📋 Summary")
                st.info(summary)
            else:
                st.error(f"Error: {res.text}")

        # Clear all button
        if st.button("🗑️ Clear All Documents"):
            st.session_state["uploaded_files"] = {}
            st.session_state["chat_history"] = []
            st.rerun()

# ─────────────────────────────
# RIGHT → Chat Interface
# ─────────────────────────────
with col2:
    st.subheader("💬 Step 2: Chat with Your Documents")

    # Show chat history
    if st.session_state["chat_history"]:
        for chat in st.session_state["chat_history"]:
            with st.chat_message("user"):
                st.write(chat["question"])
            with st.chat_message("assistant"):
                st.write(chat["answer"])
                if chat.get("sources"):
                    clean_sources = [s.split("_", 1)[-1] for s in chat["sources"]]
                    st.caption(f"📌 Sources: {', '.join(clean_sources)}")

    # Input area
    if not st.session_state["uploaded_files"]:
        st.info("👈 Please upload at least one PDF first.")
    else:
        question = st.chat_input("Ask a question about your documents...")

        if question:
            filenames = list(st.session_state["uploaded_files"].keys())

            # Build conversation context for memory
            context_history = ""
            if st.session_state["chat_history"]:
                last_3 = st.session_state["chat_history"][-3:]  # last 3 exchanges
                for c in last_3:
                    context_history += f"Q: {c['question']}\nA: {c['answer']}\n\n"

            # Add context to question if history exists
            full_question = question
            if context_history:
                full_question = f"Previous conversation:\n{context_history}\nNew question: {question}"

            payload = {
                "filenames": filenames,
                "question": full_question
            }

            with st.spinner("Thinking..."):
                ok, res = post_with_error_handling(ASK_URL, json_payload=payload)

            if not ok:
                st.error(res)
            elif res.status_code == 200:
                data = res.json()
                answer = data.get("answer", "No answer found")
                sources = data.get("sources", [])

                # Save to chat history
                st.session_state["chat_history"].append({
                    "question": question,  # original question (not with context)
                    "answer": answer,
                    "sources": sources
                })
                st.rerun()
            else:
                st.error(f"Error: {res.text}")

    # Clear chat button
    if st.session_state["chat_history"]:
        if st.button("🗑️ Clear Chat"):
            st.session_state["chat_history"] = []
            st.rerun()