# opponent_simulator.py
import random

def simulate_opponent() -> dict:
    """
    Simulate a simple opponent profile.

    Returns:
        dict: {
            'tightness': float,  # how selective the opponent is preflop (VPIP)
            'aggression': float  # how aggressively they bet/raise when entering a pot
        }

    """
    # Tightness: fraction of hands the opponent voluntarily plays preflop
    #  - 0.0 means plays 0% of possible hands (ultra-tight)
    #  - 1.0 means plays 100% of possible hands (ultra-loose)
    tightness = random.uniform(0.0, 1.0)

    # Aggression: ratio of bets/raises to total actions (bets+raises+calls)
    #  - 0.0 means always calls (passive)
    #  - 1.0 means always bets/raises (very aggressive)
    aggression = random.uniform(0.0, 1.0)

    # Round to two decimals for readability
    return {
        'tightness': round(tightness, 2),
        'aggression': round(aggression, 2),
    }
