from rest_framework import serializers

from .models import (
    OptimizationAllocation,
    OptimizationRun,
)
from .services.recommendation_service import (
    RecommendationService,
)


class OptimizationAllocationSerializer(
    serializers.ModelSerializer
):
    percentage = serializers.SerializerMethodField()

    class Meta:
        model = OptimizationAllocation

        fields = (
            "symbol",
            "weight",
            "percentage",
        )

    def get_percentage(self, obj):
        return obj.weight * 100


class OptimizationRunSerializer(
    serializers.ModelSerializer
):
    allocations = (
        OptimizationAllocationSerializer(
            many=True,
            read_only=True,
        )
    )

    explanation = serializers.SerializerMethodField()

    class Meta:
        model = OptimizationRun

        fields = (
            "id",
            "portfolio",
            "risk_profile",
            "historical_days",
            "population_size",
            "generations",
            "expected_return",
            "volatility",
            "sharpe_ratio",
            "baseline_return",
            "baseline_volatility",
            "baseline_sharpe_ratio",
            "allocations",
            "explanation",
            "created_at",
        )

    def get_explanation(self, obj):
        return RecommendationService.generate(
            obj
        )