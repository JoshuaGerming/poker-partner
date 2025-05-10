import streamlit as st
import pandas as pd
import random

from preflop import PreflopChart
from postflop import postflop_decision
from opponent_simulator import simulate_opponent

# ——— Streamlit page config ———
st.set_page_config(page_title="Texas Hold'em Assistant", layout="centered")
st.title("🂡 Poker Assistant (Texas Hold'em)")

# ——— Session History ———
if 'history' not in st.session_state:
    st.session_state.history = []

# ——— Initialize full deck for simulation ———
if 'full_deck' not in st.session_state:
    ranks = "23456789TJQKA"
    suits = "hdcs"
    st.session_state.full_deck = [r + s for r in ranks for s in suits]

# ——— Helper to normalize card strings ———
def normalize_card(card: str) -> str:
    """
    Turn inputs like '10d' or 'Td' into 'Td', 'ah' or 'AH' into 'Ah'.
    """
    raw_rank = card[:-1]
    suit = card[-1].lower()
    # map '10' to 'T'
    if raw_rank == "10":
        rank = "T"
    else:
        rank = raw_rank.upper()
    return rank + suit

# ——— User Inputs ———
hole_input = st.text_input("Hole Cards (e.g. 'Ah Kd')", "Ah Kd", key="hole")
board_input = st.text_input("Board Cards (e.g. '2c 7d Th')", "", key="board")

col1, col2 = st.columns(2)
with col1:
    pot = st.number_input("Pot Size", min_value=0, value=100, step=1, key="pot")
with col2:
    to_call = st.number_input("Amount to Call", min_value=0, value=10, step=1, key="to_call")

position = st.selectbox("Table Position", ["UTG","MP","CO","BTN","SB","BB"], key="pos")

# ——— Simulate Flop Button ———
def simulate_flop():
    hole_cards = [normalize_card(c) for c in st.session_state.hole.split()]
    available = [c for c in st.session_state.full_deck if c not in hole_cards]
    flop = random.sample(available, 3)
    st.session_state.board = " ".join(flop)

st.button("Simulate Flop", on_click=simulate_flop)

# ——— Get Recommendation ———
if st.button("Get Recommendation"):
    try:
        hole  = [normalize_card(c) for c in hole_input.split()]
        board = [normalize_card(c) for c in board_input.split()] if board_input else []
    except:
        st.error("Invalid card format. Use e.g. Ah, Kd, 10h → Th.")
        st.stop()

    opp_profile = simulate_opponent()

    # Preflop branch
    if not board:
        r1, r2 = hole[0][0], hole[1][0]
        suited = (hole[0][1] == hole[1][1])
        rank_order = "23456789TJQKA"
        if r1 == r2:
            code = r1 + r2
        else:
            if rank_order.index(r1) > rank_order.index(r2):
                high, low = r1, r2
            else:
                high, low = r2, r1
            code = f"{high}{low}" + ("s" if suited else "o")
        action = PreflopChart().recommend(code, position).upper()
        st.success(f"Preflop: {code} @ {position} → {action}")

    # Postflop branch
    else:
        action = postflop_decision(hole, board, pot, to_call, position).upper()
        st.success(f"Postflop → Suggested: {action}")
        st.json(opp_profile)

    # Record session
    st.session_state.history.append({
        "hole":   " ".join(hole),
        "board":  " ".join(board) if board else "(preflop)",
        "pos":    position,
        "pot":    pot,
        "to_call":to_call,
        "action": action,
        "opponent": opp_profile
    })

# ——— Session History Table ———
st.subheader("Session History")
if st.session_state.history:
    df_hist = pd.DataFrame(st.session_state.history)
    st.dataframe(df_hist)
else:
    st.write("No hands yet—click Get Recommendation to start!")
