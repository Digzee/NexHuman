from django.urls import path

from .views import (
    PortfolioAssetDetailView,
    PortfolioAssetListCreateView,
    PortfolioDetailView,
    PortfolioListCreateView,
    PortfolioPerformanceView,
    PortfolioRiskView,
    PortfolioValuationView,
)


urlpatterns = [
    path(
        "",
        PortfolioListCreateView.as_view(),
        name="portfolio_list_create",
    ),
    path(
        "<int:pk>/",
        PortfolioDetailView.as_view(),
        name="portfolio_detail",
    ),
    path(
        "<int:portfolio_pk>/assets/",
        PortfolioAssetListCreateView.as_view(),
        name="portfolio_asset_list_create",
    ),
    path(
        "<int:portfolio_pk>/assets/<int:pk>/",
        PortfolioAssetDetailView.as_view(),
        name="portfolio_asset_detail",
    ),
    path(
        "<int:pk>/valuation/",
        PortfolioValuationView.as_view(),
        name="portfolio_valuation",
    ),
    path(
        "<int:pk>/performance/",
        PortfolioPerformanceView.as_view(),
        name="portfolio_performance",
    ),
    path(
        "<int:pk>/risk/",
        PortfolioRiskView.as_view(),
        name="portfolio_risk",
    ),
]