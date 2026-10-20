"""Level 5: Deployment and safety: checkpoint. Implement the contracts in README.md."""

def reset(state):
    """Explicitly clear the simulated fault latch and timestamp history."""
    raise NotImplementedError("Implement reset")

def step(state, predict, features, sample_time_s, now_s, latency_s, max_age_s=0.1, budget_s=0.01, input_limit=10.0):
    """Simulated latched monitor; latency_s is injected, never a real guarantee."""
    raise NotImplementedError("Implement step")

