from django.urls import path

from .views import CryptocurrencyListView


urlpatterns = [
    path(
        "cryptocurrencies/",
        CryptocurrencyListView.as_view(),
        name="cryptocurrency_list",
    ),
]