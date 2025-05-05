from preflop import PreflopChart

chart = PreflopChart()

def test_aa_utg_is_raise():
    assert chart.recommend("AA", "UTG") == "raise"

def test_72o_all_positions_fold():
    for pos in ["UTG","MP","CO","BTN","SB","BB"]:
        assert chart.recommend("72o", pos) == "fold"
