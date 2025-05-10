# postflop.py

from typing import List
from hand_evaluator import evaluate_hand
from opponent_simulator import simulate_opponent

# --- Constants & Helpers ---

# Treys worst 7-card hand score
MAX_SCORE = 7462

def normalize_strength(score: int) -> float:
    """
    Map Treys score to [0.0 (worst) … 1.0 (best)].
    """
    return (MAX_SCORE - score) / (MAX_SCORE - 1)

# Numeric values for table positions
POSITION_VALUE = {
    "UTG": 0.0,
    "MP":  0.2,
    "CO":  0.6,
    "BTN": 1.0,
    "SB":  0.4,
    "BB":  0.3,
}

def has_flush_draw(hole: List[str], board: List[str]) -> bool:
    suits = [c[-1] for c in hole + board]
    return any(suits.count(s) == 4 for s in "hdcs")

def has_straight_draw(hole: List[str], board: List[str]) -> bool:
    # Map ranks '2'..'A' → 2..14
    RANK_MAP = {r: i+2 for i,r in enumerate("23456789TJQKA")}
    vals = {RANK_MAP[c[0]] for c in hole + board}
    for low in range(2, 11):
        window = set(range(low, low + 5))
        if len(window & vals) == 4:
            return True
    return False

def pot_odds(pot: int, to_call: int) -> float:
    if to_call <= 0:
        return 0.0
    return to_call / (pot + to_call)

# --- Heuristic Weights & Thresholds ---

W_STRENGTH    =  1.0   # how much pure hand strength matters
W_DRAW        =  0.3   # bonus for having a draw
W_POT_ODDS    = -0.1   # penalty for expensive calls
W_POSITION    =  0.2   # bonus for late position
W_TIGHTNESS   = -0.1   # prefer loose opponents
W_AGGRESSION  =  0.1   # prefer bluffing passive opponents

FOLD_THRESHOLD  = 0.1
RAISE_THRESHOLD = 0.6

# --- Core Heuristic Evaluator ---

def evaluate_state(
    hole: List[str],
    board: List[str],
    pot: int,
    to_call: int,
    position: str,
    opp_profile: dict
) -> float:
    # 1) Normalize hand strength
    score, _ = evaluate_hand(hole, board)
    s_norm   = normalize_strength(score)

    # 2) Draw bonus
    draw_flag = 1.0 if (has_flush_draw(hole, board) or has_straight_draw(hole, board)) else 0.0

    # 3) Pot‐odds cost
    odds     = pot_odds(pot, to_call)

    # 4) Table position
    pos_val  = POSITION_VALUE.get(position, 0.0)

    # 5) Opponent profile
    tight    = opp_profile["tightness"]
    aggr     = opp_profile["aggression"]

    # Weighted sum
    E = (
        W_STRENGTH   * s_norm
      + W_DRAW       * draw_flag
      + W_POT_ODDS   * odds
      + W_POSITION   * pos_val
      + W_TIGHTNESS  * tight
      + W_AGGRESSION * aggr
    )
    return E

def postflop_decision(
    hole: List[str],
    board: List[str],
    pot: int,
    to_call: int,
    position: str
) -> str:
    """
    Heuristic‐based postflop decision:
      - Raise if evaluation ≥ RAISE_THRESHOLD
      - Call  if ≥ FOLD_THRESHOLD
      - Else check/fold
    """
    opp = simulate_opponent()
    score = evaluate_state(hole, board, pot, to_call, position, opp)

    if score >= RAISE_THRESHOLD:
        return "raise"
    elif score >= FOLD_THRESHOLD:
        return "call"
    else:
        return "check/fold"
