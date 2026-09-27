from django.conf import settings
from django.db import models


class InvestorProfile(models.Model):
    """Stores a user's investment risk profile."""

    RISK_LOW = "low"
    RISK_MODERATE = "moderate"
    RISK_HIGH = "high"

    RISK_CHOICES = [
        (RISK_LOW, "Low"),
        (RISK_MODERATE, "Moderate"),
        (RISK_HIGH, "High"),
    ]

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="investor_profile",
    )

    investment_horizon = models.PositiveSmallIntegerField()
    loss_tolerance = models.PositiveSmallIntegerField()
    volatility_comfort = models.PositiveSmallIntegerField()
    investment_experience = models.PositiveSmallIntegerField()
    growth_preference = models.PositiveSmallIntegerField()

    risk_score = models.PositiveSmallIntegerField()

    risk_label = models.CharField(
        max_length=20,
        choices=RISK_CHOICES,
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    updated_at = models.DateTimeField(
        auto_now=True,
    )

    def __str__(self):
        return (
            f"{self.user.email} - "
            f"{self.get_risk_label_display()}"
        )