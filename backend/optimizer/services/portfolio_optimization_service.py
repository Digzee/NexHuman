from django.db import transaction

from market_data.models import Cryptocurrency

from optimizer.models import (
    OptimizationAllocation,
    OptimizationRun,
)

from .optimization_service import (
    OptimizationService,
)
from .return_data_service import (
    ReturnDataService,
)


class PortfolioOptimizationService:
    """Run and persist a complete NexHuman portfolio optimisation."""

    HISTORICAL_DAYS = 365

    def __init__(
        self,
        return_data_service=None,
    ):
        self.return_data_service = (
            return_data_service
            or ReturnDataService()
        )

    @transaction.atomic
    def optimise(
        self,
        user,
        portfolio,
        seed=None,
    ):
        try:
            investor_profile = (
                user.investor_profile
            )
        except Exception as error:
            raise ValueError(
                "Complete your investor profile "
                "before running optimisation."
            ) from error

        symbols = list(
            Cryptocurrency.objects.filter(
                is_active=True,
            )
            .order_by("symbol")
            .values_list(
                "symbol",
                flat=True,
            )
        )

        if len(symbols) < 2:
            raise ValueError(
                "At least two supported assets "
                "are required for optimisation."
            )

        asset_returns = (
            self.return_data_service
            .get_asset_returns(
                symbols,
                self.HISTORICAL_DAYS,
            )
        )

        result = OptimizationService.optimise(
            asset_returns=asset_returns,
            risk_profile=(
                investor_profile.risk_label
            ),
            seed=seed,
        )

        optimized = result["optimized"]
        baseline = result["baseline"]
        configuration = result[
            "configuration"
        ]

        run = OptimizationRun.objects.create(
            user=user,
            portfolio=portfolio,
            risk_profile=(
                investor_profile.risk_label
            ),
            historical_days=(
                self.HISTORICAL_DAYS
            ),
            population_size=(
                configuration[
                    "population_size"
                ]
            ),
            generations=(
                configuration[
                    "generations"
                ]
            ),
            expected_return=(
                optimized[
                    "expected_return"
                ]
            ),
            volatility=(
                optimized["volatility"]
            ),
            sharpe_ratio=(
                optimized["sharpe_ratio"]
            ),
            baseline_return=(
                baseline[
                    "expected_return"
                ]
            ),
            baseline_volatility=(
                baseline["volatility"]
            ),
            baseline_sharpe_ratio=(
                baseline["sharpe_ratio"]
            ),
        )

        OptimizationAllocation.objects.bulk_create(
            [
                OptimizationAllocation(
                    run=run,
                    symbol=symbol,
                    weight=weight,
                )
                for symbol, weight
                in optimized["weights"].items()
            ]
        )

        return run