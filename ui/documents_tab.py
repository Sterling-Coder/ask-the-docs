import streamlit as st
import pandas as pd
from rag.loader import load_and_split_document
from rag.vectorstore import create_vector_store
from rag.qa import get_rag_chain


def render_documents_tab():
    uploaded_files = st.file_uploader(
        "Upload documents",
        type=["pdf", "txt"],
        accept_multiple_files=True
    )

    if uploaded_files:
        current_names = [f.name for f in uploaded_files]
        if "processed_files" not in st.session_state:
             st.session_state.processed_files = []
        processed_names = [f["name"] for f in st.session_state.processed_files]

        if set(current_names) != set(processed_names):
            with st.spinner("Processing documents..."):
                all_chunks = []
                st.session_state.processed_files = []

                for f in uploaded_files:
                    chunks = load_and_split_document(f)
                    all_chunks.extend(chunks)
                    st.session_state.processed_files.append(
                        {"name": f.name, "chunks": len(chunks)}
                    )

                if all_chunks:
                    try:
                        vector_store = create_vector_store(all_chunks)
                        st.session_state.rag_chain = get_rag_chain(vector_store)
                        st.success(f"Processed {len(uploaded_files)} document(s) successfully.")
                    except Exception as e:
                        st.error(f"Error creating vector store: {e}")
                else:
                    st.error("No text extracted.")

    if "processed_files" in st.session_state and st.session_state.processed_files:
        st.dataframe(pd.DataFrame(st.session_state.processed_files))
