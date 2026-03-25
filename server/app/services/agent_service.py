from app.graph.agent_graph import run_agent_graph
import time


def run_agent(query: str, user_id: str):
    try:
        # ✅ Validate input
        if not query or not query.strip():
            print("[Agent] Empty query received")
            return []

        if not user_id:
            print("[Agent] Missing user_id")
            return []

        query = query.strip()

        print(f"[Agent] Running LangGraph pipeline for query: {query}")

        start_time = time.time()

        # ✅ Run graph
        properties = run_agent_graph(query, user_id=user_id)

        duration = round(time.time() - start_time, 2)

        print(f"[Agent] Completed in {duration}s | Properties: {len(properties)}")

        # ✅ Safety check
        if not isinstance(properties, list):
            print("[Agent] Invalid response format")
            return []

        return properties

    except Exception as e:
        print(f"[Agent ERROR]: {e}")
        return []
