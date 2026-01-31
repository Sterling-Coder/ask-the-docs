import streamlit as st
import os

def render_sidebar():
    with st.sidebar:
        st.header("Settings")
        api_key_input = st.text_input(
            "OpenAI API Key",
            type="password",
            help="Enter your OpenAI API key and press Enter to apply."
        )
        if api_key_input and api_key_input.strip():
            # Only show toast if the key actually changed
            if os.environ.get("OPENAI_API_KEY") != api_key_input.strip():
                os.environ["OPENAI_API_KEY"] = api_key_input.strip()
                st.toast("API Key applied successfully!", icon="✅")

        st.markdown("---")
        st.caption("Ensure you have a valid OpenAI API key.")
