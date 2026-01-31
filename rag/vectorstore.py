from langchain_community.vectorstores import FAISS
from .embeddings import get_embeddings

def create_vector_store(chunks):
    """
    Creates an in-memory FAISS vector store from document chunks
    using OpenAI embeddings (1536 dimensions).
    """
    if not chunks:
        raise ValueError("No document chunks provided to create vector store.")

    embeddings = get_embeddings()
    vector_store = FAISS.from_documents(chunks, embeddings)
    return vector_store
