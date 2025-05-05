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

# ——— Initialize deck for simulation ———
if 'full_deck' not in st.session_state:
    ranks = "23456789TJQKA"
    suits = "hdcs"
    st.session_state.full_deck = [r + s for r in ranks for s in suits]

# ——— Helper ———
def normalize_card(card: str) -> str:
    return card[:-1].upper() + card[-1].lower()

# ——— User Inputs ———
hole_input = st.text_input("Hole Cards (e.g. 'Ah Kd')", "Ah Kd", key='hole_input')

# Board input now tied to session state for simulation
def get_board_input_default():
    return st.session_state.get('board_input', '')

board_input = st.text_input(
    "Board Cards (e.g. '2c 7d Th')",
    value=get_board_input_default(),
    key='board_input'
)

col1, col2 = st.columns(2)
with col1:
    pot = st.number_input("Pot Size", min_value=0, value=100, step=1, key='pot')
with col2:
    to_call = st.number_input("Amount to Call", min_value=0, value=10, step=1, key='to_call')

position = st.selectbox(
    "Table Position", ["UTG","MP","CO","BTN","SB","BB"],
    key='position'
)

# ——— Simulate Flop Button ———
def simulate_flop():
    hole_cards = [normalize_card(c) for c in hole_input.split()]
    available = [c for c in st.session_state.full_deck if c not in hole_cards]
    flop = random.sample(available, 3)
    st.session_state.board_input = " ".join(flop)
    # trigger rerun so the text_input updates
    

st.button("Simulate Flop", on_click=simulate_flop)

# ——— Recommendation ———
if st.button("Get Recommendation"):
    # normalize and parse
    try:
        hole = [normalize_card(c) for c in hole_input.split()]
        board = [normalize_card(c) for c in board_input.split()] if board_input else []
    except:
        st.error("Invalid card format. Use e.g. Ah, Kd, 2c.")
        st.stop()

    opp_profile = simulate_opponent()

    # Preflop
    if not board:
        r1, r2 = hole[0][0], hole[1][0]
        suited = hole[0][1] == hole[1][1]
        rank_order = "23456789TJQKA"
        if r1 == r2:
            code = r1 + r2
        else:
            if rank_order.index(r1) > rank_order.index(r2): high, low = r1, r2
            else: high, low = r2, r1
            code = f"{high}{low}" + ("s" if suited else "o")
        action = PreflopChart().recommend(code, position).upper()
        st.success(f"Preflop: {code} @ {position} → {action}")
    # Postflop
    else:
        action = postflop_decision(hole, board, pot, to_call).upper()
        st.success(f"Postflop → Suggested: {action}")
        st.json(opp_profile)

    # record
    st.session_state.history.append({
        "hole":  " ".join(hole),
        "board": " ".join(board) if board else "(preflop)",
        "pos":   position,
        "pot":   pot,
        "to_call": to_call,
        "action":  action,
        "opponent": opp_profile
    })

# ——— Session History Table ———
st.subheader("Session History")
if st.session_state.history:
    st.dataframe(pd.DataFrame(st.session_state.history))
else:
    st.write("No hands yet—click Get Recommendation to start!")
