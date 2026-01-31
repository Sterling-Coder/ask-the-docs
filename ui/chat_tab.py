import os
import streamlit as st
from utils.logger import log_question_answer

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
                with st.spinner("Thinking..."):
                    if "how many document" in prompt.lower():
                        files = st.session_state.get("processed_files", [])
                        answer = f"You have uploaded {len(files)} document(s)."
                        
                    elif st.session_state.get("rag_chain") is None:
                        answer = "Please upload documents in the 'Documents' tab first so I can answer your questions!"
                        
                    else:
                        try:
                            response = st.session_state.rag_chain.invoke({"input": prompt})
                            answer = response["answer"]
                            log_question_answer(prompt, answer)
                        except Exception as e:
                            answer = f"Error: {e}"
                
                st.markdown(answer)

        st.session_state.messages.append({"role": "assistant", "content": answer})
