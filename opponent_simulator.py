# opponent_simulator.py
import random

def simulate_opponent() -> dict:
    """
    Return a toy profile; later, track real stats.
    """
    return {
        "aggression": round(random.uniform(0.0, 1.0), 2),
        "tightness": round(random.uniform(0.0, 1.0), 2),
    }
