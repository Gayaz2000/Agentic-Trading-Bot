import streamlit as st
import requests

BASE_URL = "http://localhost:8000"

st.set_page_config(
    page_title="Stock Market Agentic Chatbot",
    page_icon="💱",
    layout= "centered",
    initial_sidebar_state="expanded"
)

st.title("💰 Stock Market Agentic Chatbot")

with st.sidebar:
    st.header("📑 Upload Documents")
    st.markdown("Upload your  **Stock Market** related PDF or DocX file")
    upload_files = st.file_uploader("Choose files", type=["pdf","docx"], accept_multiple_files=True)

    if st.button("Upload"):
        if not upload_files:
            st.warning("Please upload the file")
        else:
            files = [("files", (f.name, f.read(), f.type)) for f in upload_files]
            with st.spinner("Uploading Files..."):
                response = requests.post(f"{BASE_URL}/upload", files=files)
                if response.status_code == 200:
                    st.warning("File Uploaded Succesfully")
                else:
                    st.error("Falied to Upload..", response.text)

st.header("Ask a Question")

st.markdown("Enter your File")

question = st.text_input("Question", placeholder="e.g: what is a stock in finance")

if st.button("Ask"):
    if not question.strip():
        st.warning("Please enter a question")
    else:
        with st.spinner("Thinking..."):
            payload = {"question": question}
            response = requests.post(f"{BASE_URL}/query", files=files)
            if response.status_code == 200:
                answer = response.json().get("answer", "No answer returned")
                st.markdown("### Answer")
                st.write(answer)
            else:
                st.error("Filed to get answer", response.text)
