from dataclasses import dataclass
from typing import List


@dataclass
class Holding:
    security_id: str
    quantity: float
    market_price: float


@dataclass
class Portfolio:
    portfolio_id: str
    cash_balance: float
    restricted_securities: List[str]
    max_position_pct: float
    current_holdings: List[Holding]