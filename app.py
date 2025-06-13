import streamlit as st
from components.visualize.visualize_tab import visualize_code_tab
from components.analyze.analyze_tab import analyze_code_tab

st.set_page_config(page_title="Code Visualizer", layout="wide", initial_sidebar_state="collapsed")

# 💄 Custom styles
st.markdown("""
    <style>
    .block-container { padding-top: 2rem; }
    .stButton>button {
        background-color: #374785; color: white; border-radius: 8px;
        padding: 0.5rem 1rem; margin-right: 1rem;
    }
    .stButton>button:hover {
        background-color: #24305e; color: #f8e9a1;
    }
    .stTextInput>div>div>input {
        border-radius: 6px; background-color: #edf2f7;
    }
    .css-1v0mbdj { flex-direction: row; }
    </style>
""", unsafe_allow_html=True)

st.title("Code Structure Explorer")
st.markdown("Explore any public GitHub Python project for complexity and architecture insights.")

# Horizontal Tabs
tabs = st.tabs(["📊 Visualize Code", "🧮 Analyze Complexity"])

with tabs[0]:
    visualize_code_tab()

with tabs[1]:
    analyze_code_tab()
