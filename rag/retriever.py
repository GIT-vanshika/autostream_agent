import os
from typing import List
from langchain_community.vectorstores import FAISS
from langchain_google_genai import GoogleGenerativeAIEmbeddings

from config import VECTORSTORE_PATH, EMBEDDING_MODEL, GOOGLE_API_KEY, TOP_K_DOCS

os.environ["GOOGLE_API_KEY"] = GOOGLE_API_KEY


class AutoStreamRetriever:
    def __init__(self):
        embeddings = GoogleGenerativeAIEmbeddings(model=EMBEDDING_MODEL)
        self.vectordb = FAISS.load_local(
            VECTORSTORE_PATH,
            embeddings,
            allow_dangerous_deserialization=True,
        )

    def get_relevant_docs(self, query: str) -> List[str]:
        docs = self.vectordb.similarity_search(query, k=TOP_K_DOCS)
        return [d.page_content for d in docs]
