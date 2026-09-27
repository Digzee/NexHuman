from rest_framework import serializers

from market_data.models import Cryptocurrency

from .models import Portfolio, PortfolioAsset


class PortfolioAssetSerializer(serializers.ModelSerializer):
    class Meta:
        model = PortfolioAsset
        fields = (
            "id",
            "symbol",
            "quantity",
            "average_purchase_price",
            "created_at",
            "updated_at",
        )
        read_only_fields = (
            "id",
            "created_at",
            "updated_at",
        )

    def validate_symbol(self, value):
        symbol = value.upper().strip()

        if not Cryptocurrency.objects.filter(
            symbol=symbol,
            is_active=True,
        ).exists():
            raise serializers.ValidationError(
                "This cryptocurrency is not supported."
            )

        return symbol

    def validate(self, attrs):
        portfolio = self.context.get("portfolio")

        if not portfolio:
            return attrs

        symbol = attrs.get(
            "symbol",
            getattr(self.instance, "symbol", None),
        )

        if symbol:
            existing_assets = PortfolioAsset.objects.filter(
                portfolio=portfolio,
                symbol__iexact=symbol,
            )

            if self.instance:
                existing_assets = existing_assets.exclude(
                    pk=self.instance.pk
                )

            if existing_assets.exists():
                raise serializers.ValidationError(
                    {
                        "symbol": (
                            "This asset already exists in "
                            "the portfolio."
                        )
                    }
                )

        return attrs


class PortfolioSerializer(serializers.ModelSerializer):
    assets = PortfolioAssetSerializer(
        many=True,
        read_only=True,
    )

    class Meta:
        model = Portfolio
        fields = (
            "id",
            "name",
            "assets",
            "created_at",
            "updated_at",
        )
        read_only_fields = (
            "id",
            "assets",
            "created_at",
            "updated_at",
        )