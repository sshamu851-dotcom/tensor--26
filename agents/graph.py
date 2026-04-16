from langgraph.graph import StateGraph, END
from typing import TypedDict, List

class AgentState(TypedDict):
    task: str
    plan: str
    code: str
    review: str
    shadow_explanation: str
    blocked: bool
    trust_log: List[dict]

def planner(state):
    state["plan"] = f"[Planner] Plan for: {state['task']}"
    state["trust_log"].append({"agent": "planner", "safe": True})
    return state

def guardian(state):
    BLOCKED_PATTERNS = ["delete", "rm -rf", "drop table", "hack", "kill", "sudo rm", "format", "wipe"]
    is_dangerous = any(p in state["task"].lower() for p in BLOCKED_PATTERNS)
    if is_dangerous:
        state["blocked"] = True
        state["shadow_explanation"] = f"[Guardian BLOCKED] Dangerous pattern in: '{state['task']}'"
        state["trust_log"].append({"agent": "guardian", "safe": False})
    else:
        state["blocked"] = False
        state["trust_log"].append({"agent": "guardian", "safe": True})
    return state

def coder(state):
    if state["blocked"]:
        state["code"] = ""
        return state
    state["code"] = f"# Code for: {state['plan']}\nprint('task complete')"
    state["trust_log"].append({"agent": "coder", "safe": True})
    return state

def reviewer(state):
    if state["blocked"] or not state["code"]:
        return state
    state["review"] = "[Reviewer] Code approved."
    state["trust_log"].append({"agent": "reviewer", "safe": True})
    return state

def route_after_guardian(state):
    return END if state["blocked"] else "coder"

def build_graph():
    graph = StateGraph(AgentState)
    graph.add_node("planner", planner)
    graph.add_node("guardian", guardian)
    graph.add_node("coder", coder)
    graph.add_node("reviewer", reviewer)
    graph.set_entry_point("planner")
    graph.add_edge("planner", "guardian")
    graph.add_conditional_edges("guardian", route_after_guardian, {"coder": "coder", END: END})
    graph.add_edge("coder", "reviewer")
    graph.add_edge("reviewer", END)
    return graph.compile()