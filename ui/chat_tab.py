import time
import streamlit as st
from utils.logger import log_question_answer

def generate_response_stream(prompt):
    """
    Generator function to stream responses.
    Handles both static responses and RAG chain streaming.
    """
    # 1. Hardcoded logic: Document count
    if "how many document" in prompt.lower():
        files = st.session_state.get("processed_files", [])
        response_text = f"You have uploaded {len(files)} document(s)."
        for word in response_text.split(" "):
            yield word + " "
            time.sleep(0.05)
        return

    # 2. Check if documents assume uploaded
    if st.session_state.get("rag_chain") is None:
        response_text = "Please upload documents in the 'Documents' tab first so I can answer your questions!"
        for word in response_text.split(" "):
            yield word + " "
            time.sleep(0.05)
        return

    # 3. RAG Chain Response
    try:
        # Check if the chain supports streaming (it should)
        # We assume the chain returns chunks with an "answer" key containing deltas
        for chunk in st.session_state.rag_chain.stream({"input": prompt}):
            if "answer" in chunk:
                yield chunk["answer"]
    except Exception as e:
        yield f"Error: {str(e)}"

def render_chat_tab():
    if "messages" not in st.session_state:
        st.session_state.messages = []

    messages_container = st.container(height=600)

    with messages_container:
        for msg in st.session_state.messages:
            with st.chat_message(msg["role"]):
                st.markdown(msg["content"])

    prompt = st.chat_input("Ask a question about your documents...")

    if prompt and prompt.strip():
        st.session_state.messages.append({"role": "user", "content": prompt})

        # Display user message immediately
        with messages_container:
            with st.chat_message("user"):
                st.markdown(prompt)

        # Generate response inside the chat container
        with messages_container:
            with st.chat_message("assistant"):
                # Use st.write_stream for the typewriter effect
                # We can't use st.spinner easily with stream, but the stream itself indicates activity
                answer = st.write_stream(generate_response_stream(prompt))
                
        # Log and save interaction
        if answer:
            # Re-verify if log_question_answer is robust to partials? No, answer is full string here.
            try:
               log_question_answer(prompt, answer)
            except Exception as e:
               print(f"Logging failed: {e}")
            
            st.session_state.messages.append({"role": "assistant", "content": answer})
