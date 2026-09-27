from django.contrib import admin

from .models import Cryptocurrency


@admin.register(Cryptocurrency)
class CryptocurrencyAdmin(admin.ModelAdmin):
    list_display = (
        "symbol",
        "name",
        "provider_id",
        "is_active",
    )

    list_filter = (
        "is_active",
    )

    search_fields = (
        "symbol",
        "name",
        "provider_id",
    )