from decimal import Decimal

from market_data.models import Cryptocurrency
from market_data.services.market_data_service import (
    MarketDataService,
)


class PortfolioValuationService:
    """Calculate the current value and performance of a portfolio."""

    def __init__(self, market_data_service=None):
        self.market_data_service = (
            market_data_service or MarketDataService()
        )

    def value_portfolio(self, portfolio):
        assets = list(portfolio.assets.all())

        if not assets:
            return {
                "total_value": Decimal("0"),
                "known_cost_basis": Decimal("0"),
                "known_basis_value": Decimal("0"),
                "profit_loss": Decimal("0"),
                "return_percentage": None,
                "cost_basis_coverage_percentage": None,
                "assets": [],
            }

        symbols = [
            asset.symbol
            for asset in assets
        ]

        cryptocurrencies = Cryptocurrency.objects.filter(
            symbol__in=symbols,
            is_active=True,
        )

        cryptocurrency_by_symbol = {
            cryptocurrency.symbol: cryptocurrency
            for cryptocurrency in cryptocurrencies
        }

        provider_ids = [
            cryptocurrency.provider_id
            for cryptocurrency in cryptocurrencies
        ]

        prices = self.market_data_service.get_current_prices(
            provider_ids
        )

        asset_values = []

        total_value = Decimal("0")
        known_cost_basis = Decimal("0")
        known_basis_value = Decimal("0")

        for asset in assets:
            cryptocurrency = cryptocurrency_by_symbol.get(
                asset.symbol
            )

            if not cryptocurrency:
                continue

            price_data = prices.get(
                cryptocurrency.provider_id,
                {},
            )

            current_price_raw = price_data.get("usd")

            if current_price_raw is None:
                continue

            current_price = Decimal(
                str(current_price_raw)
            )

            current_value = (
                asset.quantity * current_price
            )

            cost_basis = None
            profit_loss = None
            return_percentage = None

            if asset.average_purchase_price is not None:
                cost_basis = (
                    asset.quantity
                    * asset.average_purchase_price
                )

                profit_loss = (
                    current_value - cost_basis
                )

                if cost_basis > 0:
                    return_percentage = (
                        profit_loss
                        / cost_basis
                        * Decimal("100")
                    )

                known_cost_basis += cost_basis
                known_basis_value += current_value

            total_value += current_value

            asset_values.append(
                {
                    "id": asset.id,
                    "symbol": asset.symbol,
                    "quantity": asset.quantity,
                    "average_purchase_price":
                        asset.average_purchase_price,
                    "current_price": current_price,
                    "current_value": current_value,
                    "cost_basis": cost_basis,
                    "profit_loss": profit_loss,
                    "return_percentage":
                        return_percentage,
                    "allocation_percentage":
                        Decimal("0"),
                }
            )

        # Calculate each asset's share of the total
        # current portfolio value.
        if total_value > 0:
            for asset_value in asset_values:
                asset_value["allocation_percentage"] = (
                    asset_value["current_value"]
                    / total_value
                    * Decimal("100")
                )

        profit_loss = (
            known_basis_value - known_cost_basis
        )

        return_percentage = None

        if known_cost_basis > 0:
            return_percentage = (
                profit_loss
                / known_cost_basis
                * Decimal("100")
            )

        cost_basis_coverage_percentage = None

        if total_value > 0:
            cost_basis_coverage_percentage = (
                known_basis_value
                / total_value
                * Decimal("100")
            )

        return {
            "total_value": total_value,
            "known_cost_basis": known_cost_basis,
            "known_basis_value": known_basis_value,
            "profit_loss": profit_loss,
            "return_percentage": return_percentage,
            "cost_basis_coverage_percentage":
                cost_basis_coverage_percentage,
            "assets": asset_values,
        }