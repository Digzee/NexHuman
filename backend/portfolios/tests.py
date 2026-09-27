from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from accounts.models import User

from .models import Portfolio, PortfolioAsset


class PortfolioAPITests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email="portfolio@example.com",
            password="SecureTestPassword123!",
            first_name="Portfolio",
            last_name="User",
        )

        self.other_user = User.objects.create_user(
            email="other@example.com",
            password="SecureTestPassword123!",
            first_name="Other",
            last_name="User",
        )

        self.portfolio = Portfolio.objects.create(
            name="Main Portfolio",
            owner=self.user,
        )

        self.other_portfolio = Portfolio.objects.create(
            name="Private Portfolio",
            owner=self.other_user,
        )

        self.asset = PortfolioAsset.objects.create(
            portfolio=self.portfolio,
            symbol="BTC",
            quantity="0.25",
            average_purchase_price="65000",
        )

        self.client.force_authenticate(user=self.user)

    def test_user_can_list_only_their_portfolios(self):
        response = self.client.get(
            reverse("portfolio_list_create")
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )
        self.assertEqual(len(response.data), 1)
        self.assertEqual(
            response.data[0]["name"],
            "Main Portfolio",
        )

    def test_user_can_create_portfolio(self):
        response = self.client.post(
            reverse("portfolio_list_create"),
            {"name": "Growth Portfolio"},
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED,
        )

        portfolio = Portfolio.objects.get(
            name="Growth Portfolio"
        )

        self.assertEqual(portfolio.owner, self.user)

    def test_user_cannot_access_another_users_portfolio(self):
        response = self.client.get(
            reverse(
                "portfolio_detail",
                kwargs={"pk": self.other_portfolio.pk},
            )
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_404_NOT_FOUND,
        )

    def test_unauthenticated_user_cannot_access_portfolios(self):
        self.client.force_authenticate(user=None)

        response = self.client.get(
            reverse("portfolio_list_create")
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_401_UNAUTHORIZED,
        )


class PortfolioAssetAPITests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email="assets@example.com",
            password="SecureTestPassword123!",
        )

        self.other_user = User.objects.create_user(
            email="other-assets@example.com",
            password="SecureTestPassword123!",
        )

        self.portfolio = Portfolio.objects.create(
            name="Main Portfolio",
            owner=self.user,
        )

        self.other_portfolio = Portfolio.objects.create(
            name="Other Portfolio",
            owner=self.other_user,
        )

        self.asset = PortfolioAsset.objects.create(
            portfolio=self.portfolio,
            symbol="BTC",
            quantity="0.25",
            average_purchase_price="65000",
        )

        self.client.force_authenticate(user=self.user)

    def test_user_can_add_asset_to_own_portfolio(self):
        response = self.client.post(
            reverse(
                "portfolio_asset_list_create",
                kwargs={"portfolio_pk": self.portfolio.pk},
            ),
            {
                "symbol": "eth",
                "quantity": "2.5",
                "average_purchase_price": "3200",
            },
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED,
        )
        self.assertEqual(response.data["symbol"], "ETH")

        self.assertTrue(
            PortfolioAsset.objects.filter(
                portfolio=self.portfolio,
                symbol="ETH",
            ).exists()
        )

    def test_duplicate_asset_is_rejected(self):
        response = self.client.post(
            reverse(
                "portfolio_asset_list_create",
                kwargs={"portfolio_pk": self.portfolio.pk},
            ),
            {
                "symbol": "btc",
                "quantity": "1",
                "average_purchase_price": "70000",
            },
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST,
        )

    def test_user_cannot_add_asset_to_another_users_portfolio(self):
        response = self.client.post(
            reverse(
                "portfolio_asset_list_create",
                kwargs={
                    "portfolio_pk": self.other_portfolio.pk,
                },
            ),
            {
                "symbol": "ETH",
                "quantity": "1",
                "average_purchase_price": "3000",
            },
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_404_NOT_FOUND,
        )

        self.assertFalse(
            PortfolioAsset.objects.filter(
                portfolio=self.other_portfolio,
                symbol="ETH",
            ).exists()
        )

    def test_user_can_update_own_asset(self):
        response = self.client.patch(
            reverse(
                "portfolio_asset_detail",
                kwargs={
                    "portfolio_pk": self.portfolio.pk,
                    "pk": self.asset.pk,
                },
            ),
            {"quantity": "0.5"},
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        self.asset.refresh_from_db()

        self.assertEqual(
            str(self.asset.quantity),
            "0.500000000000",
        )

    def test_user_can_delete_own_asset(self):
        response = self.client.delete(
            reverse(
                "portfolio_asset_detail",
                kwargs={
                    "portfolio_pk": self.portfolio.pk,
                    "pk": self.asset.pk,
                },
            )
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_204_NO_CONTENT,
        )

        self.assertFalse(
            PortfolioAsset.objects.filter(
                pk=self.asset.pk
            ).exists()
        )