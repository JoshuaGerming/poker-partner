# Poker Assistant (Texas Hold'em)

An interactive command-line and web-based assistant that gives preflop and postflop advice for Texas Hold'em poker.

## Getting Started

Follow these steps **after cloning** the repo to set up and run the project:

1. **Clone the repository**
   ```bash
   git clone https://github.com/JoshuaGerming/poker-partner.git
   cd poker-partner/poker-assistant
   ```

2. **Create & activate a Python virtual environment**
   - **Windows (PowerShell)**
     ```powershell
     py -3 -m venv venv
     Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy RemoteSigned -Force
     .\venv\Scripts\Activate.ps1
     ```
   - **Windows (cmd.exe)**
     ```bat
     py -3 -m venv venv
     venv\Scripts\activate.bat
     ```
   - **macOS / Linux**
     ```bash
     python3 -m venv venv
     source venv/bin/activate
     ```
   After activation your prompt should start with `(venv)`.

3. **Install dependencies**
   ```bash
   pip install --upgrade pip
   pip install -r requirements.txt
   ```

## Running the Assistant

### Command-Line Interface (CLI)

- **Preflop**:
  ```bash
  python assistant.py --hole Ah Kd --pos CO
  ```
- **Postflop**:
  ```bash
  python assistant.py \
    --hole Ah Kd \
    --board 2c 7d Th 9h 3s \
    --pos BTN \
    --pot 150 \
    --to-call 30
  ```

### Web UI (Streamlit)

Launch the browser-based UI:
```bash
python -m streamlit run app.py
```
- Use **Simulate Flop** to deal a random flop based on your hole cards.  
- Click **Get Recommendation** for preflop or postflop advice.  
- View your **Session History** at the bottom.

## Project Layout

```
poker-assistant/             # root of the assistant module
├── app.py                  # Streamlit web UI
├── assistant.py            # CLI entrypoint
├── charts/
│   └── preflop_chart.csv   # 169×6 preflop action chart
├── hand_evaluator.py       # wraps Treys for hand scores
├── opponent_simulator.py   # stubs random tightness/aggression
├── postflop.py             # postflop decision logic (heuristic)
├── preflop.py              # loads CSV and provides PreflopChart
├── tests/                  # pytest unit tests
│   ├── test_hand_evaluator.py
│   ├── test_preflop.py
│   ├── test_postflop.py
│   └── test_draws_and_odds.py
├── evaluate_performance.py # Monte Carlo backtester
├── requirements.txt        # Python dependencies
└── README.md               # this file
```
