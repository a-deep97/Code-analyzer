# tabs/analyze_tab.py

import streamlit as st
from common.github_fetcher import clone_github_repo
from  components.analyze.code_complexity_viewer import show_complexity_analysis

def analyze_code_tab():
    st.subheader("🧮 Analyze Code Complexity")
    repo_url = st.text_input("Enter GitHub Repository URL for Analysis", key="analyze_url")

    if st.button("Analyze Complexity", key="analyze_button"):
        if repo_url.strip():
            try:
                with st.spinner("Cloning repository..."):
                    repo_path = clone_github_repo(repo_url.strip())

                show_complexity_analysis(repo_path)

            except Exception as e:
                st.error(f"Error: {e}")
        else:
            st.warning("Please enter a GitHub repository URL.")
