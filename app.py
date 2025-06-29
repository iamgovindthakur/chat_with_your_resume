import streamlit as st
from rag_chain import load_rag_chain
import tempfile

st.set_page_config(page_title="📄 Chat with Your Resume", layout="centered")

st.title("📄 Chat with Your Résumé")

# Upload PDF
uploaded_file = st.file_uploader("Upload your résumé (PDF only)", type="pdf")

# Show prompt only if uploaded
if uploaded_file:
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
        tmp.write(uploaded_file.read())
        tmp_path = tmp.name

    with st.spinner("Loading model & indexing your résumé..."):
        try:
            qa_chain = load_rag_chain(tmp_path)
            st.success("Your résumé is ready. Ask me anything ↓")
        except Exception as e:
            st.error(f"❌ Failed to load: {e}")
            st.stop()

    query = st.text_input("Your question:")
    if query:
        with st.spinner("Thinking..."):
            response = qa_chain.invoke(query)
            st.write(response)
else:
    st.info("Please upload a PDF résumé to get started.")
