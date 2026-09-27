import requests
from django.conf import settings

from .provider import MarketDataProvider


class CoinGeckoProvider(MarketDataProvider):
    """CoinGecko implementation of market data."""

    BASE_URL = "https://api.coingecko.com/api/v3"

    def __init__(self):
        self.api_key = settings.COINGECKO_API_KEY

        if not self.api_key:
            raise ValueError(
                "COINGECKO_API_KEY is not configured."
            )

    def _get(self, endpoint, params=None):
        headers = {
            "x-cg-demo-api-key": self.api_key,
        }

        try:
            response = requests.get(
                f"{self.BASE_URL}{endpoint}",
                headers=headers,
                params=params,
                timeout=10,
            )

            response.raise_for_status()

            return response.json()

        except requests.RequestException as error:
            raise RuntimeError(
                "Unable to retrieve market data."
            ) from error

    def get_current_prices(
        self,
        asset_ids,
        currency="usd",
    ):
        return self._get(
            "/simple/price",
            params={
                "ids": ",".join(asset_ids),
                "vs_currencies": currency,
            },
        )

    def get_historical_prices(
        self,
        asset_id,
        days,
        currency="usd",
    ):
        return self._get(
            f"/coins/{asset_id}/market_chart",
            params={
                "vs_currency": currency,
                "days": days,
            },
        )