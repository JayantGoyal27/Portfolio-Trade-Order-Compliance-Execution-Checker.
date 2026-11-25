import json

from models.portfolio import Portfolio
from models.portfolio import Holding


class PortfolioRepository:

    def __init__(self, file_path: str):
        self.file_path = file_path
        self.portfolios = self._load()

    def _load(self):
        with open(self.file_path, "r") as file:
            raw_data = json.load(file)

        portfolios = {}

        for portfolio_id, data in raw_data.items():

            holdings = [
                Holding(
                    security_id=h["security_id"],
                    quantity=h["quantity"],
                    market_price=h["market_price"]
                )
                for h in data["current_holdings"]
            ]

            portfolios[portfolio_id] = Portfolio(
                portfolio_id=portfolio_id,
                cash_balance=data["cash_balance"],
                restricted_securities=data["restricted_securities"],
                max_position_pct=data["max_position_pct"],
                current_holdings=holdings
            )

        return portfolios

    def get_portfolio(self, portfolio_id):
        return self.portfolios.get(portfolio_id)

    def get_all(self):
        return self.portfolios

    def save(self, output_file: str):

        data = {}

        for portfolio_id, portfolio in self.portfolios.items():

            data[portfolio_id] = {
                "cash_balance": portfolio.cash_balance,
                "restricted_securities": portfolio.restricted_securities,
                "max_position_pct": portfolio.max_position_pct,
                "current_holdings": [
                    {
                        "security_id": holding.security_id,
                        "quantity": holding.quantity,
                        "market_price": holding.market_price
                    }
                    for holding in portfolio.current_holdings
                ]
            }

        with open(output_file, "w") as file:
            json.dump(data, file, indent=4)