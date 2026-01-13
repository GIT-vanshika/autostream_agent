import os
from langchain_community.vectorstores import FAISS
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import TextLoader
from langchain_google_genai import GoogleGenerativeAIEmbeddings

from config import (
    KB_PATH,
    VECTORSTORE_PATH,
    EMBEDDING_MODEL,
    RAG_CHUNK_SIZE,
    RAG_CHUNK_OVERLAP,
    GOOGLE_API_KEY,
)

os.environ["GOOGLE_API_KEY"] = GOOGLE_API_KEY


def build_vectorstore():
    loader = TextLoader(KB_PATH, encoding="utf-8")
    docs = loader.load()
    print("Loaded docs:", len(docs))

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=RAG_CHUNK_SIZE,
        chunk_overlap=RAG_CHUNK_OVERLAP,
    )
    chunks = splitter.split_documents(docs)
    print("Chunks:", len(chunks))

    embeddings = GoogleGenerativeAIEmbeddings(model=EMBEDDING_MODEL)
    vectordb = FAISS.from_documents(chunks, embeddings)

    os.makedirs(VECTORSTORE_PATH, exist_ok=True)
    vectordb.save_local(VECTORSTORE_PATH)
    print(f"FAISS index saved to {VECTORSTORE_PATH}")

if __name__ == "__main__":
    build_vectorstore()
