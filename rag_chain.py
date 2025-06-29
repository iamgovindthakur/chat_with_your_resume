# rag_chain.py  (LLAMA‑3.1 version)
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_ollama import ChatOllama, OllamaEmbeddings
from langchain_community.vectorstores import Chroma
from langchain.chains import RetrievalQA

MODEL_TAG = "llama3.1:latest"   # ← your local model name

def load_rag_chain(pdf_path: str):
    # 1. Load the PDF
    docs = PyPDFLoader(pdf_path).load()

    # 2. Split into chunks ~500 tokens each
    chunks = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=50
    ).split_documents(docs)

    # 3. Embed chunks with the SAME local model
    embeddings = OllamaEmbeddings(model=MODEL_TAG)
    vectordb = Chroma.from_documents(chunks, embeddings)

    # 4. Local chat model
    llm = ChatOllama(
        model=MODEL_TAG,
        temperature=0.1,
        streaming=True      # nice token‑by‑token effect
    )

    # 5. Retrieval‑augmented QA chain
    return RetrievalQA.from_chain_type(
        llm=llm,
        retriever=vectordb.as_retriever(search_kwargs={"k": 3}),
    )
