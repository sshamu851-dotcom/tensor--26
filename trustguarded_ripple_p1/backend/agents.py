from langgraph.graph import StateGraph, END
from backend.state import AgentState
from langchain_community.llms import Ollama

llm = Ollama(model="tinyllama")
# --- NODE 1: Planner ---
def planner(state: AgentState) -> AgentState:
    plan = llm.invoke(f"Plan how to complete this task: {state['task']}")
    state["decisions"].append(f"[PLANNER]: {plan}")
    state["total_calls"] += 1
    return state

# --- NODE 2: Guardian ---
BLOCKED_PATTERNS = ["delete", "rm -rf", "hack", "inject", "drop table", "exec("]

def guardian(state: AgentState) -> AgentState:
    last_decision = state["decisions"][-1].lower()
    is_malicious = any(p in last_decision for p in BLOCKED_PATTERNS)
    
    if is_malicious:
        state["blocked"] = True
        state["decisions"].append("[GUARDIAN]: ⛔ BLOCKED — violated safety rule")
    else:
        state["blocked"] = False
        state["safe_calls"] += 1
        state["decisions"].append("[GUARDIAN]: ✅ Validated")
    
    state["total_calls"] += 1
    state["trust_velocity"] = state["safe_calls"] / state["total_calls"]
    return state

# --- NODE 3: Coder ---
def coder(state: AgentState) -> AgentState:
    if state["blocked"]:
        return state  # skip if blocked
    code = llm.invoke(f"Write clean code for: {state['task']}")
    state["decisions"].append(f"[CODER]: {code[:200]}")  # truncate for speed
    state["total_calls"] += 1
    state["safe_calls"] += 1
    return state

# --- NODE 4: Reviewer ---
def reviewer(state: AgentState) -> AgentState:
    if state["blocked"]:
        state["output"] = "❌ Task blocked by Guardian."
        return state
    review = llm.invoke(f"Review this for correctness: {state['decisions'][-1]}")
    state["decisions"].append(f"[REVIEWER]: {review[:200]}")
    state["output"] = "✅ Task completed successfully."
    state["total_calls"] += 1
    state["safe_calls"] += 1
    state["trust_velocity"] = state["safe_calls"] / state["total_calls"]
    return state

# --- ROUTING: Skip Coder/Reviewer if blocked ---
def route_after_guardian(state: AgentState):
    return "reviewer" if state["blocked"] else "coder"

# --- BUILD GRAPH ---
graph = StateGraph(AgentState)
graph.add_node("planner", planner)
graph.add_node("guardian", guardian)
graph.add_node("coder", coder)
graph.add_node("reviewer", reviewer)

graph.set_entry_point("planner")
graph.add_edge("planner", "guardian")
graph.add_conditional_edges("guardian", route_after_guardian, {
    "coder": "coder",
    "reviewer": "reviewer"
})
graph.add_edge("coder", "reviewer")
graph.add_edge("reviewer", END)

app = graph.compile()