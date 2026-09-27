from abc import ABC, abstractmethod


class MarketDataProvider(ABC):
    """Interface for external cryptocurrency market data."""

    @abstractmethod
    def get_current_prices(
        self,
        asset_ids,
        currency="usd",
    ):
        """Return current prices for requested assets."""
        raise NotImplementedError

    @abstractmethod
    def get_historical_prices(
        self,
        asset_id,
        days,
        currency="usd",
    ):
        """Return historical prices for an asset."""
        raise NotImplementedError