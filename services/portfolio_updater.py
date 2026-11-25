from models.portfolio import Holding
class PortfolioUpdater:

    def apply_trade(self, portfolio, trade):

        trade_value = (
            trade.quantity
            * trade.price
        )

        if trade.action == "Buy":

            portfolio.cash_balance -= trade_value

            for holding in portfolio.current_holdings:

                if holding.security_id == trade.security_id:

                    holding.quantity += trade.quantity
                    holding.market_price = trade.price
                    return

            portfolio.current_holdings.append(
                Holding(
                    security_id=trade.security_id,
                    quantity=trade.quantity,
                    market_price=trade.price
                )
            )

        else:

            portfolio.cash_balance += trade_value

            for holding in portfolio.current_holdings:

                if holding.security_id == trade.security_id:

                    holding.quantity -= trade.quantity

                    if holding.quantity == 0:
                        portfolio.current_holdings.remove(
                            holding
                        )

                    return