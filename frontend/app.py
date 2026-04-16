import streamlit as st
from pyvis.network import Network
import streamlit.components.v1 as components

st.set_page_config(page_title="TrustGuarded Ripple", layout="wide")
st.title("🛡️ TrustGuarded Ripple — Live Agent Monitor")

def build_agent_graph(blocked=False):
    net = Network(height="400px", width="100%", bgcolor="#0a0a0f", font_color="white")

    # 4 agents from architecture
    net.add_node("Planner",  label="🧠 Planner",  color="#00ff88", size=30)
    net.add_node("Guardian", label="🛡️ Guardian", color="#ff3366", size=30)
    net.add_node("Coder",    label="⚙️ Coder",    color="#4488ff", size=30)
    net.add_node("Reviewer", label="✅ Reviewer", color="#aa66ff", size=30)

    # Edges from architecture: Planner→Guardian→Coder→Reviewer
    edge_color = "#ff3366" if blocked else "#00ff88"
    net.add_edge("Planner",  "Guardian", title="decides",   color=edge_color, width=2)
    net.add_edge("Guardian", "Coder",    title="validates", color=edge_color, width=2)
    net.add_edge("Coder",    "Reviewer", title="explains",  color=edge_color, width=2)

    net.save_graph("agent_graph.html")
    with open("agent_graph.html", "r", encoding="utf-8") as f:
        return f.read()
    
# --- Mock state toggle ---
mock_mode = st.selectbox(
    "Simulate agent state (mock):",
    ["Normal flow — green pulse", "Guardian BLOCKED — red pulse"]
)

blocked = mock_mode == "Guardian BLOCKED — red pulse"


# --- 3-panel layout ---
col1, col2, col3 = st.columns([2, 1, 1])

with col1:
    st.subheader("🌐 Agent Network")
    html = build_agent_graph(blocked=blocked)
    components.html(html, height=420)

with col2:
    st.subheader("🔍 Shadow Explanation")
    if blocked:
        st.error("🛑 Guardian blocked: harmful instruction detected")
    else:
        st.success("✅ Normal flow — all agents passing")

with col3:
    st.subheader("📊 Trust Velocity")
    st.metric("τ (Trust Velocity)", "97%" if not blocked else "12%")
    st.metric("Guardian Blocks", "0" if not blocked else "1")