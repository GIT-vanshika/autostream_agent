import os
from dotenv import load_dotenv

load_dotenv()

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

KB_PATH = "data/kb_autostream.md"
VECTORSTORE_PATH = "data/faiss_index_autostream"

EMBEDDING_MODEL = "models/text-embedding-004"
RAG_CHUNK_SIZE = 500
RAG_CHUNK_OVERLAP = 50
TOP_K_DOCS = 4
