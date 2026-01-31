import streamlit as st
from utils.logger import get_history

def render_history_tab():
    history = get_history()
    if history:
        for i, row in enumerate(reversed(history)):
            question = row.get("Question", "Unknown Question")
            answer = row.get("Answer", "No answer recorded.")
            timestamp = row.get("Timestamp", "")

            with st.expander(f"📝 {question}"):
                st.markdown(f"**Time:** {timestamp}")
                st.markdown("**Answer:**")
                st.markdown(answer if answer else "_No answer available_")
    else:
        st.info("No history yet.")
