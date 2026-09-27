from django.contrib import admin

from .models import Portfolio, PortfolioAsset


class PortfolioAssetInline(admin.TabularInline):
    model = PortfolioAsset
    extra = 0


@admin.register(Portfolio)
class PortfolioAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "owner",
        "created_at",
        "updated_at",
    )

    search_fields = (
        "name",
        "owner__email",
    )

    list_filter = (
        "created_at",
        "updated_at",
    )

    inlines = (PortfolioAssetInline,)


@admin.register(PortfolioAsset)
class PortfolioAssetAdmin(admin.ModelAdmin):
    list_display = (
        "symbol",
        "portfolio",
        "quantity",
        "average_purchase_price",
        "updated_at",
    )

    search_fields = (
        "symbol",
        "portfolio__name",
        "portfolio__owner__email",
    )

    list_filter = (
        "symbol",
        "created_at",
        "updated_at",
    )