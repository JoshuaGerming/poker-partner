# preflop.py
import csv
from typing import Literal

# Define your positions here
Position = Literal["UTG", "MP", "CO", "BTN", "SB", "BB"]

class PreflopChart:
    def __init__(self, chart_path: str = "charts/preflop_chart.csv"):
        self.chart: dict[str, dict[Position, str]] = {}
        with open(chart_path, newline="") as f:
            reader = csv.DictReader(f)
            for row in reader:
                hand = row["hand"].upper()
                # build a sub-dict for each position
                self.chart[hand] = {
                    pos: row[pos].lower() for pos in reader.fieldnames if pos != "hand"
                }

    def recommend(self, hand: str, pos: Position) -> str:
        """
        hand: e.g. "AKs", "QJo", "77"
        pos: one of "UTG","MP","CO","BTN","SB","BB"
        returns: 'fold', 'call', 'raise', etc.
        """
        hand = hand.upper()
        return self.chart.get(hand, {}).get(pos, "fold")
