from django.urls import path

from .views import (
    OptimizationHistoryView,
    PortfolioOptimizationView,
)


urlpatterns = [
    path(
        "portfolio/<int:portfolio_id>/",
        PortfolioOptimizationView.as_view(),
        name="portfolio_optimization",
    ),
    path(
        "history/",
        OptimizationHistoryView.as_view(),
        name="optimization_history",
    ),
]