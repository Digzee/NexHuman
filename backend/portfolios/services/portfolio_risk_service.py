from decimal import Decimal


class PortfolioRiskService:
    """Calculate portfolio risk and diversification measures."""

    def calculate_risk(
        self,
        valuation,
        performance,
    ):
        assets = valuation.get(
            "assets",
            [],
        )

        annualised_volatility = (
            performance.get(
                "annualised_volatility_percentage"
            )
        )

        maximum_drawdown = (
            performance.get(
                "maximum_drawdown_percentage"
            )
        )

        allocations = [
            Decimal(
                str(
                    asset[
                        "allocation_percentage"
                    ]
                )
            )
            for asset in assets
            if asset.get(
                "allocation_percentage"
            )
            is not None
        ]

        largest_holding_percentage = (
            max(allocations)
            if allocations
            else None
        )

        concentration_index = (
            self._calculate_concentration_index(
                allocations
            )
        )

        diversification_label = (
            self._classify_diversification(
                concentration_index
            )
        )

        risk_label = (
            self._classify_risk(
                annualised_volatility,
                maximum_drawdown,
                largest_holding_percentage,
            )
        )

        return {
            "risk_label": risk_label,
            "annualised_volatility_percentage":
                annualised_volatility,
            "maximum_drawdown_percentage":
                maximum_drawdown,
            "largest_holding_percentage":
                largest_holding_percentage,
            "concentration_index":
                concentration_index,
            "diversification_label":
                diversification_label,
            "asset_count": len(assets),
        }

    @staticmethod
    def _calculate_concentration_index(
        allocations,
    ):
        if not allocations:
            return None

        weights = [
            allocation / Decimal("100")
            for allocation in allocations
        ]

        return sum(
            weight ** 2
            for weight in weights
        )

    @staticmethod
    def _classify_diversification(
        concentration_index,
    ):
        if concentration_index is None:
            return "Unavailable"

        if concentration_index <= Decimal(
            "0.25"
        ):
            return "High"

        if concentration_index <= Decimal(
            "0.50"
        ):
            return "Moderate"

        return "Low"

    @staticmethod
    def _classify_risk(
        annualised_volatility,
        maximum_drawdown,
        largest_holding_percentage,
    ):
        if (
            annualised_volatility is None
            or maximum_drawdown is None
            or largest_holding_percentage is None
        ):
            return "Unavailable"

        volatility = Decimal(
            str(annualised_volatility)
        )

        drawdown = abs(
            Decimal(
                str(maximum_drawdown)
            )
        )

        largest_holding = Decimal(
            str(
                largest_holding_percentage
            )
        )

        risk_score = 0

        if volatility >= Decimal("80"):
            risk_score += 3
        elif volatility >= Decimal("50"):
            risk_score += 2
        elif volatility >= Decimal("25"):
            risk_score += 1

        if drawdown >= Decimal("40"):
            risk_score += 3
        elif drawdown >= Decimal("25"):
            risk_score += 2
        elif drawdown >= Decimal("10"):
            risk_score += 1

        if largest_holding >= Decimal("75"):
            risk_score += 3
        elif largest_holding >= Decimal("50"):
            risk_score += 2
        elif largest_holding >= Decimal("35"):
            risk_score += 1

        if risk_score >= 7:
            return "Very High"

        if risk_score >= 5:
            return "High"

        if risk_score >= 3:
            return "Moderate"

        return "Low"