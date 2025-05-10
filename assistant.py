# assistant.py

import sys
import argparse
from hand_evaluator import evaluate_hand
from preflop import PreflopChart
from postflop import postflop_decision
from opponent_simulator import simulate_opponent

def normalize_card(card: str) -> str:
    rank = card[:-1].upper()
    suit = card[-1].lower()
    return rank + suit

def parse_args():
    parser = argparse.ArgumentParser(
        description="Poker Assistant for Texas Hold'em"
    )
    parser.add_argument(
        "--hole", "-H", nargs=2, required=True,
        help="Two hole cards, e.g. Ah Kd"
    )
    parser.add_argument(
        "--board", "-B", nargs="*", default=[],
        help="Board cards, e.g. 2c 7d Th 9h 3s"
    )
    parser.add_argument(
        "--pos", "-P",
        choices=["UTG","MP","CO","BTN","SB","BB"],
        required=True, help="Your table position"
    )
    need_post = "--board" in sys.argv
    parser.add_argument(
        "--pot", type=int, required=need_post,
        help="Current pot size"
    )
    parser.add_argument(
        "--to-call", dest="to_call", type=int, required=need_post,
        help="Amount to call"
    )
    return parser.parse_args()

def main():
    args  = parse_args()
    hole  = [normalize_card(c) for c in args.hole]
    board = [normalize_card(c) for c in args.board]
    pos   = args.pos

    chart = PreflopChart()

    if not board:
        # build code like "AKs" or "72o" by sorting ranks properly
        r1, r2 = hole[0][0], hole[1][0]
        suited = hole[0][1] == hole[1][1]

        # poker rank order from deuce (2) up to ace (A)
        rank_order = "23456789TJQKA"
        if r1 == r2:
            # pocket pair
            code = r1 + r2
        else:
            # pick the higher card first
            if rank_order.index(r1) > rank_order.index(r2):
                high, low = r1, r2
            else:
                high, low = r2, r1
            code = f"{high}{low}" + ("s" if suited else "o")

        action = chart.recommend(code, pos)
        print(f"[ Preflop ] {code} @ {pos} → {action.upper()}")
    else:
        pot     = args.pot
        to_call = args.to_call
        action = postflop_decision(hole, board, pot, to_call, pos).upper()
        opp     = simulate_opponent()

        print(f"[ Postflop ] Board: {board}  Pot: {pot}  To call: {to_call}")
        print(f"Suggested action → {action}")
        print(f"Opponent profile → {opp}")

if __name__ == "__main__":
    main()
