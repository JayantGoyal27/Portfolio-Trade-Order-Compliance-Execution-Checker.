
from models.decision import TradeDecision
from constants.decisions import (
    APPROVED,
    REJECTED,
    MANUAL_SIGNOFF
)

class TradeChecker:

    def evaluate_trade(self, trade, portfolio):

        # Step 1
        if (
            trade.quantity <= 0
            or trade.price <= 0
            or trade.action not in ["Buy", "Sell"]
        ):
            return TradeDecision(
                trade.portfolio_id,
                trade.security_id,
                REJECTED,
                "Invalid trade data."
            )

        # Step 2
        if trade.security_id in portfolio.restricted_securities:
            return TradeDecision(
                trade.portfolio_id,
                trade.security_id,
                REJECTED,
                "Security is restricted for this portfolio."
            )

        # Step 3
        if trade.action == "Sell":

            holding_qty = 0

            for holding in portfolio.current_holdings:
                if holding.security_id == trade.security_id:
                    holding_qty = holding.quantity
                    break

            if holding_qty < trade.quantity:
                return TradeDecision(
                    trade.portfolio_id,
                    trade.security_id,
                    REJECTED,
                    "Insufficient holdings to sell."
                )

        # Step 4
        if trade.action == "Buy":

            cost = trade.quantity * trade.price

            if cost > portfolio.cash_balance:
                return TradeDecision(
                    trade.portfolio_id,
                    trade.security_id,
                    REJECTED,
                    "Insufficient cash for this buy order."
                )

        # Step 5
        if trade.action == "Buy":

            decision = self._check_concentration(
                trade,
                portfolio
            )

            if decision:
                return decision

        return TradeDecision(
            trade.portfolio_id,
            trade.security_id,
            APPROVED,
            "Trade approved."
        )

    def _check_concentration(
        self,
        trade,
        portfolio
    ):

        post_trade_cash = (
            portfolio.cash_balance
            - trade.quantity * trade.price
        )

        existing_quantity = 0

        for holding in portfolio.current_holdings:
            if holding.security_id == trade.security_id:
                existing_quantity = holding.quantity
                break

        post_trade_quantity = (
            existing_quantity
            + trade.quantity
        )

        security_value = (
            post_trade_quantity
            * trade.price
        )

        other_holdings_value = 0

        for holding in portfolio.current_holdings:

            if holding.security_id == trade.security_id:
                continue

            other_holdings_value += (
                holding.quantity
                * holding.market_price
            )

        total_value = (
            post_trade_cash
            + security_value
            + other_holdings_value
        )

        position_pct = security_value / total_value

        if position_pct > portfolio.max_position_pct:

            return TradeDecision(
                trade.portfolio_id,
                trade.security_id,
                MANUAL_SIGNOFF,
                "Exceeds maximum position concentration — requires approval."
            )

        return None