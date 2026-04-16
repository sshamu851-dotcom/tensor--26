from typing import TypedDict, List

class AgentState(TypedDict):
    task: str              # current task/command
    decisions: List[str]   # log of each agent's decision
    blocked: bool          # did Guardian block?
    total_calls: int       # total agent calls
    safe_calls: int        # calls that passed Guardian
    trust_velocity: float  # τ = safe_calls / total_calls
    output: str            # final output