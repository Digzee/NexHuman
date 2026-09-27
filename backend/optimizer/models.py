from django.conf import settings
from django.db import models

from portfolios.models import Portfolio


class OptimizationRun(models.Model):
    """A persisted NexHuman genetic algorithm optimisation run."""

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="optimization_runs",
    )

    portfolio = models.ForeignKey(
        Portfolio,
        on_delete=models.CASCADE,
        related_name="optimization_runs",
    )

    risk_profile = models.CharField(
        max_length=20,
    )

    historical_days = models.PositiveIntegerField(
        default=365,
    )

    population_size = models.PositiveIntegerField()
    generations = models.PositiveIntegerField()

    expected_return = models.FloatField()
    volatility = models.FloatField()
    sharpe_ratio = models.FloatField()

    baseline_return = models.FloatField()
    baseline_volatility = models.FloatField()
    baseline_sharpe_ratio = models.FloatField()

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return (
            f"Optimisation {self.id} - "
            f"{self.portfolio.name}"
        )


class OptimizationAllocation(models.Model):
    """Recommended asset allocation from an optimisation run."""

    run = models.ForeignKey(
        OptimizationRun,
        on_delete=models.CASCADE,
        related_name="allocations",
    )

    symbol = models.CharField(
        max_length=20,
    )

    weight = models.FloatField()

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["run", "symbol"],
                name="unique_optimization_allocation",
            ),
        ]

    def save(self, *args, **kwargs):
        self.symbol = self.symbol.upper().strip()
        super().save(*args, **kwargs)

    def __str__(self):
        return (
            f"{self.symbol}: "
            f"{self.weight:.2%}"
        )