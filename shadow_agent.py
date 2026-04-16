# shadow_agent.py
# Member C — Shadow LLM that explains every agent decision

from groq import Groq  # or use Ollama if Groq isn't set up yet

client = Groq(api_key="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")
# Get free API key at: https://console.groq.com

def shadow_explain(decision: str) -> str:
    """
    Takes an agent's decision as input.
    Returns a plain-English explanation.
    """
    prompt = f"Explain this AI agent decision in simple terms: {decision}"
    
    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",  # Free on Groq
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content

# Quick test
if __name__ == "__main__":
    test_decision = "Planner decided to generate a Python function for sorting a list"
    explanation = shadow_explain(test_decision)
    print("Shadow says:", explanation)