# postflop.py

from typing import List
from hand_evaluator import evaluate_hand

# map ranks to integers for straight‐draw detection
RANK_MAP = {r: i+2 for i, r in enumerate("23456789TJQKA")}

def has_flush_draw(hole: List[str], board: List[str]) -> bool:
    suits = [c[-1] for c in hole + board]
    return any(suits.count(s) == 4 for s in "hdcs")

def has_straight_draw(hole: List[str], board: List[str]) -> bool:
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

def postflop_decision(
    hole: List[str],
    board: List[str],
    pot: int,
    to_call: int
) -> str:
    """
    1) If your hand “makes” a better category than the board alone (Pair+), bet/raise.
    2) Else if this is flop/turn (len(board)<5) and you have a draw, call if
       pot_odds < 0.25 else check/fold.
    3) Otherwise check/fold.
    """
    # actual hand vs board‐only hand
    score_actual, rank_actual = evaluate_hand(hole, board)

    # build two dummy cards that cannot improve the board
    board_ranks = {c[0] for c in board}
    dummy = []
    for r in "23456789TJQKA":
        if r not in board_ranks:
            dummy.append(r + "h")
        if len(dummy) == 2:
            break

    score_board, rank_board = evaluate_hand(dummy, board)

    # 1) Made the board? (rank changed)
    if rank_actual != rank_board:
        return "bet/raise"

    # 2) Draw logic (only on flop/turn)
    if len(board) < 5:
        if has_flush_draw(hole, board) or has_straight_draw(hole, board):
            return "call" if pot_odds(pot, to_call) < 0.25 else "check/fold"

    # 3) Nothing to do
    return "check/fold"
