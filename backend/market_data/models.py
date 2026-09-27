from django.db import models


class Cryptocurrency(models.Model):
    """A cryptocurrency supported by NexHuman."""

    symbol = models.CharField(
        max_length=20,
        unique=True,
    )

    name = models.CharField(
        max_length=100,
    )

    provider_id = models.CharField(
        max_length=100,
        unique=True,
    )

    is_active = models.BooleanField(
        default=True,
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    updated_at = models.DateTimeField(
        auto_now=True,
    )

    class Meta:
        ordering = ["symbol"]

    def save(self, *args, **kwargs):
        self.symbol = self.symbol.upper().strip()
        self.provider_id = self.provider_id.lower().strip()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.symbol} - {self.name}"