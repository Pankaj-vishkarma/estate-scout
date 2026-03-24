from app.graph.agent_graph import run_agent_graph


def run_agent(query: str, user_id: str):  # ✅ user_id added
    print(f"[Agent] Running LangGraph pipeline for query: {query}")

    try:
        # ✅ pass user_id to graph
        properties = run_agent_graph(query, user_id=user_id)

        print(f"[Agent] Completed. Total properties: {len(properties)}")

        return properties

    except Exception as e:
        print(f"[Agent ERROR]: {e}")
        return []
