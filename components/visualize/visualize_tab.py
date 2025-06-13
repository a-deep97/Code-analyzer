# tabs/visualize_tab.py

import streamlit as st
from common.github_fetcher import clone_github_repo
from components.visualize.code_structure_viewer import show_code_structure

def visualize_code_tab():
    st.subheader("📊 Visualize Codebase Structure")
    repo_url = st.text_input("Enter GitHub Repository URL for Visualization", key="visualize_url")

    if st.button("Visualize Codebase", key="visualize_button"):
        if repo_url.strip():
            try:
                with st.spinner("Cloning repository..."):
                    repo_path = clone_github_repo(repo_url.strip())
                show_code_structure(repo_path)
            except Exception as e:
                st.error(f"Error: {e}")
        else:
            st.warning("Please enter a GitHub repository URL.")
