import streamlit as st
import requests

st.set_page_config(
    page_title="PDF QA System",
    page_icon="📄",
    layout="wide",
)

UPLOAD_URL = "http://127.0.0.1:8000/upload-preview"
ASK_URL = "http://127.0.0.1:8000/ask-question"

if "saved_filename" not in st.session_state:
    st.session_state["saved_filename"] = None

st.markdown("<h1 style='text-align:center;'>📄 PDF Question Answering System</h1>", unsafe_allow_html=True)
st.write("")

col1, col2 = st.columns([1, 1])

# -----------------------------
# 📌 LEFT SIDE → Upload PDF
# -----------------------------
with col1:
    st.subheader("Step 1: Upload Your PDF")

    uploaded_file = st.file_uploader("Choose a PDF", type=["pdf"])

    if uploaded_file:
        with st.spinner("Uploading to backend..."):
            files = {"file": (uploaded_file.name, uploaded_file, "application/pdf")}
            response = requests.post(UPLOAD_URL, files=files)

        if response.status_code == 200:
            data = response.json()

            st.success("Preview Loaded!")

            st.session_state["saved_filename"] = data["filename"]

            st.subheader("📌 PDF Preview (300 words)")

            with st.expander("Click to expand preview"):
                st.write(data["preview"])

            st.caption(f"Saved filename: {data['filename']}")
        else:
            st.error(f"Backend Error: {response.text}")

# -----------------------------
# 📌 RIGHT SIDE → Ask Question
# -----------------------------
with col2:
    st.subheader("Step 2: Ask Your Question")

    question = st.text_area("Enter your question", height=120)

    if st.button("Ask"):
        if not st.session_state["saved_filename"]:
            st.error("Please upload a PDF first.")
        elif not question.strip():
            st.error("Please enter a question.")
        else:
            payload = {
                "filename": st.session_state["saved_filename"],
                "question": question
            }
            with st.spinner("Getting answer..."):
                res = requests.post(ASK_URL, json=payload)

            if res.status_code == 200:
                ans = res.json().get("answer", "No answer found")
                st.success("Answer:")
                st.write(ans)
            else:
                st.error(f"Error: {res.text}")
