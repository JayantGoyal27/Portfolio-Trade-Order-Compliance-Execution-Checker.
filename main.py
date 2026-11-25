from repositories.portfolio_repository import PortfolioRepository
from processors.batch_processor import BatchProcessor


def main():

    repository = PortfolioRepository(
        "data/portfolios.json"
    )

    processor = BatchProcessor(
        repository
    )

    processor.process(
        input_file="data/trades_test.csv",
        output_file="output/results.csv"
    )

    repository.save(
        "output/portfolios_final.json"
    )
    print("Processing completed.")
    print("\nFinal Portfolio State")
    print("-" * 80)

    for portfolio in repository.get_all().values():

        print(f"\nPortfolio: {portfolio.portfolio_id}")
        print(f"Cash Balance: {portfolio.cash_balance}")

        print("Holdings:")

        for holding in portfolio.current_holdings:
            print(
                f"  {holding.security_id} | "
                f"Qty={holding.quantity} | "
                f"Price={holding.market_price}"
            )
    


if __name__ == "__main__":
    main()