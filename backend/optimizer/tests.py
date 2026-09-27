from django.test import TestCase

from .services.genetic_algorithm import (
    GeneticAlgorithmOptimizer,
)
from .services.optimization_service import (
    OptimizationService,
)


TEST_RETURNS = {
    "BTC": [
        0.010,
        -0.005,
        0.012,
        0.004,
        -0.003,
        0.009,
        0.006,
        -0.002,
        0.011,
        0.005,
    ],
    "ETH": [
        0.014,
        -0.008,
        0.016,
        0.006,
        -0.005,
        0.012,
        0.008,
        -0.004,
        0.015,
        0.007,
    ],
    "SOL": [
        0.020,
        -0.015,
        0.024,
        0.010,
        -0.009,
        0.018,
        0.013,
        -0.007,
        0.022,
        0.011,
    ],
    "XRP": [
        0.006,
        -0.003,
        0.007,
        0.002,
        -0.002,
        0.005,
        0.004,
        -0.001,
        0.006,
        0.003,
    ],
    "ADA": [
        0.008,
        -0.004,
        0.009,
        0.003,
        -0.003,
        0.007,
        0.005,
        -0.002,
        0.008,
        0.004,
    ],
}


class GeneticAlgorithmTests(TestCase):
    def create_optimizer(
        self,
        max_weight=0.60,
        seed=42,
    ):
        return GeneticAlgorithmOptimizer(
            asset_returns=TEST_RETURNS,
            population_size=30,
            generations=20,
            mutation_rate=0.10,
            elite_count=3,
            tournament_size=3,
            max_weight=max_weight,
            seed=seed,
        )

    def test_optimized_weights_sum_to_one(self):
        optimizer = self.create_optimizer()

        result = optimizer.optimise()

        total_weight = sum(
            result["weights"].values()
        )

        self.assertAlmostEqual(
            total_weight,
            1.0,
            places=8,
        )

    def test_optimized_weights_are_long_only(self):
        optimizer = self.create_optimizer()

        result = optimizer.optimise()

        for weight in result["weights"].values():
            self.assertGreaterEqual(
                weight,
                0.0,
            )

    def test_concentration_limit_is_respected(self):
        max_weight = 0.35

        optimizer = self.create_optimizer(
            max_weight=max_weight
        )

        result = optimizer.optimise()

        for weight in result["weights"].values():
            self.assertLessEqual(
                weight,
                max_weight + 1e-8,
            )

    def test_equal_weight_baseline(self):
        optimizer = self.create_optimizer()

        result = (
            optimizer.equal_weight_baseline()
        )

        for weight in result["weights"].values():
            self.assertAlmostEqual(
                weight,
                0.20,
                places=8,
            )

        self.assertAlmostEqual(
            sum(result["weights"].values()),
            1.0,
            places=8,
        )

    def test_optimizer_returns_metrics(self):
        optimizer = self.create_optimizer()

        result = optimizer.optimise()

        self.assertIn(
            "expected_return",
            result,
        )

        self.assertIn(
            "volatility",
            result,
        )

        self.assertIn(
            "sharpe_ratio",
            result,
        )

        self.assertGreaterEqual(
            result["volatility"],
            0.0,
        )

    def test_same_seed_is_reproducible(self):
        first_optimizer = self.create_optimizer(
            seed=123
        )

        second_optimizer = self.create_optimizer(
            seed=123
        )

        first_result = (
            first_optimizer.optimise()
        )

        second_result = (
            second_optimizer.optimise()
        )

        for symbol in TEST_RETURNS:
            self.assertAlmostEqual(
                first_result["weights"][symbol],
                second_result["weights"][symbol],
                places=10,
            )

        self.assertAlmostEqual(
            first_result["sharpe_ratio"],
            second_result["sharpe_ratio"],
            places=10,
        )


class OptimizationServiceTests(TestCase):
    def test_low_profile_uses_lower_concentration_limit(self):
        result = OptimizationService.optimise(
            asset_returns=TEST_RETURNS,
            risk_profile="low",
            seed=42,
        )

        self.assertEqual(
            result["configuration"]["max_weight"],
            0.35,
        )

        for weight in (
            result["optimized"]["weights"].values()
        ):
            self.assertLessEqual(
                weight,
                0.35 + 1e-8,
            )

    def test_moderate_profile_uses_moderate_limit(self):
        result = OptimizationService.optimise(
            asset_returns=TEST_RETURNS,
            risk_profile="moderate",
            seed=42,
        )

        self.assertEqual(
            result["configuration"]["max_weight"],
            0.45,
        )

    def test_high_profile_uses_higher_concentration_limit(self):
        result = OptimizationService.optimise(
            asset_returns=TEST_RETURNS,
            risk_profile="high",
            seed=42,
        )

        self.assertEqual(
            result["configuration"]["max_weight"],
            0.60,
        )

    def test_service_returns_equal_weight_baseline(self):
        result = OptimizationService.optimise(
            asset_returns=TEST_RETURNS,
            risk_profile="moderate",
            seed=42,
        )

        self.assertIn(
            "baseline",
            result,
        )

        self.assertIn(
            "optimized",
            result,
        )

        self.assertAlmostEqual(
            sum(
                result["baseline"][
                    "weights"
                ].values()
            ),
            1.0,
            places=8,
        )


