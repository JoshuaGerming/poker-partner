Poker Assistant (Texas Hold’em)
An interactive tool and command-line helper that gives preflop and postflop advice using position, hand strength, draw detection, and pot odds.

Prerequisites
• Python 3.8+ installed
• Git

Installation

Clone the repo:
git clone https://github.com/JoshuaGerming/poker-partner.git
cd poker-partner/poker-assistant

Create & activate a venv:
– Windows (PowerShell):
py -3 -m venv venv
.\venv\Scripts\Activate.ps1
– macOS/Linux:
python3 -m venv venv
source venv/bin/activate

Install dependencies:
pip install --upgrade pip
pip install -r requirements.txt

Usage

Command-line
• Preflop advice:
python assistant.py --hole Ah Kd --pos CO
• Postflop advice:
python assistant.py --hole Ah Kd --board 2c 7d Th --pos CO --pot 100 --to-call 20

Streamlit UI
• Run: streamlit run app.py
• Enter your hole cards (and board if you like), click Simulate Flop to deal a random flop, then Get Recommendation.
• The session history of hands & opponent profiles appears below.

Development
• Preflop chart is in charts/preflop_chart.csv (169 hands)
• Tests live in tests/; run with python -m pytest -q
