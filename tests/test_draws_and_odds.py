# tests/test_draws_and_odds.py

from postflop import has_flush_draw, has_straight_draw, pot_odds

def test_flush_draw_true():
    # Two hearts in hand + two hearts on board = flush draw
    hole  = ["Ah", "Kh"]
    board = ["2h", "5h", "9c", "Td"]
    assert has_flush_draw(hole, board)

def test_flush_draw_false():
    # Only three hearts total => no draw
    hole  = ["Ah", "Ks"]
    board = ["2h", "5h", "9c", "Td"]
    assert not has_flush_draw(hole, board)

def test_straight_draw_true():
    # 6-7 in hand plus 4-5 on board = open-ended draw
    hole  = ["6d", "7c"]
    board = ["4s", "5h", "9d", "Jc"]
    assert has_straight_draw(hole, board)

def test_straight_draw_false():
    # No 4-card straight window
    hole  = ["2d", "9c"]
    board = ["4s", "5h", "Jd", "Qc"]
    assert not has_straight_draw(hole, board)

def test_pot_odds_zero_to_call():
    assert pot_odds(100, 0) == 0.0

def test_pot_odds_calc():
    # 20 to call into 100 pot => 20/120 ≈ 0.1667
    assert abs(pot_odds(100, 20) - 0.1667) < 1e-3
