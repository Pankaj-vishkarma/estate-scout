from app.graph.agent_graph import run_agent_graph


def run_agent(query: str):
    print(f"[Agent] Running LangGraph pipeline for query: {query}")

    try:
        properties = run_agent_graph(query)

        print(f"[Agent] Completed. Total properties: {len(properties)}")

        return properties

    except Exception as e:
        print(f"[Agent ERROR]: {e}")
        return []
