# analyzer/code_complexity_viewer.py

import streamlit as st
from analyzer.file_scanner import find_python_files
from analyzer.metrics import get_cyclomatic_complexity

def show_complexity_analysis(repo_path: str):
    st.subheader("Cyclomatic Complexity Results")
    py_files = find_python_files(repo_path)

    if not py_files:
        st.warning("No Python files found.")
        return

    for file_path in py_files:
        with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
            code = f.read()

        st.markdown(f"#### `{file_path.replace(repo_path + '/', '')}`")
        try:
            complexity = get_cyclomatic_complexity(code)
            if complexity:
                for func in complexity:
                    st.markdown(f"""
                    - **Function**: `{func['name']}`
                    - **Line**: `{func['lineno']}`
                    - **Complexity**: `{func['complexity']}`
                    """)
            else:
                st.info("No functions found in this file.")
        except Exception as e:
            st.error(f"Error analyzing file: {e}")
