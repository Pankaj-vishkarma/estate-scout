from typing import TypedDict, List, Dict, Any
from langgraph.graph import StateGraph, END

from app.services.scout_service import scout_properties
from app.services.inspector_service import inspect_property
from app.services.broker_service import create_property_files
from app.services.crm_service import save_property
from app.services.memory_service import save_user_preference


# 🔥 STATE
class AgentState(TypedDict):
    query: str
    properties: List[Dict[str, Any]]


# 🔥 NODE 1: Scout
def scout_node(state: AgentState):
    print("[Graph] Scout Node")

    save_user_preference(state["query"])

    properties = scout_properties(state["query"])

    return {"properties": properties}


# 🔥 NODE 2: Inspector
def inspector_node(state: AgentState):
    print("[Graph] Inspector Node")

    properties = state["properties"]

    for index, prop in enumerate(properties):
        screenshot_path = inspect_property(prop["address"], index)

        if screenshot_path.startswith("data/"):
            prop["image"] = f"/{screenshot_path}"
        else:
            prop["image"] = screenshot_path

    return {"properties": properties}


# 🔥 NODE 3: Broker
def broker_node(state: AgentState):
    print("[Graph] Broker Node")

    properties = state["properties"]

    for prop in properties:
        create_property_files(prop)

    return {"properties": properties}


# 🔥 NODE 4: CRM
def crm_node(state: AgentState):
    print("[Graph] CRM Node")

    properties = state["properties"]

    for prop in properties:
        save_property(prop)

    return {"properties": properties}


# 🚀 BUILD GRAPH
def build_graph():
    builder = StateGraph(AgentState)

    builder.add_node("scout", scout_node)
    builder.add_node("inspector", inspector_node)
    builder.add_node("broker", broker_node)
    builder.add_node("crm", crm_node)

    builder.set_entry_point("scout")

    builder.add_edge("scout", "inspector")
    builder.add_edge("inspector", "broker")
    builder.add_edge("broker", "crm")
    builder.add_edge("crm", END)

    return builder.compile()


# 🔥 RUN GRAPH
graph = build_graph()


def run_agent_graph(query: str):
    result = graph.invoke({"query": query})

    return result.get("properties", [])
