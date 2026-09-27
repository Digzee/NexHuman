from .coingecko import CoinGeckoProvider


class MarketDataService:
    """Provides market data to the NexHuman application."""

    def __init__(self, provider=None):
        self.provider = provider or CoinGeckoProvider()

    def get_current_prices(
        self,
        asset_ids,
        currency="usd",
    ):
        return self.provider.get_current_prices(
            asset_ids,
            currency,
        )

    def get_historical_prices(
        self,
        asset_id,
        days,
        currency="usd",
    ):
        return self.provider.get_historical_prices(
            asset_id,
            days,
            currency,
        )