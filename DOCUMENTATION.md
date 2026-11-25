# Project Documentation

# Portfolio Trade Order Compliance & Execution Checker

## Overview

This project validates portfolio trades against a set of compliance and execution rules before execution.

The application:

1. Loads portfolio reference data from a JSON file.
2. Reads proposed trades from a CSV file.
3. Processes trades sequentially.
4. Validates each trade against compliance rules.
5. Updates portfolio state for accepted trades.
6. Generates decision reports.
7. Saves the final portfolio state after processing.

---

# High-Level Execution Flow

```text
portfolios.json
        │
        ▼
PortfolioRepository
        │
        ▼
BatchProcessor
        │
        ▼
TradeChecker
        │
        ▼
TradeDecision
        │
        ▼
PortfolioUpdater
        │
        ▼
Updated Portfolio State
        │
        ├── results.csv
        └── portfolios_final.json
```

---

# Project Structure

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

# Root Files

## main.py

### Purpose

Application entry point.

### Responsibilities

- Initializes repository.
- Initializes batch processor.
- Starts trade processing.
- Saves final portfolio state.
- Displays processing results.

### Flow

```python
Load Portfolio Data
        ↓
Read Trade CSV
        ↓
Process Trades
        ↓
Generate Results
        ↓
Save Final Portfolios
```

---

# data/

Contains all input files required by the application.

---

## portfolios.json

### Purpose

Stores portfolio reference data.

### Contents

Each portfolio contains:

- Portfolio ID
- Cash Balance
- Restricted Securities
- Maximum Position Concentration
- Current Holdings

### Example

```json
{
  "POR001": {
    "cash_balance": 100000
  }
}
```

---

## trades_test.csv

### Purpose

Stores the list of proposed trades.

### Example

```csv
portfolio_id,security_id,action,quantity,price,security_type
POR001,AAPL,Buy,20,150,Equity
```

### Processing Order

Trades are processed in the exact order in which they appear in the file.

---

# models/

Contains all domain models used by the application.

Models are simple data structures that represent business entities.

---

## trade.py

### Purpose

Represents a single trade request.

### Class

```python
Trade
```

### Attributes

| Field | Description |
|---------|-------------|
| portfolio_id | Portfolio identifier |
| security_id | Security symbol |
| action | Buy or Sell |
| quantity | Number of units |
| price | Trade price |
| security_type | Equity/Bond/ETF |

### Example

```python
Trade(
    portfolio_id="POR001",
    security_id="AAPL",
    action="Buy",
    quantity=20,
    price=150,
    security_type="Equity"
)
```

---

## portfolio.py

### Purpose

Represents portfolio-related information.

### Classes

```python
Holding
Portfolio
```

---

### Holding

Represents a single security position.

#### Attributes

| Field | Description |
|---------|-------------|
| security_id | Security symbol |
| quantity | Number of units held |
| market_price | Current market price |

---

### Portfolio

Represents a complete portfolio.

#### Attributes

| Field | Description |
|---------|-------------|
| portfolio_id | Portfolio identifier |
| cash_balance | Available cash |
| restricted_securities | Securities that cannot be traded |
| max_position_pct | Maximum allowed concentration |
| current_holdings | Collection of holdings |

---

## decision.py

### Purpose

Represents the outcome of trade validation.

### Class

```python
TradeDecision
```

### Attributes

| Field | Description |
|---------|-------------|
| portfolio_id | Portfolio identifier |
| security_id | Security symbol |
| decision | Approved / Rejected / Needs Manual Sign-off |
| reason | Reason for decision |

---

# repositories/

Responsible for data access.

Repositories isolate file access from business logic.

---

## portfolio_repository.py

### Purpose

Loads and stores portfolio information.

### Responsibilities

- Read portfolios from JSON.
- Convert JSON into Portfolio objects.
- Retrieve portfolios by ID.
- Save updated portfolios after processing.

### Public Methods

### Load Data

```python
_load()
```

Loads data from JSON.

---

### Get Portfolio

```python
get_portfolio(portfolio_id)
```

Returns a portfolio object.

---

### Get All Portfolios

```python
get_all()
```

Returns all portfolios.

---

### Save

```python
save(output_file)
```

Writes updated portfolio data to JSON.

---

# services/

Contains the business logic layer.

This is the core of the application.

---

## trade_checker.py

### Purpose

Validates trades against compliance rules.

### Responsibilities

Determines whether a trade should be:

- Approved
- Rejected
- Sent for Manual Sign-off

### Main Method

```python
evaluate_trade()
```

---

### Validation Rules

---

#### Rule 1

Trade Validation

Checks:

- Quantity > 0
- Price > 0
- Action is Buy or Sell

Failure:

```text
Rejected
Invalid trade data.
```

---

#### Rule 2

Restricted Security Check

Checks:

```text
Security exists in restricted list
```

Failure:

```text
Rejected
Security is restricted for this portfolio.
```

---

#### Rule 3

Sell Validation

Checks:

```text
Holding quantity >= sell quantity
```

Failure:

```text
Rejected
Insufficient holdings to sell.
```

---

#### Rule 4

Buy Affordability

Checks:

```text
Cash Balance >= Trade Cost
```

Failure:

```text
Rejected
Insufficient cash for this buy order.
```

---

#### Rule 5

Position Concentration Check

Calculates:

```text
Position %
```

Checks:

```text
Position % > max_position_pct
```

Result:

```text
Needs Manual Sign-off
```

---

#### Rule 6

Approval

If no previous rule fails:

```text
Approved
```

---

## portfolio_updater.py

### Purpose

Updates portfolio state after successful validation.

### Responsibilities

- Adjust cash balance.
- Update quantities.
- Create new holdings.
- Remove empty holdings.

---

### Buy Processing

Updates:

```text
Cash Balance
Holding Quantity
Market Price
```

---

### Sell Processing

Updates:

```text
Cash Balance
Holding Quantity
```

If quantity reaches zero:

```text
Holding is removed.
```

---

# processors/

Coordinates the end-to-end workflow.

Acts as the application's orchestrator.

---

## batch_processor.py

### Purpose

Processes all trades from a CSV file.

### Responsibilities

- Read trade CSV.
- Convert rows into Trade objects.
- Retrieve portfolios.
- Execute validation.
- Record decisions.
- Apply successful trades.
- Generate output files.

---

### Processing Workflow

```text
Read CSV Row
      ↓
Create Trade Object
      ↓
Load Portfolio
      ↓
Validate Trade
      ↓
Get Decision
      ↓
Update Portfolio
      ↓
Store Result
```

---

### Portfolio State Update Rules

| Decision | Update Portfolio |
|-----------|------------------|
| Approved | Yes |
| Needs Manual Sign-off | Yes |
| Rejected | No |

---

# output/

Contains generated output files.

Created after processing.

---

## results.csv

### Purpose

Stores trade-level decisions.

### Example

```csv
portfolio_id,security_id,decision,reason
POR001,AAPL,Approved,Trade approved.
```

---

## portfolios_final.json

### Purpose

Stores the final state of all portfolios after processing.

### Includes

- Updated cash balances
- Updated holdings
- New positions
- Deleted positions

Used for verification and auditing.

---

# Design Decisions

## Why JSON?

- Lightweight
- No database setup
- Easy to inspect
- Simple for local execution

---

## Why CSV?

- Common business data format
- Easy to generate and edit
- Supports bulk trade processing

---

## Why Sequential Processing?

Portfolio state changes after accepted trades.

Example:

```text
Trade 1
Approved
      ↓
Portfolio Updated

Trade 2
Uses Updated Portfolio
```

This better reflects real-world portfolio management systems.

---
