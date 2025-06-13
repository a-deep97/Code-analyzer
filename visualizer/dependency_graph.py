import ast
import os

def get_imports_from_file(filepath):
    with open(filepath, "r", encoding="utf-8") as f:
        tree = ast.parse(f.read(), filename=filepath)
    imports = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            imports.extend([n.name.split('.')[0] for n in node.names])
        elif isinstance(node, ast.ImportFrom):
            if node.module:
                imports.append(node.module.split('.')[0])
    return imports

def build_dependency_graph(repo_path):
    edges = []
    project_nodes = set()
    external_nodes = set()

    for root, _, files in os.walk(repo_path):
        for file in files:
            if file.endswith(".py"):
                full_path = os.path.join(root, file)
                module_name = os.path.relpath(full_path, repo_path).replace("\\", "/")
                project_nodes.add(module_name)

                imports = get_imports_from_file(full_path)
                for imp in imports:
                    edges.append((imp, module_name))
                    external_nodes.add(imp)

    all_nodes = project_nodes.union(external_nodes)

    return {
        "nodes": list(all_nodes),
        "project_nodes": list(project_nodes),
        "edges": edges
    }
