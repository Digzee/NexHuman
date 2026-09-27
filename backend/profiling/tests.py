from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from accounts.models import User

from .models import InvestorProfile
from .services import InvestorProfilingService


class InvestorProfilingServiceTests(APITestCase):
    def test_low_risk_profile(self):
        answers = {
            "investment_horizon": 1,
            "loss_tolerance": 2,
            "volatility_comfort": 2,
            "investment_experience": 2,
            "growth_preference": 2,
        }

        result = (
            InvestorProfilingService.calculate_profile(
                answers
            )
        )

        self.assertEqual(
            result["risk_score"],
            9,
        )

        self.assertEqual(
            result["risk_label"],
            "low",
        )

    def test_moderate_risk_profile(self):
        answers = {
            "investment_horizon": 3,
            "loss_tolerance": 3,
            "volatility_comfort": 3,
            "investment_experience": 3,
            "growth_preference": 3,
        }

        result = (
            InvestorProfilingService.calculate_profile(
                answers
            )
        )

        self.assertEqual(
            result["risk_score"],
            15,
        )

        self.assertEqual(
            result["risk_label"],
            "moderate",
        )

    def test_high_risk_profile(self):
        answers = {
            "investment_horizon": 5,
            "loss_tolerance": 5,
            "volatility_comfort": 4,
            "investment_experience": 4,
            "growth_preference": 4,
        }

        result = (
            InvestorProfilingService.calculate_profile(
                answers
            )
        )

        self.assertEqual(
            result["risk_score"],
            22,
        )

        self.assertEqual(
            result["risk_label"],
            "high",
        )


class InvestorProfileAPITests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email="profile@example.com",
            password="SecureTestPassword123!",
        )

        self.client.force_authenticate(
            user=self.user
        )

        self.url = reverse(
            "investor_profile"
        )

        self.answers = {
            "investment_horizon": 3,
            "loss_tolerance": 3,
            "volatility_comfort": 3,
            "investment_experience": 3,
            "growth_preference": 3,
        }

    def test_user_can_create_profile(self):
        response = self.client.post(
            self.url,
            self.answers,
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        self.assertEqual(
            response.data["risk_score"],
            15,
        )

        self.assertEqual(
            response.data["risk_label"],
            "moderate",
        )

        self.assertEqual(
            InvestorProfile.objects.count(),
            1,
        )

    def test_user_can_get_profile(self):
        self.client.post(
            self.url,
            self.answers,
            format="json",
        )

        response = self.client.get(
            self.url
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        self.assertEqual(
            response.data["risk_score"],
            15,
        )

    def test_resubmission_updates_existing_profile(self):
        self.client.post(
            self.url,
            self.answers,
            format="json",
        )

        updated_answers = {
            "investment_horizon": 5,
            "loss_tolerance": 5,
            "volatility_comfort": 5,
            "investment_experience": 5,
            "growth_preference": 5,
        }

        response = self.client.post(
            self.url,
            updated_answers,
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

        self.assertEqual(
            response.data["risk_score"],
            25,
        )

        self.assertEqual(
            response.data["risk_label"],
            "high",
        )

        self.assertEqual(
            InvestorProfile.objects.count(),
            1,
        )

    def test_invalid_response_is_rejected(self):
        invalid_answers = {
            **self.answers,
            "loss_tolerance": 6,
        }

        response = self.client.post(
            self.url,
            invalid_answers,
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST,
        )

    def test_missing_profile_returns_404(self):
        response = self.client.get(
            self.url
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_404_NOT_FOUND,
        )

    def test_unauthenticated_user_cannot_access_profile(self):
        self.client.force_authenticate(
            user=None
        )

        response = self.client.get(
            self.url
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_401_UNAUTHORIZED,
        )