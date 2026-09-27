class RecommendationService:
    """Generate transparent explanations for optimisation results."""

    @staticmethod
    def generate(run):
        allocations = list(
            run.allocations.order_by(
                "-weight"
            )
        )

        meaningful_allocations = [
            allocation
            for allocation in allocations
            if allocation.weight >= 0.001
        ]

        if meaningful_allocations:
            largest = meaningful_allocations[0]

            allocation_summary = ", ".join(
                (
                    f"{allocation.symbol} "
                    f"{allocation.weight * 100:.1f}%"
                )
                for allocation
                in meaningful_allocations
            )
        else:
            largest = None
            allocation_summary = (
                "No meaningful allocations "
                "were identified."
            )

        sharpe_difference = (
            run.sharpe_ratio
            - run.baseline_sharpe_ratio
        )

        if sharpe_difference > 0.01:
            comparison = (
                "The optimised portfolio achieved "
                "a higher historical Sharpe ratio "
                "than the equal-weight baseline."
            )
        elif sharpe_difference < -0.01:
            comparison = (
                "The optimised portfolio achieved "
                "a lower historical Sharpe ratio "
                "than the equal-weight baseline."
            )
        else:
            comparison = (
                "The optimised portfolio and "
                "equal-weight baseline produced "
                "similar historical Sharpe ratios."
            )

        if run.expected_return < 0:
            return_context = (
                "The historical period produced a "
                "negative annualised return estimate, "
                "so the optimisation should not be "
                "interpreted as predicting positive "
                "future returns."
            )
        else:
            return_context = (
                "The historical period produced a "
                "positive annualised return estimate, "
                "but historical performance does not "
                "predict future returns."
            )

        if largest:
            concentration = (
                f"The largest recommended allocation "
                f"is {largest.symbol} at "
                f"{largest.weight * 100:.1f}%."
            )
        else:
            concentration = ""

        return {
            "summary": (
                f"The genetic algorithm recommends "
                f"the following meaningful allocation: "
                f"{allocation_summary}."
            ),
            "comparison": comparison,
            "risk_context": (
                f"This run used the user's "
                f"{run.risk_profile} investor profile "
                f"when applying portfolio constraints. "
                f"{concentration}"
            ),
            "return_context": return_context,
            "methodology": (
                f"The result was generated from "
                f"{run.historical_days} days of "
                f"historical market data using a "
                f"population of {run.population_size} "
                f"candidate portfolios over "
                f"{run.generations} generations."
            ),
        }