from decimal import Decimal
from unittest.mock import patch

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from accounts.models import User
from market_data.models import Cryptocurrency

from .models import Portfolio, PortfolioAsset
from .services.portfolio_valuation_service import (
    PortfolioValuationService,
)


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

        self.assertEqual(
            response.data["symbol"],
            "ETH",
        )

        self.assertTrue(
            PortfolioAsset.objects.filter(
                portfolio=self.portfolio,
                symbol="ETH",
            ).exists()
        )

    def test_unsupported_asset_is_rejected(self):
        response = self.client.post(
            reverse(
                "portfolio_asset_list_create",
                kwargs={
                    "portfolio_pk": self.portfolio.pk,
                },
            ),
            {
                "symbol": "BANANA123",
                "quantity": "1",
                "average_purchase_price": "10",
            },
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST,
        )

        self.assertIn(
            "symbol",
            response.data,
        )

        self.assertFalse(
            PortfolioAsset.objects.filter(
                portfolio=self.portfolio,
                symbol="BANANA123",
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


class FakeMarketDataService:
    def get_current_prices(
        self,
        asset_ids,
        currency="usd",
    ):
        return {
            "bitcoin": {
                "usd": 70000,
            },
            "ethereum": {
                "usd": 3500,
            },
        }


class PortfolioValuationServiceTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email="valuation@example.com",
            password="SecureTestPassword123!",
        )

        self.portfolio = Portfolio.objects.create(
            name="Valuation Portfolio",
            owner=self.user,
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

        PortfolioAsset.objects.create(
            portfolio=self.portfolio,
            symbol="BTC",
            quantity="0.25",
            average_purchase_price="65000",
        )

        PortfolioAsset.objects.create(
            portfolio=self.portfolio,
            symbol="ETH",
            quantity="2",
            average_purchase_price="3000",
        )

        self.service = PortfolioValuationService(
            market_data_service=FakeMarketDataService()
        )

    def test_portfolio_valuation_is_calculated_correctly(self):
        valuation = self.service.value_portfolio(
            self.portfolio
        )

        self.assertEqual(
            valuation["total_value"],
            Decimal("24500.00"),
        )

        self.assertEqual(
            valuation["known_cost_basis"],
            Decimal("22250.00"),
        )

        self.assertEqual(
            valuation["profit_loss"],
            Decimal("2250.00"),
        )

        self.assertAlmostEqual(
            valuation["return_percentage"],
            Decimal("10.1123595506"),
            places=6,
        )

        self.assertEqual(
            len(valuation["assets"]),
            2,
        )

        self.assertEqual(
            valuation["cost_basis_coverage_percentage"],
            Decimal("100"),
        )

        btc = next(
            asset
            for asset in valuation["assets"]
            if asset["symbol"] == "BTC"
        )

        eth = next(
            asset
            for asset in valuation["assets"]
            if asset["symbol"] == "ETH"
        )

        self.assertAlmostEqual(
            btc["allocation_percentage"],
            Decimal("71.4285714286"),
            places=6,
        )

        self.assertAlmostEqual(
            eth["allocation_percentage"],
            Decimal("28.5714285714"),
            places=6,
        )

        total_allocation = sum(
            asset["allocation_percentage"]
            for asset in valuation["assets"]
        )

        self.assertAlmostEqual(
            total_allocation,
            Decimal("100"),
            places=6,
        )

    def test_empty_portfolio_returns_zero_valuation(self):
        empty_portfolio = Portfolio.objects.create(
            name="Empty Portfolio",
            owner=self.user,
        )

        valuation = self.service.value_portfolio(
            empty_portfolio
        )

        self.assertEqual(
            valuation["total_value"],
            Decimal("0"),
        )

        self.assertEqual(
            valuation["known_cost_basis"],
            Decimal("0"),
        )

        self.assertEqual(
            valuation["profit_loss"],
            Decimal("0"),
        )

        self.assertIsNone(
            valuation["return_percentage"]
        )

    def test_missing_purchase_price_does_not_distort_return(self):
        PortfolioAsset.objects.filter(
            portfolio=self.portfolio,
            symbol="ETH",
        ).update(
            average_purchase_price=None
        )

        valuation = self.service.value_portfolio(
            self.portfolio
        )

        self.assertEqual(
            valuation["total_value"],
            Decimal("24500.00"),
        )

        self.assertEqual(
            valuation["known_cost_basis"],
            Decimal("16250.00"),
        )

        self.assertEqual(
            valuation["known_basis_value"],
            Decimal("17500.00"),
        )

        self.assertEqual(
            valuation["profit_loss"],
            Decimal("1250.00"),
        )

        self.assertAlmostEqual(
            valuation["return_percentage"],
            Decimal("7.6923076923"),
            places=6,
        )

        self.assertAlmostEqual(
            valuation["cost_basis_coverage_percentage"],
            Decimal("71.4285714286"),
            places=6,
        )


class PortfolioValuationAPITests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email="valuation-api@example.com",
            password="SecureTestPassword123!",
        )

        self.other_user = User.objects.create_user(
            email="valuation-other@example.com",
            password="SecureTestPassword123!",
        )

        self.portfolio = Portfolio.objects.create(
            name="API Valuation Portfolio",
            owner=self.user,
        )

        self.other_portfolio = Portfolio.objects.create(
            name="Private Portfolio",
            owner=self.other_user,
        )

        self.client.force_authenticate(
            user=self.user
        )

    @patch(
        "portfolios.views.PortfolioValuationService.value_portfolio"
    )
    def test_user_can_get_portfolio_valuation(
        self,
        mock_value_portfolio,
    ):
        mock_value_portfolio.return_value = {
            "total_value": Decimal("24500"),
            "known_cost_basis": Decimal("22250"),
            "known_basis_value": Decimal("24500"),
            "profit_loss": Decimal("2250"),
            "return_percentage": Decimal("10.11235955"),
            "cost_basis_coverage_percentage":
                Decimal("100"),
            "assets": [],
        }

        response = self.client.get(
            reverse(
                "portfolio_valuation",
                kwargs={"pk": self.portfolio.pk},
            )
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        self.assertEqual(
            Decimal(response.data["total_value"]),
            Decimal("24500"),
        )

        mock_value_portfolio.assert_called_once()

    def test_user_cannot_get_another_users_valuation(self):
        response = self.client.get(
            reverse(
                "portfolio_valuation",
                kwargs={
                    "pk": self.other_portfolio.pk,
                },
            )
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_404_NOT_FOUND,
        )

    def test_unauthenticated_user_cannot_get_valuation(self):
        self.client.force_authenticate(
            user=None
        )

        response = self.client.get(
            reverse(
                "portfolio_valuation",
                kwargs={"pk": self.portfolio.pk},
            )
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_401_UNAUTHORIZED,
        )