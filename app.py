import streamlit as st
from dotenv import load_dotenv
import ui.layout
import ui.sidebar
import ui.documents_tab
import ui.chat_tab
import ui.history_tab

load_dotenv()

ui.layout.setup_page()
ui.sidebar.render_sidebar()

if "rag_chain" not in st.session_state:
    st.session_state.rag_chain = None
if "vector_store" not in st.session_state:
    st.session_state.vector_store = None
if "processed_files" not in st.session_state:
    st.session_state.processed_files = []

tab1, tab2, tab3 = st.tabs(["💬 Chat", "📂 Documents", "📜 History"])

with tab1:
    ui.chat_tab.render_chat_tab()

with tab2:
    ui.documents_tab.render_documents_tab()

with tab3:
    ui.history_tab.render_history_tab()
