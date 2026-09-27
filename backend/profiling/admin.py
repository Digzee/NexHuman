from django.contrib import admin

from .models import InvestorProfile


@admin.register(InvestorProfile)
class InvestorProfileAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "risk_score",
        "risk_label",
        "updated_at",
    )

    list_filter = (
        "risk_label",
    )

    search_fields = (
        "user__email",
    )

    readonly_fields = (
        "risk_score",
        "risk_label",
        "created_at",
        "updated_at",
    )