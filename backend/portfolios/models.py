from decimal import Decimal

from django.conf import settings
from django.core.validators import MinValueValidator
from django.db import models


class Portfolio(models.Model):
    """An investment portfolio belonging to a NexHuman user."""

    name = models.CharField(
        max_length=100,
    )

    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="portfolios",
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    updated_at = models.DateTimeField(
        auto_now=True,
    )

    def __str__(self):
        return f"{self.name} ({self.owner.email})"


class PortfolioAsset(models.Model):
    """A cryptocurrency holding within a portfolio."""

    portfolio = models.ForeignKey(
        Portfolio,
        on_delete=models.CASCADE,
        related_name="assets",
    )

    symbol = models.CharField(
        max_length=20,
    )

    quantity = models.DecimalField(
        max_digits=30,
        decimal_places=12,
        validators=[
            MinValueValidator(Decimal("0")),
        ],
    )

    average_purchase_price = models.DecimalField(
        max_digits=30,
        decimal_places=8,
        validators=[
            MinValueValidator(Decimal("0")),
        ],
        null=True,
        blank=True,
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    updated_at = models.DateTimeField(
        auto_now=True,
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["portfolio", "symbol"],
                name="unique_asset_per_portfolio",
            ),
        ]

    def save(self, *args, **kwargs):
        self.symbol = self.symbol.upper().strip()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.symbol} - {self.portfolio.name}"