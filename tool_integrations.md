## Tool Integrations — TrustGuarded Ripple

### Agent Framework
- **LangGraph** — 4-node stateful graph (Planner→Guardian→Coder→Reviewer)
  - Free OSS, unlimited local usage
  - Used by: Member A

### LLM Inference
- **Groq API** (llama3-8b-8192) — Shadow agent explanations
  - Free tier, ~800 tokens/sec inference
  - Used by: Member C (shadow_agent.py)
- **Ollama** — Local LLM fallback for offline use
  - Used by: Member A (backup)

### Visualization
- **Pyvis** — Interactive agent trust graph
  - Used by: Member B (frontend)
- **Plotly** — Trust Velocity gauge + metrics
  - Used by: Member B (frontend)

### Observability
- **LangSmith** — Agent decision trace logging
  - Free tier, full trace visibility
  - Used by: Member A

### Collaboration
- **GitHub** — Version control, branch per member
- **Notion** — Phase checklist + bug log
- **ngrok** — Backend tunnel for B and C

### API Calls Summary
| Tool | Calls/Phase | Cost |
|------|-------------|------|
| Groq API | ~500 (benchmark) | Free |
| Ollama | Unlimited | Free |
| LangSmith | All traces | Free tier |