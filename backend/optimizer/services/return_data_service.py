from datetime import datetime, timezone

from market_data.models import Cryptocurrency
from market_data.services.market_data_service import (
    MarketDataService,
)


class ReturnDataService:
    """Prepare aligned historical daily returns for optimisation."""

    def __init__(self, market_data_service=None):
        self.market_data_service = (
            market_data_service
            or MarketDataService()
        )

    def get_asset_returns(
        self,
        symbols,
        days=365,
    ):
        cryptocurrencies = {
            cryptocurrency.symbol:
                cryptocurrency
            for cryptocurrency in (
                Cryptocurrency.objects.filter(
                    symbol__in=symbols,
                    is_active=True,
                )
            )
        }

        missing_symbols = (
            set(symbols)
            - set(cryptocurrencies.keys())
        )

        if missing_symbols:
            raise ValueError(
                "Unsupported cryptocurrency: "
                + ", ".join(
                    sorted(missing_symbols)
                )
            )

        price_series = {}

        for symbol in symbols:
            cryptocurrency = cryptocurrencies[
                symbol
            ]

            data = (
                self.market_data_service
                .get_historical_prices(
                    cryptocurrency.provider_id,
                    days,
                )
            )

            prices = data.get("prices", [])

            daily_prices = {}

            for timestamp, price in prices:
                date = datetime.fromtimestamp(
                    timestamp / 1000,
                    tz=timezone.utc,
                ).date()

                daily_prices[date] = float(price)

            price_series[symbol] = daily_prices

        common_dates = set.intersection(
            *(
                set(series.keys())
                for series in price_series.values()
            )
        )

        ordered_dates = sorted(common_dates)

        if len(ordered_dates) < 3:
            raise ValueError(
                "Insufficient common historical "
                "price data for optimisation."
            )

        returns = {}

        for symbol, series in price_series.items():
            asset_returns = []

            for index in range(
                1,
                len(ordered_dates),
            ):
                previous_price = series[
                    ordered_dates[index - 1]
                ]

                current_price = series[
                    ordered_dates[index]
                ]

                if previous_price <= 0:
                    raise ValueError(
                        "Invalid historical price data."
                    )

                daily_return = (
                    current_price
                    / previous_price
                ) - 1

                asset_returns.append(
                    daily_return
                )

            returns[symbol] = asset_returns

        return returns