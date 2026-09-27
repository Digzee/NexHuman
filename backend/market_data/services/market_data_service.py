from django.core.cache import cache

from .coingecko import CoinGeckoProvider


class MarketDataService:
    """Provide cached market data to the NexHuman application."""

    CURRENT_PRICE_CACHE_SECONDS = 60
    HISTORICAL_PRICE_CACHE_SECONDS = 3600

    def __init__(self, provider=None):
        self.provider = provider or CoinGeckoProvider()

    def get_current_prices(
        self,
        asset_ids,
        currency="usd",
    ):
        normalised_asset_ids = sorted(
            {
                asset_id.lower().strip()
                for asset_id in asset_ids
            }
        )

        if not normalised_asset_ids:
            return {}

        cache_key = self._build_current_price_cache_key(
            normalised_asset_ids,
            currency,
        )

        cached_data = cache.get(cache_key)

        if cached_data is not None:
            return cached_data

        data = self.provider.get_current_prices(
            normalised_asset_ids,
            currency,
        )

        cache.set(
            cache_key,
            data,
            timeout=self.CURRENT_PRICE_CACHE_SECONDS,
        )

        return data

    def get_historical_prices(
        self,
        asset_id,
        days,
        currency="usd",
    ):
        normalised_asset_id = (
            asset_id.lower().strip()
        )

        cache_key = (
            self._build_historical_price_cache_key(
                normalised_asset_id,
                days,
                currency,
            )
        )

        cached_data = cache.get(cache_key)

        if cached_data is not None:
            return cached_data

        data = self.provider.get_historical_prices(
            normalised_asset_id,
            days,
            currency,
        )

        cache.set(
            cache_key,
            data,
            timeout=(
                self.HISTORICAL_PRICE_CACHE_SECONDS
            ),
        )

        return data

    @staticmethod
    def _build_current_price_cache_key(
        asset_ids,
        currency,
    ):
        assets = "-".join(asset_ids)

        return (
            f"market-data:current:"
            f"{currency.lower()}:{assets}"
        )

    @staticmethod
    def _build_historical_price_cache_key(
        asset_id,
        days,
        currency,
    ):
        return (
            f"market-data:historical:"
            f"{currency.lower()}:"
            f"{asset_id}:{days}"
        )