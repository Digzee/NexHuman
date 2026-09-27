import os

from openai import OpenAI

from optimizer.models import OptimizationRun


class AdvisorService:
    """Generate contextual AI explanations using NexHuman data."""

    SYSTEM_PROMPT = """
You are NexHuman, an educational cryptocurrency portfolio
advisor.

Your role is to help the user understand their portfolio,
investor profile, and NexHuman genetic algorithm results.

Important rules:

1. Base portfolio-specific answers only on the NexHuman
   context supplied to you.
2. Do not invent holdings, prices, allocations, returns,
   optimisation results, or investor-profile information.
3. Clearly distinguish historical results from forecasts.
4. Historical performance does not guarantee future
   performance.
5. Explain financial and optimisation concepts in clear,
   accessible language.
6. Do not claim that a portfolio is guaranteed to make money.
7. Do not tell the user that they must buy or sell an asset.
8. When appropriate, explain how the genetic algorithm,
   investor profile, concentration constraints, Sharpe ratio,
   volatility, and equal-weight baseline affect the result.
9. If information needed to answer the question is not
   available in the supplied context, say so.
10. Keep answers concise and useful.
11. Treat optimisation results as decision-support information,
    not personalised regulated financial advice.
"""

    def __init__(self):
        api_key = os.getenv("OPENAI_API_KEY")

        if not api_key:
            raise RuntimeError(
                "OPENAI_API_KEY is not configured."
            )

        self.client = OpenAI(
            api_key=api_key
        )

        self.model = os.getenv(
            "OPENAI_MODEL",
            "gpt-5.6-luna",
        )

    def ask(self, user, message):
        context = self._build_context(user)

        prompt = f"""
NEXHUMAN USER CONTEXT

{context}

USER QUESTION

{message}
"""

        try:
            response = self.client.responses.create(
                model=self.model,
                instructions=self.SYSTEM_PROMPT,
                input=prompt,
            )
        except Exception as exc:
            raise RuntimeError(
                "The AI advisor is temporarily unavailable."
            ) from exc

        answer = response.output_text

        if not answer:
            raise RuntimeError(
                "The AI advisor returned an empty response."
            )

        return answer.strip()

    def _build_context(self, user):
        sections = [
            self._profile_context(user),
            self._portfolio_context(user),
            self._optimization_context(user),
        ]

        return "\n\n".join(sections)

    def _profile_context(self, user):
        try:
            profile = user.investor_profile
        except Exception:
            return (
                "INVESTOR PROFILE\n"
                "No investor profile is available."
            )

        return (
            "INVESTOR PROFILE\n"
            f"Risk label: {profile.risk_label}\n"
            f"Risk score: {profile.risk_score}/25\n"
            f"Investment horizon score: "
            f"{profile.investment_horizon}/5\n"
            f"Loss tolerance score: "
            f"{profile.loss_tolerance}/5\n"
            f"Volatility comfort score: "
            f"{profile.volatility_comfort}/5\n"
            f"Investment experience score: "
            f"{profile.investment_experience}/5\n"
            f"Growth preference score: "
            f"{profile.growth_preference}/5"
        )

    def _portfolio_context(self, user):
        portfolios = (
            user.portfolios
            .all()
            .prefetch_related("assets")
        )

        if not portfolios.exists():
            return (
                "CURRENT PORTFOLIOS\n"
                "No portfolios are available."
            )

        lines = [
            "CURRENT PORTFOLIOS"
        ]

        for portfolio in portfolios:
            lines.append(
                f"Portfolio: {portfolio.name}"
            )

            assets = portfolio.assets.all()

            if not assets.exists():
                lines.append(
                    "- No assets"
                )
                continue

            for asset in assets:
                lines.append(
                    f"- {asset.symbol}: "
                    f"quantity {asset.quantity}, "
                    f"average purchase price "
                    f"{asset.average_purchase_price}"
                )

        return "\n".join(lines)

    def _optimization_context(self, user):
        run = (
            OptimizationRun.objects
            .filter(user=user)
            .prefetch_related("allocations")
            .first()
        )

        if run is None:
            return (
                "LATEST OPTIMISATION\n"
                "No optimisation result is available."
            )

        lines = [
            "LATEST OPTIMISATION",
            f"Run ID: {run.id}",
            f"Risk profile: {run.risk_profile}",
            (
                "Historical window: "
                f"{run.historical_days} days"
            ),
            (
                "Annualised historical return: "
                f"{run.expected_return * 100:.2f}%"
            ),
            (
                "Annualised historical volatility: "
                f"{run.volatility * 100:.2f}%"
            ),
            (
                "GA Sharpe ratio: "
                f"{run.sharpe_ratio:.3f}"
            ),
            (
                "Equal-weight annualised return: "
                f"{run.baseline_return * 100:.2f}%"
            ),
            (
                "Equal-weight annualised volatility: "
                f"{run.baseline_volatility * 100:.2f}%"
            ),
            (
                "Equal-weight Sharpe ratio: "
                f"{run.baseline_sharpe_ratio:.3f}"
            ),
            "Recommended allocation:",
        ]

        allocations = (
            run.allocations
            .order_by("-weight")
        )

        for allocation in allocations:
            lines.append(
                f"- {allocation.symbol}: "
                f"{allocation.weight * 100:.2f}%"
            )

        return "\n".join(lines)