from dataclasses import dataclass


@dataclass
class TradeDecision:
    portfolio_id: str
    security_id: str
    decision: str
    reason: str

