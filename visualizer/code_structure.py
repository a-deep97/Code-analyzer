import os

def build_code_structure(path, root=True):
    """
    Recursively builds a nested dictionary representing the file/folder structure.
    Useful for visualizing the structure in Streamlit.
    """
    name = os.path.basename(path)
    if not name:
        name = path  # In case of root directory
    
    structure = {"name": name}

    if os.path.isdir(path):
        structure["type"] = "directory"
        structure["children"] = []
        try:
            entries = sorted(os.listdir(path))
            for entry in entries:
                full_path = os.path.join(path, entry)
                if entry.startswith(".") or "__pycache__" in entry:
                    continue  # Skip hidden/system folders
                structure["children"].append(build_code_structure(full_path, root=False))
        except Exception as e:
            structure["error"] = f"Could not read directory: {e}"
    else:
        structure["type"] = "file"

    if root:
        return {"structure": structure}
    return structure
