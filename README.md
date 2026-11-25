# Portfolio Trade Order Compliance & Execution Checker

## Overview

The Portfolio Trade Order Compliance & Execution Checker is a Python-based application that validates proposed portfolio trades against a set of predefined compliance and execution-readiness rules before they can be executed.

The system processes trades from a CSV file, evaluates them sequentially against portfolio data stored in a JSON file, and generates trade decisions indicating whether each trade is:

- Approved
- Rejected
- Needs Manual Sign-off

The application also updates portfolio positions and cash balances after successful trade evaluations, simulating real-world trade processing behavior. The final portfolio state and trade evaluation results are exported for review. Based on the requirements defined in trade_compliance_requirements.md. 【1-78477d】

---

## Why This Project Is Useful

In investment and portfolio management systems, proposed trades cannot be executed without passing compliance checks.

This project helps:

- Prevent execution of invalid or restricted trades.
- Ensure sufficient cash is available before buy orders are placed.
- Ensure sufficient holdings exist before sell orders are executed.
- Monitor portfolio concentration risk.
- Simulate portfolio state changes after each accepted trade.
- Generate an auditable record of trade decisions.

The application processes trades sequentially, meaning each approved trade updates the portfolio and affects subsequent trade validations.

---

## Features

### Trade Validation Rules

The system evaluates trades in the following order:

1. Validate trade data
   - Quantity must be positive.
   - Price must be positive.
   - Action must be either Buy or Sell.

2. Restricted Security Check
   - Reject trades involving restricted securities.

3. Sell Holdings Check
   - Verify sufficient holdings exist before selling.

4. Buy Affordability Check
   - Verify available cash can cover the purchase.

5. Position Concentration Check
   - Flag trades exceeding maximum portfolio concentration limits.

6. Trade Decision
   - Approved
   - Rejected
   - Needs Manual Sign-off

Based on the business requirements in trade_compliance_requirements.md. 【1-78477d】

---

## Project Structure

```text
trade-compliance-checker/
│
├── main.py
│
├── data/
│   ├── portfolios.json
│   └── trades_test.csv
│
├── models/
│   ├── trade.py
│   ├── portfolio.py
│   └── decision.py
│
├── repositories/
│   └── portfolio_repository.py
│
├── services/
│   ├── trade_checker.py
│   └── portfolio_updater.py
│
├── processors/
│   └── batch_processor.py
│
├── output/
│   ├── results.csv
│   └── portfolios_final.json
│
└── README.md
```

---

## Input Files

### Portfolio Data

Portfolio information is stored in:

```text
data/portfolios.json
```

The file contains:

- Cash balance
- Restricted securities
- Maximum position concentration
- Current holdings

Example:

```json
{
  "POR001": {
    "cash_balance": 100000,
    "restricted_securities": ["XYZCORP"],
    "max_position_pct": 0.25,
    "current_holdings": [
      {
        "security_id": "AAPL",
        "quantity": 100,
        "market_price": 150
      }
    ]
  }
}
```

---

### Trade Data

Trades are provided via CSV.

Example from trades_test.csv: 【2-249cfc】

```csv
portfolio_id,security_id,action,quantity,price,security_type
POR001,AAPL,Buy,20,150,Equity
POR001,TCS,Sell,50,310,Equity
POR003,RELIANCE,Sell,30,2400,Equity
```

---

## How It Works

1. Load portfolio data from JSON.
2. Read trades from CSV.
3. Process trades sequentially.
4. Evaluate each trade against compliance rules.
5. Generate a decision for each trade.
6. Update portfolio state for:
   - Approved trades
   - Needs Manual Sign-off trades
7. Export:
   - Trade results
   - Final portfolio snapshot
8. Display results in the terminal.

---

## Getting Started

### Prerequisites

- Python 3.10+

Verify installation:

```bash
python --version
```

---

### Clone or Download

```bash
git clone <https://github.com/JayantGoyal27/Portfolio-Trade-Order-Compliance-Execution-Checker..git>
cd trade-compliance-checker
```

Or simply download the project folder.

---

### Prepare Input Files

Place the following files inside the `data` directory:

```text
data/
├── portfolios.json
└── trades_test.csv
```

---

### Run the Application

```bash
python main.py
```

---

## Outputs

### Trade Evaluation Results

Generated file:

```text
output/results.csv
```

Example:

```csv
portfolio_id,security_id,decision,reason
POR001,AAPL,Approved,Trade approved.
POR001,TCS,Rejected,Insufficient holdings to sell.
```

---

### Final Portfolio Snapshot

Generated file:

```text
output/portfolios_final.json
```

Contains the updated portfolio state after all valid trades have been processed.

---

## Example Terminal Output

```text
Trade Processing Results
-----------------------------------------------------

POR001 | AAPL | Approved | Trade approved.
POR001 | TCS | Rejected | Insufficient holdings to sell.

Processing completed.

Final Portfolio State
--------------------------------------------------------------------------------

Portfolio: POR001
Cash Balance: 28500.0
Holdings:
  AAPL | Qty=580.0 | Price=150.0
  INFY | Qty=10.0 | Price=1500.0
```

---

## Assumptions

- Trades are processed in the exact order provided in the CSV file.
- Each approved trade immediately updates portfolio state.
- Trades requiring manual sign-off also update portfolio state.
- Rejected trades do not affect portfolio state.
- Portfolio data is loaded into memory at startup.

---

## Author

Jayant Goyal