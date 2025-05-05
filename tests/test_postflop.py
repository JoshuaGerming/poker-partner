# tests/test_postflop.py

from postflop import postflop_decision

def test_strong_hand_bets():
    """
    A monster hand (pocket aces on a dry board) should bet/raise.
    """
    hole  = ["Ah", "Ad"]
    board = ["2c", "7d", "Th", "9h", "3s"]
    action = postflop_decision(hole, board, pot=100, to_call=10)
    assert action == "bet/raise"

def test_medium_hand_or_draw_calls():
    """
    A flush draw or medium‐strength hand with good pot odds should call.
    """
    hole  = ["Ah", "Kh"]
    board = ["2h", "5h", "9c", "Td"]  # four hearts total => flush draw
    action = postflop_decision(hole, board, pot=100, to_call=10)
    assert action == "call"

def test_weak_hand_checks_or_folds():
    """
    A weak hand on a completed board should check/fold.
    """
    hole  = ["2c", "7d"]
    board = ["As", "Kc", "Qc", "Jd", "Tc"]  # you have nothing here
    action = postflop_decision(hole, board, pot=100, to_call=10)
    assert action == "check/fold"
