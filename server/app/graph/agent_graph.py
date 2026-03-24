from typing import TypedDict, List, Dict, Any
from langgraph.graph import StateGraph, END

from app.services.scout_service import scout_properties
from app.services.inspector_service import inspect_property
from app.services.broker_service import create_property_files
from app.services.crm_service import save_property
from app.services.memory_service import (
    save_user_preference,
    get_user_preferences,
)


# 🔥 STATE (UPDATED)
class AgentState(TypedDict):
    query: str
    user_id: str  # ✅ NEW
    properties: List[Dict[str, Any]]
    user_preferences: Dict[str, Any]


# 🔥 NODE 0: Memory Check (USER-SPECIFIC)
def memory_node(state: AgentState):
    print("[Graph] Memory Node")

    user_id = state["user_id"]  # ✅ NEW

    # ✅ Save preference (user-specific)
    save_user_preference(state["query"], user_id)

    # ✅ Get preference (user-specific)
    preferences = get_user_preferences(user_id)

    return {"user_preferences": preferences}


# 🔥 NODE 1: Scout (UNCHANGED)
def scout_node(state: AgentState):
    print("[Graph] Scout Node")

    properties = scout_properties(state["query"])

    return {"properties": properties}


# 🔥 NODE 2: Inspector (UNCHANGED)
def inspector_node(state: AgentState):
    print("[Graph] Inspector Node")

    properties = state["properties"]

    for index, prop in enumerate(properties):
        result = inspect_property(prop["address"], index)

        screenshot_path = result.get("street_view")

        if screenshot_path:
            if screenshot_path.startswith("data/"):
                prop["street_view"] = f"/{screenshot_path}"
            else:
                prop["street_view"] = screenshot_path

    return {"properties": properties}


# 🔥 NODE 3: Broker (UNCHANGED)
def broker_node(state: AgentState):
    print("[Graph] Broker Node")

    properties = state["properties"]

    for prop in properties:
        folder_path = create_property_files(prop)
        prop["folder"] = folder_path

    return {"properties": properties}


# 🔥 NODE 4: CRM (UNCHANGED)
def crm_node(state: AgentState):
    print("[Graph] CRM Node")

    properties = state["properties"]

    for prop in properties:
        save_property(prop)

    return {"properties": properties}


# 🚀 BUILD GRAPH
def build_graph():
    builder = StateGraph(AgentState)

    builder.add_node("memory", memory_node)
    builder.add_node("scout", scout_node)
    builder.add_node("inspector", inspector_node)
    builder.add_node("broker", broker_node)
    builder.add_node("crm", crm_node)

    builder.set_entry_point("memory")

    builder.add_edge("memory", "scout")
    builder.add_edge("scout", "inspector")
    builder.add_edge("inspector", "broker")
    builder.add_edge("broker", "crm")
    builder.add_edge("crm", END)

    return builder.compile()


# 🔥 RUN GRAPH (UPDATED)
graph = build_graph()


def run_agent_graph(query: str, user_id: str):  # ✅ UPDATED
    result = graph.invoke(
        {
            "query": query,
            "user_id": user_id,  # ✅ IMPORTANT
        }
    )

    return result.get("properties", [])
