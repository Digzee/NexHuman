from django.shortcuts import get_object_or_404

from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Portfolio, PortfolioAsset
from .serializers import (
    PortfolioAssetSerializer,
    PortfolioSerializer,
)
from .services.portfolio_performance_service import (
    PortfolioPerformanceService,
)
from .services.portfolio_risk_service import (
    PortfolioRiskService,
)
from .services.portfolio_valuation_service import (
    PortfolioValuationService,
)


class PortfolioListCreateView(
    generics.ListCreateAPIView
):
    serializer_class = PortfolioSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return (
            Portfolio.objects
            .filter(owner=self.request.user)
            .prefetch_related("assets")
            .order_by("-created_at")
        )

    def perform_create(self, serializer):
        serializer.save(
            owner=self.request.user
        )


class PortfolioDetailView(
    generics.RetrieveUpdateDestroyAPIView
):
    serializer_class = PortfolioSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return (
            Portfolio.objects
            .filter(owner=self.request.user)
            .prefetch_related("assets")
        )


class PortfolioAssetListCreateView(
    generics.ListCreateAPIView
):
    serializer_class = PortfolioAssetSerializer
    permission_classes = (IsAuthenticated,)

    def get_portfolio(self):
        return get_object_or_404(
            Portfolio,
            pk=self.kwargs["portfolio_pk"],
            owner=self.request.user,
        )

    def get_queryset(self):
        portfolio = self.get_portfolio()

        return (
            PortfolioAsset.objects
            .filter(portfolio=portfolio)
            .order_by("symbol")
        )

    def get_serializer_context(self):
        context = super().get_serializer_context()

        context["portfolio"] = (
            self.get_portfolio()
        )

        return context

    def perform_create(self, serializer):
        serializer.save(
            portfolio=self.get_portfolio()
        )


class PortfolioAssetDetailView(
    generics.RetrieveUpdateDestroyAPIView
):
    serializer_class = PortfolioAssetSerializer
    permission_classes = (IsAuthenticated,)

    def get_portfolio(self):
        return get_object_or_404(
            Portfolio,
            pk=self.kwargs["portfolio_pk"],
            owner=self.request.user,
        )

    def get_queryset(self):
        return PortfolioAsset.objects.filter(
            portfolio=self.get_portfolio()
        )

    def get_serializer_context(self):
        context = super().get_serializer_context()

        context["portfolio"] = (
            self.get_portfolio()
        )

        return context


class PortfolioValuationView(
    generics.RetrieveAPIView
):
    """Return the current valuation of a user's portfolio."""

    permission_classes = (IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        portfolio = get_object_or_404(
            Portfolio,
            pk=self.kwargs["pk"],
            owner=request.user,
        )

        service = PortfolioValuationService()

        valuation = service.value_portfolio(
            portfolio
        )

        return Response(valuation)


class PortfolioPerformanceView(APIView):
    """Return historical performance for a user's portfolio."""

    permission_classes = (IsAuthenticated,)

    ALLOWED_PERIODS = {
        30,
        90,
        180,
        365,
    }

    def get(self, request, pk):
        portfolio = get_object_or_404(
            Portfolio,
            pk=pk,
            owner=request.user,
        )

        try:
            days = int(
                request.query_params.get(
                    "days",
                    30,
                )
            )

        except (TypeError, ValueError):
            return Response(
                {
                    "detail": (
                        "Invalid performance period."
                    ),
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        if days not in self.ALLOWED_PERIODS:
            return Response(
                {
                    "detail": (
                        "Performance period must be "
                        "30, 90, 180, or 365 days."
                    ),
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        service = PortfolioPerformanceService()

        performance = (
            service.calculate_performance(
                portfolio,
                days=days,
            )
        )

        return Response(performance)


class PortfolioRiskView(APIView):
    """Return risk analysis for a user's portfolio."""

    permission_classes = (IsAuthenticated,)

    ALLOWED_PERIODS = {
        30,
        90,
        180,
        365,
    }

    def get(self, request, pk):
        portfolio = get_object_or_404(
            Portfolio,
            pk=pk,
            owner=request.user,
        )

        try:
            days = int(
                request.query_params.get(
                    "days",
                    30,
                )
            )

        except (TypeError, ValueError):
            return Response(
                {
                    "detail": (
                        "Invalid risk analysis period."
                    ),
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        if days not in self.ALLOWED_PERIODS:
            return Response(
                {
                    "detail": (
                        "Risk analysis period must be "
                        "30, 90, 180, or 365 days."
                    ),
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        valuation_service = (
            PortfolioValuationService()
        )

        performance_service = (
            PortfolioPerformanceService()
        )

        risk_service = (
            PortfolioRiskService()
        )

        valuation = (
            valuation_service.value_portfolio(
                portfolio
            )
        )

        performance = (
            performance_service.calculate_performance(
                portfolio,
                days=days,
            )
        )

        risk = risk_service.calculate_risk(
            valuation,
            performance,
        )

        return Response(risk)