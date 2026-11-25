from dataclasses import dataclass


@dataclass
class Trade:
    portfolio_id: str
    security_id: str
    action: str
    quantity: float
    price: float
    security_type: str