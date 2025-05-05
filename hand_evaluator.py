# hand_evaluator.py
from treys import Card, Evaluator

evaluator = Evaluator()

def evaluate_hand(hole_cards: list[str], board_cards: list[str]) -> tuple[int, str]:
    """
    hole_cards: e.g. ["Ah", "Kd"]
    board_cards: e.g. ["2c", "7d", "Th", "9h", "3s"]
    Returns (score, rank_name). Lower score = stronger hand.
    """
    hole = [Card.new(c) for c in hole_cards]
    board = [Card.new(c) for c in board_cards]
    score = evaluator.evaluate(board, hole)
    rank_class = evaluator.get_rank_class(score)
    rank_name = evaluator.class_to_string(rank_class)
    return score, rank_name

if __name__ == "__main__":
    # quick smoke test
    s, r = evaluate_hand(["Ah", "Kd"], ["2c", "7d", "Th"])
    print(f"Score: {s}   Rank: {r}")
