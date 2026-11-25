import csv

from models.trade import Trade

from services.trade_checker import (
    TradeChecker,
    APPROVED,
    MANUAL_SIGNOFF
)

from services.portfolio_updater import PortfolioUpdater

class BatchProcessor:

    def __init__(self, portfolio_repository):
        self.portfolio_repository = portfolio_repository
        self.trade_checker = TradeChecker()
        self.portfolio_updater = PortfolioUpdater()

    def process(
        self,
        input_file: str,
        output_file: str
    ):

        results = []

        with open(input_file, mode="r", newline="") as file:

            reader = csv.DictReader(file)

            for row in reader:

                trade = Trade(
                    portfolio_id=row["portfolio_id"].strip(),
                    security_id=row["security_id"].strip(),
                    action=row["action"].strip(),
                    quantity=float(row["quantity"]),
                    price=float(row["price"]),
                    security_type=row["security_type"].strip()
                )

                portfolio = (
                    self.portfolio_repository
                    .get_portfolio(trade.portfolio_id)
                )

                if portfolio is None:

                    results.append({
                        "portfolio_id": trade.portfolio_id,
                        "security_id": trade.security_id,
                        "decision": "Rejected",
                        "reason": "Portfolio not found."
                    })

                    continue

                decision = self.trade_checker.evaluate_trade(
                    trade,
                    portfolio
                )

                results.append({
                    "portfolio_id": decision.portfolio_id,
                    "security_id": decision.security_id,
                    "decision": decision.decision,
                    "reason": decision.reason
                })

                if decision.decision in [
                    APPROVED,
                    MANUAL_SIGNOFF
                ]:
                    self.portfolio_updater.apply_trade(
                        portfolio,
                        trade
                    )

        self._write_results(
            results,
            output_file
        )
        print("\nTrade Processing Results")
        print("-" * 80)

        for result in results:
            print(
                f"{result['portfolio_id']} | "
                f"{result['security_id']} | "
                f"{result['decision']} | "
                f"{result['reason']}\n"
            )

    def _write_results(
        self,
        results,
        output_file
    ):

        with open(
            output_file,
            mode="w",
            newline=""
        ) as file:

            writer = csv.DictWriter(
                file,
                fieldnames=[
                    "portfolio_id",
                    "security_id",
                    "decision",
                    "reason"
                ]
            )

            writer.writeheader()

            writer.writerows(results)