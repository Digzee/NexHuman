from django.shortcuts import get_object_or_404
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from .models import Portfolio, PortfolioAsset
from .serializers import (
    PortfolioAssetSerializer,
    PortfolioSerializer,
)

class PortfolioListCreateView(generics.ListCreateAPIView):
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
        serializer.save(owner=self.request.user)


class PortfolioDetailView(generics.RetrieveUpdateDestroyAPIView):
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
        context["portfolio"] = self.get_portfolio()
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
        context["portfolio"] = self.get_portfolio()
        return context