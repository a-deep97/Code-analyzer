# visualizer/code_structure_viewer.py

import streamlit as st
from visualizer.dependency_graph import build_dependency_graph
from visualizer.code_structure import build_code_structure
from visualizer.visualizer import render_dependency_graph, render_code_structure

def show_code_structure(repo_path: str):
    st.subheader("Dependency Graph")
    with st.spinner("Building dependency graph..."):
        graph = build_dependency_graph(repo_path)
        render_dependency_graph(graph)

    st.subheader("Code Structure Tree")
    with st.spinner("Building code structure tree..."):
        tree = build_code_structure(repo_path)
        render_code_structure(tree)
