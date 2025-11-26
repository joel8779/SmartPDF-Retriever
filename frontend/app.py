import streamlit as st
import requests

st.set_page_config(page_title="SmartPDF Retriever", page_icon="📄", layout="centered")

st.title("📄 SmartPDF Retriever – LLM + RAG PDF Q&A System")

st.write("Upload a PDF and ask questions. Answers are generated locally using Ollama (Llama3).")

# -------------------------------
# PDF Upload Section
# -------------------------------
st.header("📤 Upload PDF")

uploaded_file = st.file_uploader("Choose a PDF file", type=["pdf"])

if uploaded_file is not None:
    with open("temp.pdf", "wb") as f:
        f.write(uploaded_file.getbuffer())

    files = {"file": open("temp.pdf", "rb")}

    st.info("Uploading and processing PDF...")

    try:
        res = requests.post("http://localhost:8000/upload", files=files)
        st.success(f"PDF processed successfully! 🔍 Created {res.json()['chunks']} chunks.")
    except Exception as e:
        st.error("❌ Error connecting to the backend. Make sure FastAPI is running.")
        st.exception(e)

# -------------------------------
# Question Answering Section
# -------------------------------
st.header("❓ Ask Your Question")

question = st.text_input("Enter your question about the PDF:")

if st.button("Get Answer"):
    if not question.strip():
        st.warning("Please enter a question.")
    else:
        try:
            res = requests.get("http://localhost:8000/ask", params={"q": question})
            answer = res.json().get("answer", "No answer returned.")

            st.subheader("🧠 Answer:")
            st.write(answer)

        except Exception as e:
            st.error("❌ Error: Could not get response from backend.")
            st.exception(e)
