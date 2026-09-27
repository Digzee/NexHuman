from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from accounts.models import User

from .models import Cryptocurrency


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