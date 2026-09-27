from unittest.mock import Mock

from django.core.cache import cache
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from accounts.models import User

from .models import Cryptocurrency
from .services.market_data_service import (
    MarketDataService,
)


class CryptocurrencyAPITests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email="marketdata@example.com",
            password="SecureTestPassword123!",
        )

        Cryptocurrency.objects.create(
            symbol="BTC",
            name="Bitcoin",
            provider_id="bitcoin",
        )

        Cryptocurrency.objects.create(
            symbol="ETH",
            name="Ethereum",
            provider_id="ethereum",
        )

        Cryptocurrency.objects.create(
            symbol="OLD",
            name="Inactive Asset",
            provider_id="inactive-asset",
            is_active=False,
        )

        self.client.force_authenticate(
            user=self.user
        )

    def test_authenticated_user_can_list_supported_assets(self):
        response = self.client.get(
            reverse("cryptocurrency_list")
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        self.assertEqual(
            len(response.data),
            2,
        )

        symbols = [
            asset["symbol"]
            for asset in response.data
        ]

        self.assertIn("BTC", symbols)
        self.assertIn("ETH", symbols)
        self.assertNotIn("OLD", symbols)

    def test_provider_id_is_not_exposed(self):
        response = self.client.get(
            reverse("cryptocurrency_list")
        )

        self.assertNotIn(
            "provider_id",
            response.data[0],
        )

    def test_unauthenticated_user_cannot_list_supported_assets(self):
        self.client.force_authenticate(
            user=None
        )

        response = self.client.get(
            reverse("cryptocurrency_list")
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_401_UNAUTHORIZED,
        )


class MarketDataServiceCacheTests(TestCase):
    def setUp(self):
        cache.clear()

        self.provider = Mock()

        self.service = MarketDataService(
            provider=self.provider
        )

    def tearDown(self):
        cache.clear()

    def test_current_prices_are_cached(self):
        expected_data = {
            "bitcoin": {
                "usd": 70000,
            },
            "ethereum": {
                "usd": 3500,
            },
        }

        self.provider.get_current_prices.return_value = (
            expected_data
        )

        first_result = self.service.get_current_prices(
            ["bitcoin", "ethereum"]
        )

        second_result = self.service.get_current_prices(
            ["bitcoin", "ethereum"]
        )

        self.assertEqual(
            first_result,
            expected_data,
        )

        self.assertEqual(
            second_result,
            expected_data,
        )

        self.provider.get_current_prices.assert_called_once_with(
            ["bitcoin", "ethereum"],
            "usd",
        )

    def test_historical_prices_are_cached(self):
        expected_data = {
            "prices": [
                [1000, 65000],
                [2000, 66000],
            ],
        }

        self.provider.get_historical_prices.return_value = (
            expected_data
        )

        first_result = (
            self.service.get_historical_prices(
                "bitcoin",
                30,
            )
        )

        second_result = (
            self.service.get_historical_prices(
                "bitcoin",
                30,
            )
        )

        self.assertEqual(
            first_result,
            expected_data,
        )

        self.assertEqual(
            second_result,
            expected_data,
        )

        self.provider.get_historical_prices.assert_called_once_with(
            "bitcoin",
            30,
            "usd",
        )

    def test_historical_periods_use_separate_cache_entries(self):
        thirty_day_data = {
            "prices": [
                [1000, 65000],
            ],
        }

        ninety_day_data = {
            "prices": [
                [1000, 60000],
                [2000, 65000],
            ],
        }

        self.provider.get_historical_prices.side_effect = [
            thirty_day_data,
            ninety_day_data,
        ]

        thirty_day_result = (
            self.service.get_historical_prices(
                "bitcoin",
                30,
            )
        )

        ninety_day_result = (
            self.service.get_historical_prices(
                "bitcoin",
                90,
            )
        )

        self.assertEqual(
            thirty_day_result,
            thirty_day_data,
        )

        self.assertEqual(
            ninety_day_result,
            ninety_day_data,
        )

        self.assertEqual(
            self.provider.get_historical_prices.call_count,
            2,
        )

    def test_current_price_cache_is_independent_of_asset_order(self):
        expected_data = {
            "bitcoin": {
                "usd": 70000,
            },
            "ethereum": {
                "usd": 3500,
            },
        }

        self.provider.get_current_prices.return_value = (
            expected_data
        )

        first_result = self.service.get_current_prices(
            ["bitcoin", "ethereum"]
        )

        second_result = self.service.get_current_prices(
            ["ethereum", "bitcoin"]
        )

        self.assertEqual(
            first_result,
            expected_data,
        )

        self.assertEqual(
            second_result,
            expected_data,
        )

        self.provider.get_current_prices.assert_called_once_with(
            ["bitcoin", "ethereum"],
            "usd",
        )