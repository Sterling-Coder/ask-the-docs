from langchain_openai import OpenAIEmbeddings
import os

def get_embeddings():
    """
    Returns the embedding model to use.
    Assumes OPENAI_API_KEY is set in environment or loaded.
    """
    return OpenAIEmbeddings(model="text-embedding-3-small")