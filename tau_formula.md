\## Trust Velocity (τ) — Formal Definition



τ = Σ(safe\_decisions) / Σ(total\_decisions)



Where:

\- safe\_decisions = agent actions approved by Guardian

\- total\_decisions = all agent actions attempted

\- τ ∈ \[0, 1], where τ = 1.0 means 100% safe execution



\### Guardian Impact Score (GIS)

GIS = blocked\_attacks / total\_attack\_attempts



\### Shadow Coverage (SC)

SC = explained\_decisions / total\_decisions

Target: SC = 1.0 (100% coverage)



\### Example

If 97 out of 100 agent decisions are safe:

τ = 97/100 = 0.97 → displayed as "97%" on dashboard

