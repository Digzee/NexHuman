from django.urls import path

from .views import (
    PortfolioAssetDetailView,
    PortfolioAssetListCreateView,
    PortfolioDetailView,
    PortfolioListCreateView,
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
]