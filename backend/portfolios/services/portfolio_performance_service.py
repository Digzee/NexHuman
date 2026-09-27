from datetime import datetime, timezone
from decimal import Decimal
from math import sqrt

from market_data.models import Cryptocurrency
from market_data.services.market_data_service import (
    MarketDataService,
)


class PortfolioPerformanceService:
    """Calculate historical performance for a portfolio."""

    ANNUALISATION_DAYS = Decimal("365")

    def __init__(self, market_data_service=None):
        self.market_data_service = (
            market_data_service or MarketDataService()
        )

    def calculate_performance(
        self,
        portfolio,
        days=30,
    ):
        assets = list(portfolio.assets.all())

        if not assets:
            return self._empty_result(days)

        historical_assets = []

        for asset in assets:
            cryptocurrency = Cryptocurrency.objects.filter(
                symbol=asset.symbol,
                is_active=True,
            ).first()

            if cryptocurrency is None:
                return self._empty_result(days)

            history = (
                self.market_data_service
                .get_historical_prices(
                    cryptocurrency.provider_id,
                    days,
                )
            )

            prices = history.get("prices", [])

            if not prices:
                return self._empty_result(days)

            prices_by_date = {}

            for timestamp, price in prices:
                date = self._timestamp_to_date(
                    timestamp
                )

                prices_by_date[date] = Decimal(
                    str(price)
                )

            if not prices_by_date:
                return self._empty_result(days)

            historical_assets.append(
                {
                    "symbol": asset.symbol,
                    "quantity": asset.quantity,
                    "prices_by_date": prices_by_date,
                }
            )

        common_dates = set(
            historical_assets[0][
                "prices_by_date"
            ].keys()
        )

        for asset in historical_assets[1:]:
            common_dates &= set(
                asset["prices_by_date"].keys()
            )

        if not common_dates:
            return self._empty_result(days)

        data_points = []

        for date in sorted(common_dates):
            portfolio_value = Decimal("0")

            for asset in historical_assets:
                price = asset[
                    "prices_by_date"
                ][date]

                portfolio_value += (
                    asset["quantity"] * price
                )

            data_points.append(
                {
                    "date": date,
                    "value": portfolio_value,
                }
            )

        starting_value = data_points[0]["value"]
        ending_value = data_points[-1]["value"]

        total_return_percentage = (
            self._calculate_total_return(
                starting_value,
                ending_value,
            )
        )

        annualised_return_percentage = (
            self._calculate_annualised_return(
                starting_value,
                ending_value,
                days,
            )
        )

        daily_returns = (
            self._calculate_daily_returns(
                data_points
            )
        )

        annualised_volatility_percentage = (
            self._calculate_annualised_volatility(
                daily_returns
            )
        )

        maximum_drawdown_percentage = (
            self._calculate_maximum_drawdown(
                data_points
            )
        )

        return {
            "period_days": days,
            "starting_value": starting_value,
            "ending_value": ending_value,
            "total_return_percentage":
                total_return_percentage,
            "annualised_return_percentage":
                annualised_return_percentage,
            "annualised_volatility_percentage":
                annualised_volatility_percentage,
            "maximum_drawdown_percentage":
                maximum_drawdown_percentage,
            "data_points": data_points,
        }

    @staticmethod
    def _calculate_total_return(
        starting_value,
        ending_value,
    ):
        if starting_value <= 0:
            return None

        return (
            (ending_value - starting_value)
            / starting_value
            * Decimal("100")
        )

    def _calculate_annualised_return(
        self,
        starting_value,
        ending_value,
        days,
    ):
        if (
            starting_value <= 0
            or ending_value <= 0
            or days <= 0
        ):
            return None

        growth_ratio = (
            ending_value / starting_value
        )

        annualisation_factor = (
            float(self.ANNUALISATION_DAYS)
            / float(days)
        )

        annualised_return = (
            float(growth_ratio)
            ** annualisation_factor
        ) - 1

        return Decimal(
            str(annualised_return * 100)
        )

    @staticmethod
    def _calculate_daily_returns(data_points):
        daily_returns = []

        for index in range(
            1,
            len(data_points),
        ):
            previous_value = data_points[
                index - 1
            ]["value"]

            current_value = data_points[
                index
            ]["value"]

            if previous_value <= 0:
                continue

            daily_return = (
                current_value - previous_value
            ) / previous_value

            daily_returns.append(
                daily_return
            )

        return daily_returns

    def _calculate_annualised_volatility(
        self,
        daily_returns,
    ):
        if len(daily_returns) < 2:
            return None

        mean_return = (
            sum(daily_returns)
            / Decimal(len(daily_returns))
        )

        squared_differences = [
            (daily_return - mean_return) ** 2
            for daily_return in daily_returns
        ]

        variance = (
            sum(squared_differences)
            / Decimal(
                len(daily_returns) - 1
            )
        )

        daily_volatility = sqrt(
            float(variance)
        )

        annualised_volatility = (
            daily_volatility
            * sqrt(
                float(
                    self.ANNUALISATION_DAYS
                )
            )
        )

        return Decimal(
            str(
                annualised_volatility
                * 100
            )
        )

    @staticmethod
    def _calculate_maximum_drawdown(
        data_points,
    ):
        if not data_points:
            return None

        peak_value = data_points[0][
            "value"
        ]

        maximum_drawdown = Decimal("0")

        for point in data_points:
            current_value = point["value"]

            if current_value > peak_value:
                peak_value = current_value

            if peak_value <= 0:
                continue

            drawdown = (
                current_value - peak_value
            ) / peak_value

            if drawdown < maximum_drawdown:
                maximum_drawdown = drawdown

        return (
            maximum_drawdown
            * Decimal("100")
        )

    @staticmethod
    def _empty_result(days):
        return {
            "period_days": days,
            "starting_value": Decimal("0"),
            "ending_value": Decimal("0"),
            "total_return_percentage": None,
            "annualised_return_percentage": None,
            "annualised_volatility_percentage": None,
            "maximum_drawdown_percentage": None,
            "data_points": [],
        }

    @staticmethod
    def _timestamp_to_date(timestamp):
        return datetime.fromtimestamp(
            timestamp / 1000,
            tz=timezone.utc,
        ).date().isoformat()