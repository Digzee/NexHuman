from django.contrib import admin

from .models import (
    OptimizationAllocation,
    OptimizationRun,
)


class OptimizationAllocationInline(
    admin.TabularInline
):
    model = OptimizationAllocation
    extra = 0
    readonly_fields = (
        "symbol",
        "weight",
    )


@admin.register(OptimizationRun)
class OptimizationRunAdmin(
    admin.ModelAdmin
):
    list_display = (
        "id",
        "user",
        "portfolio",
        "risk_profile",
        "sharpe_ratio",
        "created_at",
    )

    list_filter = (
        "risk_profile",
        "created_at",
    )

    search_fields = (
        "user__email",
        "portfolio__name",
    )

    readonly_fields = (
        "created_at",
    )

    inlines = [
        OptimizationAllocationInline
    ]