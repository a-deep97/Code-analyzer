from pyvis.network import Network
import streamlit.components.v1 as components
import networkx as nx
import os
import tempfile
import streamlit as st

def render_dependency_graph(data):
    G = nx.DiGraph()
    project_nodes = set(data.get("project_nodes", []))

    for node in data["nodes"]:
        color = "#8fd3f4" if node in project_nodes else "#b2bec3"
        shape = "box" if node in project_nodes else "ellipse"
        G.add_node(node, label=node, color=color, shape=shape)

    edge_colors = {}
    color_palette = ["#e17055", "#00b894", "#6c5ce7", "#fdcb6e", "#0984e3", "#d63031", "#2d3436"]
    color_index = 0

    net = Network(height="600px", width="100%", directed=True, bgcolor="#ffffff", font_color="#2d3436")

    for source, target in data["edges"]:
        if source not in G.nodes:
            G.add_node(source, label=source, color="#b2bec3", shape="ellipse")

        color = edge_colors.get(target)
        if not color:
            color = color_palette[color_index % len(color_palette)]
            edge_colors[target] = color
            color_index += 1

        G.add_edge(target, source, color=color, arrows="to", physics=True)

    net.from_nx(G)

    net.set_options("""
    {
      "layout": {
        "improvedLayout": true
      },
      "physics": {
        "enabled": true,
        "forceAtlas2Based": {
          "gravitationalConstant": -80,
          "centralGravity": 0.01,
          "springLength": 200,
          "springConstant": 0.08
        },
        "solver": "forceAtlas2Based",
        "timestep": 0.35,
        "stabilization": {
          "iterations": 150
        }
      }
    }
    """)

    # Save to a temporary HTML file and load into Streamlit
    with tempfile.NamedTemporaryFile(delete=False, suffix=".html") as tmp_file:
        net.save_graph(tmp_file.name)
        html = open(tmp_file.name, 'r', encoding='utf-8').read()

    # Save to a temporary HTML file
    with tempfile.NamedTemporaryFile(delete=False, suffix=".html") as tmp_file:
        tmp_file_path = tmp_file.name
        net.save_graph(tmp_file_path)
        html = open(tmp_file_path, 'r', encoding='utf-8').read()

    # Inject JS button for download
    download_script = """
    <script type="text/javascript">
    function downloadPNG() {
        const container = document.getElementById("mynetwork");
        html2canvas(container).then(canvas => {
            const link = document.createElement("a");
            link.download = "dependency_graph.png";
            link.href = canvas.toDataURL("image/png");
            link.click();
        });
    }
    </script>
    <button onclick="downloadPNG()" style="margin: 10px 0; padding: 6px 12px; border-radius: 5px; background-color: #374785; color: white;">📸 Save as PNG</button>
    """

    # Inject html2canvas library and our custom button
    html2canvas_script = '<script src="https://html2canvas.hertzen.com/dist/html2canvas.min.js"></script>'
    html = html2canvas_script + download_script + html

    # Embed graph in Streamlit
    with st.expander("🧩 Expand to View Dependency Graph", expanded=True):
        components.html(html, height=650, scrolling=True)

    # Optional: Download full HTML
    st.download_button(
        label="📥 Download Full Graph as HTML",
        data=html,
        file_name="dependency_graph.html",
        mime="text/html"
    )

def build_code_structure(path):
    def build_node(current_path):
        name = os.path.basename(current_path)
        if os.path.isdir(current_path):
            children = []
            try:
                for entry in os.listdir(current_path):
                    full_path = os.path.join(current_path, entry)
                    children.append(build_node(full_path))
            except Exception as e:
                print(f"Skipping directory due to error: {e}")
            return {
                "name": name,
                "type": "directory",
                "children": children
            }
        else:
            return {
                "name": name,
                "type": "file"
            }

    if os.path.exists(path) and os.path.isdir(path):
        return build_node(path)
    else:
        return {
            "name": os.path.basename(path),
            "type": "file"
        }



# analyzer/visualizer.py (append this if not already)

def render_code_structure(node, indent=0):
    if not isinstance(node, dict):
        st.markdown("❌ Invalid node in structure.")
        return

    name = node.get("name", "Unknown")
    node_type = node.get("type", "file")
    spacer = "&nbsp;" * indent * 4

    if node_type == "directory":
        st.markdown(f"{spacer}📁 **{name}**", unsafe_allow_html=True)
        for child in node.get("children", []):
            render_code_structure(child, indent + 1)
    else:
        st.markdown(f"{spacer}📄 {name}", unsafe_allow_html=True)



