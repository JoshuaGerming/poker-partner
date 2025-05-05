from hand_evaluator import evaluate_hand

def test_pair_beats_high_card():
    board = ["2c", "7d", "Th", "9h", "3s"]
    score_aa, _ = evaluate_hand(["Ah", "Ad"], board)  # pocket aces
    score_kk, _ = evaluate_hand(["Kh", "Kd"], board)  # pocket kings
    assert score_aa < score_kk
