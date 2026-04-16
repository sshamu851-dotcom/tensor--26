def compute_trust_velocity(trust_log: list) -> float:
    if not trust_log:
        return 0.0
    safe = sum(1 for e in trust_log if e["safe"])
    return round(safe / len(trust_log), 4)