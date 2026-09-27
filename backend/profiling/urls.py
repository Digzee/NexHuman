from django.urls import path

from .views import InvestorProfileView


urlpatterns = [
    path(
        "",
        InvestorProfileView.as_view(),
        name="investor_profile",
    ),
]