from unittest.mock import patch

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from accounts.models import User
from portfolios.models import Portfolio
from profiling.models import InvestorProfile

from .models import (
    OptimizationAllocation,
    OptimizationRun,
)

class PortfolioOptimizationAPITests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email="optimizer@example.com",
            password="SecureTestPassword123!",
        )

        self.other_user = User.objects.create_user(
            email="other@example.com",
            password="SecureTestPassword123!",
        )

        self.portfolio = Portfolio.objects.create(
            owner=self.user,
            name="Main Portfolio",
        )

        InvestorProfile.objects.create(
            user=self.user,
            investment_horizon=3,
            loss_tolerance=3,
            volatility_comfort=3,
            investment_experience=3,
            growth_preference=3,
            risk_score=15,
            risk_label="moderate",
        )

        self.client.force_authenticate(
            user=self.user
        )

        self.url = reverse(
            "portfolio_optimization",
            kwargs={
                "portfolio_id": self.portfolio.id,
            },
        )

    @patch(
        "optimizer.views."
        "PortfolioOptimizationService.optimise"
    )
    def test_authenticated_user_can_run_optimization(
        self,
        mock_optimise,
    ):
        run = OptimizationRun.objects.create(
            user=self.user,
            portfolio=self.portfolio,
            risk_profile="moderate",
            historical_days=365,
            population_size=100,
            generations=100,
            expected_return=0.25,
            volatility=0.40,
            sharpe_ratio=0.625,
            baseline_return=0.18,
            baseline_volatility=0.45,
            baseline_sharpe_ratio=0.40,
        )

        OptimizationAllocation.objects.create(
            run=run,
            symbol="BTC",
            weight=0.45,
        )

        OptimizationAllocation.objects.create(
            run=run,
            symbol="ETH",
            weight=0.30,
        )

        OptimizationAllocation.objects.create(
            run=run,
            symbol="SOL",
            weight=0.25,
        )

        mock_optimise.return_value = run

        response = self.client.post(
            self.url,
            {},
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED,
        )

        self.assertEqual(
            response.data["risk_profile"],
            "moderate",
        )

        self.assertEqual(
            len(response.data["allocations"]),
            3,
        )

        mock_optimise.assert_called_once_with(
            user=self.user,
            portfolio=self.portfolio,
        )

    def test_user_cannot_optimize_another_users_portfolio(
        self,
    ):
        other_portfolio = Portfolio.objects.create(
            owner=self.other_user,
            name="Private Portfolio",
        )

        url = reverse(
            "portfolio_optimization",
            kwargs={
                "portfolio_id":
                    other_portfolio.id,
            },
        )

        response = self.client.post(
            url,
            {},
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_404_NOT_FOUND,
        )

    def test_unauthenticated_user_cannot_run_optimization(
        self,
    ):
        self.client.force_authenticate(
            user=None
        )

        response = self.client.post(
            self.url,
            {},
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_401_UNAUTHORIZED,
        )

    @patch(
        "optimizer.views."
        "PortfolioOptimizationService.optimise"
    )
    def test_market_data_failure_returns_503(
        self,
        mock_optimise,
    ):
        mock_optimise.side_effect = RuntimeError(
            "Provider unavailable"
        )

        response = self.client.post(
            self.url,
            {},
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_503_SERVICE_UNAVAILABLE,
        )


class OptimizationHistoryAPITests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email="history@example.com",
            password="SecureTestPassword123!",
        )

        self.other_user = User.objects.create_user(
            email="otherhistory@example.com",
            password="SecureTestPassword123!",
        )

        self.portfolio = Portfolio.objects.create(
            owner=self.user,
            name="History Portfolio",
        )

        self.other_portfolio = Portfolio.objects.create(
            owner=self.other_user,
            name="Other Portfolio",
        )

        self.client.force_authenticate(
            user=self.user
        )

    def create_run(
        self,
        user,
        portfolio,
    ):
        return OptimizationRun.objects.create(
            user=user,
            portfolio=portfolio,
            risk_profile="moderate",
            historical_days=365,
            population_size=100,
            generations=100,
            expected_return=0.20,
            volatility=0.35,
            sharpe_ratio=0.57,
            baseline_return=0.15,
            baseline_volatility=0.40,
            baseline_sharpe_ratio=0.375,
        )

    def test_history_only_returns_current_users_runs(
        self,
    ):
        own_run = self.create_run(
            self.user,
            self.portfolio,
        )

        self.create_run(
            self.other_user,
            self.other_portfolio,
        )

        response = self.client.get(
            reverse("optimization_history")
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        self.assertEqual(
            len(response.data),
            1,
        )

        self.assertEqual(
            response.data[0]["id"],
            own_run.id,
        )