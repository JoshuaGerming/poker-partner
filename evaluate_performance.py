import random
from treys import Card, Evaluator
from postflop import postflop_decision

def estimate_equity(hole, board, trials=2000):
    """
    Monte Carlo estimate of equity vs one random opponent.
    """
    evaluator = Evaluator()
    # build deck of all cards
    ranks = "23456789TJQKA"
    suits = "hdcs"
    deck = [r + s for r in ranks for s in suits]
    # remove known cards
    for c in hole + board:
        deck.remove(c)

    wins = ties = 0
    for _ in range(trials):
        opp = random.sample(deck, 2)
        unseen = [c for c in deck if c not in opp]
        # complete the board
        if len(board) == 3:
            community = board + random.sample(unseen, 2)
        elif len(board) == 4:
            community = board + random.sample(unseen, 1)
        else:
            community = board

        # get scores
        me_score = evaluator.evaluate(
            [Card.new(c) for c in community],
            [Card.new(c) for c in hole]
        )
        opp_score = evaluator.evaluate(
            [Card.new(c) for c in community],
            [Card.new(c) for c in opp]
        )
        if me_score < opp_score:
            wins += 1
        elif me_score == opp_score:
            ties += 1

    return (wins + ties/2) / trials


def performance_test(sample_size=10000):
    """
    Run a quick performance check: accuracy of call/fold vs equity>0.
    """
    positions = ["UTG","MP","CO","BTN","SB","BB"]
    correct = total = 0
    total_ev_loss = 0.0

    for _ in range(sample_size):
        # random hole
        ranks = "23456789TJQKA"
        suits = "hdcs"
        deck = [r + s for r in ranks for s in suits]
        hole = random.sample(deck, 2)
        # random flop
        remaining = [c for c in deck if c not in hole]
        board = random.sample(remaining, 3)
        pos = random.choice(positions)
        pot = 100
        to_call = 20

        rec = postflop_decision(hole, board, pot, to_call, pos)
        e = estimate_equity(hole, board)
        ev_call = e * (pot + to_call) - (1 - e) * to_call
        ev_fold = 0

        # correct if folds when EV_call<=0, or calls/raises when EV_call>0
        is_correct = (ev_call > 0 and rec in ("call","raise")) or (ev_call <= 0 and rec == "check/fold")
        correct += is_correct
        total += 1
        # EV loss: if we called when EV<0 or folded when EV>0
        if rec in ("call","raise") and ev_call <= 0:
            total_ev_loss += -ev_call
        if rec == "check/fold" and ev_call > 0:
            total_ev_loss += ev_call

    accuracy = correct / total
    avg_ev_loss = total_ev_loss / total
    print(f"Accuracy vs call/fold baseline: {accuracy:.2%}")
    print(f"Average EV loss per sample: {avg_ev_loss:.2f}")

if __name__ == "__main__":
    print("Running performance test...\n")
    performance_test(sample_size=100)
