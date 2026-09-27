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
from .services.portfolio_performance_service import (
    PortfolioPerformanceService,
)
from portfolios.services.portfolio_risk_service import (
    PortfolioRiskService,
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

class FakeHistoricalMarketDataService:
    """Provide deterministic historical prices for testing."""

    def get_historical_prices(
        self,
        asset_id,
        days,
        currency="usd",
    ):
        histories = {
            "bitcoin": {
                "prices": [
                    [1756684800000, 60000],
                    [1756771200000, 62000],
                    [1756857600000, 64000],
                ],
            },
            "ethereum": {
                "prices": [
                    [1756684800000, 3000],
                    [1756771200000, 3100],
                    [1756857600000, 3200],
                ],
            },
        }

        return histories.get(
            asset_id,
            {"prices": []},
        )

class FakeMisalignedHistoricalMarketDataService:
    """Provide historical data with a missing asset date."""

    def get_historical_prices(
        self,
        asset_id,
        days,
        currency="usd",
    ):
        histories = {
            "bitcoin": {
                "prices": [
                    [1756684800000, 60000],
                    [1756771200000, 62000],
                    [1756857600000, 64000],
                ],
            },
            "ethereum": {
                "prices": [
                    [1756684800000, 3000],
                    [1756857600000, 3200],
                ],
            },
        }

        return histories.get(
            asset_id,
            {"prices": []},
        )

class FakeIncompleteHistoricalMarketDataService:
    """Provide no historical data for one portfolio asset."""

    def get_historical_prices(
        self,
        asset_id,
        days,
        currency="usd",
    ):
        histories = {
            "bitcoin": {
                "prices": [
                    [1756684800000, 60000],
                    [1756771200000, 62000],
                    [1756857600000, 64000],
                ],
            },
            "ethereum": {
                "prices": [],
            },
        }

        return histories.get(
            asset_id,
            {"prices": []},
        )

class FakeDrawdownHistoricalMarketDataService:
    """Historical data containing a clear peak-to-trough decline."""

    def get_historical_prices(
        self,
        asset_id,
        days,
        currency="usd",
    ):
        prices = {
            "bitcoin": [
                [1756684800000, 100],
                [1756771200000, 120],
                [1756857600000, 90],
                [1756944000000, 110],
            ],
        }

        return {
            "prices": prices.get(
                asset_id,
                []
            ),
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

class PortfolioPerformanceServiceTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email="performance@example.com",
            password="SecureTestPassword123!",
        )

        self.portfolio = Portfolio.objects.create(
            name="Performance Portfolio",
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
            average_purchase_price="55000",
        )

        PortfolioAsset.objects.create(
            portfolio=self.portfolio,
            symbol="ETH",
            quantity="2",
            average_purchase_price="2800",
        )

        self.service = PortfolioPerformanceService(
            market_data_service=(
                FakeHistoricalMarketDataService()
            )
        )

    def test_historical_performance_is_calculated_correctly(
        self,
    ):
        performance = (
            self.service.calculate_performance(
                self.portfolio,
                days=30,
            )
        )

        self.assertEqual(
            performance["period_days"],
            30,
        )

        self.assertEqual(
            len(performance["data_points"]),
            3,
        )

        self.assertEqual(
            performance["starting_value"],
            Decimal("21000.00"),
        )

        self.assertEqual(
            performance["ending_value"],
            Decimal("22400.00"),
        )

        self.assertAlmostEqual(
            performance[
                "total_return_percentage"
            ],
            Decimal("6.6666666667"),
            places=6,
        )

    def test_historical_data_points_are_correct(
        self,
    ):
        performance = (
            self.service.calculate_performance(
                self.portfolio,
                days=30,
            )
        )

        values = [
            point["value"]
            for point in performance["data_points"]
        ]

        self.assertEqual(
            values,
            [
                Decimal("21000.00"),
                Decimal("21700.00"),
                Decimal("22400.00"),
            ],
        )

    def test_empty_portfolio_returns_empty_performance(
        self,
    ):
        empty_portfolio = Portfolio.objects.create(
            name="Empty Performance Portfolio",
            owner=self.user,
        )

        performance = (
            self.service.calculate_performance(
                empty_portfolio,
                days=30,
            )
        )

        self.assertEqual(
            performance["starting_value"],
            Decimal("0"),
        )

        self.assertEqual(
            performance["ending_value"],
            Decimal("0"),
        )

        self.assertIsNone(
            performance[
                "total_return_percentage"
            ]
        )

        self.assertEqual(
            performance["data_points"],
            [],
        )

    def test_missing_asset_date_is_excluded(
        self,
    ):
        service = PortfolioPerformanceService(
            market_data_service=(
                FakeMisalignedHistoricalMarketDataService()
            )
        )

        performance = service.calculate_performance(
            self.portfolio,
            days=30,
        )

        self.assertEqual(
            len(performance["data_points"]),
            2,
        )

        values = [
            point["value"]
            for point in performance["data_points"]
        ]

        self.assertEqual(
            values,
            [
                Decimal("21000.00"),
                Decimal("22400.00"),
            ],
        )

    def test_missing_asset_history_returns_empty_performance(
        self,
    ):
        service = PortfolioPerformanceService(
            market_data_service=(
                FakeIncompleteHistoricalMarketDataService()
            )
        )

        performance = service.calculate_performance(
            self.portfolio,
            days=30,
        )

        self.assertEqual(
            performance["starting_value"],
            Decimal("0"),
        )

        self.assertEqual(
            performance["ending_value"],
            Decimal("0"),
        )

        self.assertIsNone(
            performance["total_return_percentage"]
        )

        self.assertEqual(
            performance["data_points"],
            [],
        )
        
    def test_performance_calculates_annualised_return(self):
        service = PortfolioPerformanceService(
            market_data_service=(
                FakeHistoricalMarketDataService()
            )
        )

        result = service.calculate_performance(
            self.portfolio,
            days=30,
        )

        self.assertIsNotNone(
            result[
                "annualised_return_percentage"
            ]
        )

        self.assertGreater(
            result[
                "annualised_return_percentage"
            ],
            Decimal("0"),
        )


    def test_performance_calculates_annualised_volatility(self):
        service = PortfolioPerformanceService(
            market_data_service=(
                FakeHistoricalMarketDataService()
            )
        )

        result = service.calculate_performance(
            self.portfolio,
            days=30,
        )

        volatility = result[
            "annualised_volatility_percentage"
        ]

        self.assertIsNotNone(volatility)
        self.assertGreater(
            volatility,
            Decimal("0"),
        )


    def test_performance_calculates_maximum_drawdown(self):
        portfolio = Portfolio.objects.create(
            name="Drawdown Portfolio",
            owner=self.user,
        )

        PortfolioAsset.objects.create(
            portfolio=portfolio,
            symbol="BTC",
            quantity=Decimal("1"),
            average_purchase_price=Decimal(
                "100"
            ),
        )

        service = PortfolioPerformanceService(
            market_data_service=(
                FakeDrawdownHistoricalMarketDataService()
            )
        )

        result = service.calculate_performance(
            portfolio,
            days=30,
        )

        self.assertAlmostEqual(
            float(
                result[
                    "maximum_drawdown_percentage"
                ]
            ),
            -25.0,
            places=6,
        )


    def test_empty_performance_has_no_metrics(self):
        portfolio = Portfolio.objects.create(
            name="Empty Metrics Portfolio",
            owner=self.user,
        )

        service = PortfolioPerformanceService(
            market_data_service=(
                FakeHistoricalMarketDataService()
            )
        )

        result = service.calculate_performance(
            portfolio,
            days=30,
        )

        self.assertIsNone(
            result[
                "total_return_percentage"
            ]
        )
        self.assertIsNone(
            result[
                "annualised_return_percentage"
            ]
        )
        self.assertIsNone(
            result[
                "annualised_volatility_percentage"
            ]
        )
        self.assertIsNone(
            result[
                "maximum_drawdown_percentage"
            ]
        )

class PortfolioRiskServiceTests(
    APITestCase
):
    def setUp(self):
        self.service = PortfolioRiskService()

    def test_equal_weight_portfolio_has_high_diversification(
        self,
    ):
        valuation = {
            "assets": [
                {
                    "allocation_percentage":
                        Decimal("20"),
                },
                {
                    "allocation_percentage":
                        Decimal("20"),
                },
                {
                    "allocation_percentage":
                        Decimal("20"),
                },
                {
                    "allocation_percentage":
                        Decimal("20"),
                },
                {
                    "allocation_percentage":
                        Decimal("20"),
                },
            ],
        }

        performance = {
            "annualised_volatility_percentage":
                Decimal("20"),
            "maximum_drawdown_percentage":
                Decimal("-8"),
        }

        result = self.service.calculate_risk(
            valuation,
            performance,
        )

        self.assertEqual(
            result["concentration_index"],
            Decimal("0.20"),
        )

        self.assertEqual(
            result["diversification_label"],
            "High",
        )

        self.assertEqual(
            result[
                "largest_holding_percentage"
            ],
            Decimal("20"),
        )

        self.assertEqual(
            result["asset_count"],
            5,
        )

    def test_single_asset_portfolio_has_low_diversification(
        self,
    ):
        valuation = {
            "assets": [
                {
                    "allocation_percentage":
                        Decimal("100"),
                },
            ],
        }

        performance = {
            "annualised_volatility_percentage":
                Decimal("30"),
            "maximum_drawdown_percentage":
                Decimal("-15"),
        }

        result = self.service.calculate_risk(
            valuation,
            performance,
        )

        self.assertEqual(
            result["concentration_index"],
            Decimal("1"),
        )

        self.assertEqual(
            result["diversification_label"],
            "Low",
        )

        self.assertEqual(
            result[
                "largest_holding_percentage"
            ],
            Decimal("100"),
        )

    def test_high_risk_portfolio_is_classified_correctly(
        self,
    ):
        valuation = {
            "assets": [
                {
                    "allocation_percentage":
                        Decimal("80"),
                },
                {
                    "allocation_percentage":
                        Decimal("20"),
                },
            ],
        }

        performance = {
            "annualised_volatility_percentage":
                Decimal("85"),
            "maximum_drawdown_percentage":
                Decimal("-45"),
        }

        result = self.service.calculate_risk(
            valuation,
            performance,
        )

        self.assertEqual(
            result["risk_label"],
            "Very High",
        )

    def test_moderate_risk_portfolio_is_classified_correctly(
        self,
    ):
        valuation = {
            "assets": [
                {
                    "allocation_percentage":
                        Decimal("40"),
                },
                {
                    "allocation_percentage":
                        Decimal("35"),
                },
                {
                    "allocation_percentage":
                        Decimal("25"),
                },
            ],
        }

        performance = {
            "annualised_volatility_percentage":
                Decimal("35"),
            "maximum_drawdown_percentage":
                Decimal("-15"),
        }

        result = self.service.calculate_risk(
            valuation,
            performance,
        )

        self.assertEqual(
            result["risk_label"],
            "Moderate",
        )

    def test_missing_metrics_return_unavailable_risk(
        self,
    ):
        valuation = {
            "assets": [],
        }

        performance = {
            "annualised_volatility_percentage":
                None,
            "maximum_drawdown_percentage":
                None,
        }

        result = self.service.calculate_risk(
            valuation,
            performance,
        )

        self.assertEqual(
            result["risk_label"],
            "Unavailable",
        )

        self.assertEqual(
            result["diversification_label"],
            "Unavailable",
        )

        self.assertIsNone(
            result["concentration_index"]
        )

        self.assertIsNone(
            result[
                "largest_holding_percentage"
            ]
        )

        self.assertEqual(
            result["asset_count"],
            0,
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

class PortfolioPerformanceAPITests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email="performance-api@example.com",
            password="SecureTestPassword123!",
        )

        self.other_user = User.objects.create_user(
            email="performance-other@example.com",
            password="SecureTestPassword123!",
        )

        self.portfolio = Portfolio.objects.create(
            name="Performance API Portfolio",
            owner=self.user,
        )

        self.other_portfolio = Portfolio.objects.create(
            name="Private Performance Portfolio",
            owner=self.other_user,
        )

        self.client.force_authenticate(
            user=self.user
        )

    @patch(
        "portfolios.views."
        "PortfolioPerformanceService.calculate_performance"
    )
    def test_user_can_get_portfolio_performance(
        self,
        mock_calculate_performance,
    ):
        mock_calculate_performance.return_value = {
            "period_days": 30,
            "starting_value": Decimal("21000"),
            "ending_value": Decimal("22400"),
            "total_return_percentage":
                Decimal("6.6666666667"),
            "data_points": [
                {
                    "date": "2025-09-01",
                    "value": Decimal("21000"),
                },
                {
                    "date": "2025-09-03",
                    "value": Decimal("22400"),
                },
            ],
        }

        response = self.client.get(
            reverse(
                "portfolio_performance",
                kwargs={"pk": self.portfolio.pk},
            ),
            {"days": 30},
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        self.assertEqual(
            response.data["period_days"],
            30,
        )

        mock_calculate_performance.assert_called_once()

    def test_invalid_performance_period_is_rejected(self):
        response = self.client.get(
            reverse(
                "portfolio_performance",
                kwargs={"pk": self.portfolio.pk},
            ),
            {"days": 45},
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST,
        )

    def test_non_numeric_performance_period_is_rejected(self):
        response = self.client.get(
            reverse(
                "portfolio_performance",
                kwargs={"pk": self.portfolio.pk},
            ),
            {"days": "invalid"},
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST,
        )

    def test_user_cannot_get_another_users_performance(self):
        response = self.client.get(
            reverse(
                "portfolio_performance",
                kwargs={
                    "pk": self.other_portfolio.pk,
                },
            ),
            {"days": 30},
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_404_NOT_FOUND,
        )

    def test_unauthenticated_user_cannot_get_performance(self):
        self.client.force_authenticate(
            user=None
        )

        response = self.client.get(
            reverse(
                "portfolio_performance",
                kwargs={"pk": self.portfolio.pk},
            ),
            {"days": 30},
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_401_UNAUTHORIZED,
        )

class PortfolioRiskAPITests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email="risk-api@example.com",
            password="SecureTestPassword123!",
        )

        self.other_user = User.objects.create_user(
            email="risk-other@example.com",
            password="SecureTestPassword123!",
        )

        self.portfolio = Portfolio.objects.create(
            name="Risk API Portfolio",
            owner=self.user,
        )

        self.other_portfolio = Portfolio.objects.create(
            name="Private Risk Portfolio",
            owner=self.other_user,
        )

        self.client.force_authenticate(
            user=self.user
        )

    @patch(
        "portfolios.views."
        "PortfolioRiskService.calculate_risk"
    )
    @patch(
        "portfolios.views."
        "PortfolioPerformanceService.calculate_performance"
    )
    @patch(
        "portfolios.views."
        "PortfolioValuationService.value_portfolio"
    )
    def test_user_can_get_portfolio_risk(
        self,
        mock_value_portfolio,
        mock_calculate_performance,
        mock_calculate_risk,
    ):
        valuation = {
            "total_value": Decimal("24500"),
            "assets": [
                {
                    "symbol": "BTC",
                    "allocation_percentage":
                        Decimal("70"),
                },
                {
                    "symbol": "ETH",
                    "allocation_percentage":
                        Decimal("30"),
                },
            ],
        }

        performance = {
            "period_days": 30,
            "annualised_volatility_percentage":
                Decimal("60"),
            "maximum_drawdown_percentage":
                Decimal("-20"),
        }

        risk = {
            "risk_label": "High",
            "annualised_volatility_percentage":
                Decimal("60"),
            "maximum_drawdown_percentage":
                Decimal("-20"),
            "largest_holding_percentage":
                Decimal("70"),
            "concentration_index":
                Decimal("0.58"),
            "diversification_label": "Low",
            "asset_count": 2,
        }

        mock_value_portfolio.return_value = (
            valuation
        )

        mock_calculate_performance.return_value = (
            performance
        )

        mock_calculate_risk.return_value = risk

        response = self.client.get(
            reverse(
                "portfolio_risk",
                kwargs={
                    "pk": self.portfolio.pk,
                },
            ),
            {
                "days": 30,
            },
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        self.assertEqual(
            response.data["risk_label"],
            "High",
        )

        self.assertEqual(
            response.data[
                "diversification_label"
            ],
            "Low",
        )

        self.assertEqual(
            response.data["asset_count"],
            2,
        )

        mock_value_portfolio.assert_called_once()

        mock_calculate_performance.assert_called_once_with(
            self.portfolio,
            days=30,
        )

        mock_calculate_risk.assert_called_once_with(
            valuation,
            performance,
        )

    def test_invalid_risk_period_is_rejected(
        self,
    ):
        response = self.client.get(
            reverse(
                "portfolio_risk",
                kwargs={
                    "pk": self.portfolio.pk,
                },
            ),
            {
                "days": 45,
            },
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST,
        )

    def test_non_numeric_risk_period_is_rejected(
        self,
    ):
        response = self.client.get(
            reverse(
                "portfolio_risk",
                kwargs={
                    "pk": self.portfolio.pk,
                },
            ),
            {
                "days": "invalid",
            },
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST,
        )

    def test_user_cannot_get_another_users_risk(
        self,
    ):
        response = self.client.get(
            reverse(
                "portfolio_risk",
                kwargs={
                    "pk":
                        self.other_portfolio.pk,
                },
            ),
            {
                "days": 30,
            },
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_404_NOT_FOUND,
        )

    def test_unauthenticated_user_cannot_get_risk(
        self,
    ):
        self.client.force_authenticate(
            user=None
        )

        response = self.client.get(
            reverse(
                "portfolio_risk",
                kwargs={
                    "pk": self.portfolio.pk,
                },
            ),
            {
                "days": 30,
            },
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_401_UNAUTHORIZED,
        )