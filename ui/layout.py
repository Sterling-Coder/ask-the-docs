import streamlit as st

def setup_page():
    st.set_page_config(page_title="Ask the Docs", layout="wide")
    st.title("📄 Ask the Docs")
    st.markdown("Upload PDF or TXT files and ask questions about their content.")

    st.markdown("""
    <style>
        /* Import Inter font */
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600&display=swap');

        html, body, [class*="css"] {
            font-family: 'Inter', sans-serif;
            color: #333;
        }

        /* Title with Gradient */
        /* Title with Premium Color */
        h1 {
            color: #1A2980 !important;
            font-weight: 800 !important;
            letter-spacing: -0.5px;
        }

        /* Custom Tabs */
        .stTabs [data-baseweb="tab-list"] {
            gap: 20px;
        }

        .stTabs [data-baseweb="tab"] {
            height: 48px;
            white-space: pre-wrap;
            border-radius: 4px;
            font-size: 16px;
            font-weight: 600;
        }

        .stTabs [aria-selected="true"] {
            color: #1A2980 !important;
            border-bottom-color: #1A2980 !important;
            background-color: rgba(26, 41, 128, 0.05);
        }

        /* Input Fields */
        /* Input Fields */
        .stTextInput input, .stChatInputContainer textarea {
            border-radius: 8px !important;
            border: 1px solid #ddd;
            padding-left: 12px;
            padding-top: 8px;
            padding-bottom: 8px;
        }

        /* Hide "Press Enter to apply" hint to reduce clutter */
        [data-testid="InputInstructions"] {
            display: none !important;
        }
        
        .stTextInput input:focus, .stChatInputContainer textarea:focus {
            border-color: #26D0CE !important;
            box-shadow: 0 0 0 1px #26D0CE;
        }

        /* Buttons */
        .stButton button {
            border-radius: 8px;
            font-weight: 600;
            transition: all 0.3s ease;
        }

        /* History Expanders */
        .streamlit-expanderHeader {
            background-color: #f8f9fa;
            border-radius: 6px;
            font-weight: 500;
        }

        /* Remove default padding */
        .main .block-container {
            padding-top: 2rem;
            padding-bottom: 2rem;
        }
    </style>
    """, unsafe_allow_html=True)
