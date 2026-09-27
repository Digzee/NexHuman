class InvestorProfilingService:
    """Calculate investor risk tolerance from questionnaire responses."""

    MIN_ANSWER = 1
    MAX_ANSWER = 5

    LOW_MAX_SCORE = 11
    MODERATE_MAX_SCORE = 18

    QUESTION_FIELDS = (
        "investment_horizon",
        "loss_tolerance",
        "volatility_comfort",
        "investment_experience",
        "growth_preference",
    )

    @classmethod
    def calculate_profile(cls, answers):
        score = sum(
            answers[field]
            for field in cls.QUESTION_FIELDS
        )

        if score <= cls.LOW_MAX_SCORE:
            risk_label = "low"
        elif score <= cls.MODERATE_MAX_SCORE:
            risk_label = "moderate"
        else:
            risk_label = "high"

        return {
            "risk_score": score,
            "risk_label": risk_label,
        }