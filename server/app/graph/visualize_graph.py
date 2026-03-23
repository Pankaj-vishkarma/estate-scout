from app.graph.agent_graph import graph


def generate_graph_image():
    try:
        # 🔥 Generate Mermaid diagram
        mermaid_code = graph.get_graph().draw_mermaid()

        # Save mermaid file
        with open("graph.mmd", "w") as f:
            f.write(mermaid_code)

        print("✅ Mermaid graph saved as graph.mmd")

    except Exception as e:
        print("❌ Graph generation error:", e)


if __name__ == "__main__":
    generate_graph_image()
