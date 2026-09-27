from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from .models import Cryptocurrency
from .serializers import CryptocurrencySerializer


class CryptocurrencyListView(generics.ListAPIView):
    """Return cryptocurrencies currently supported by NexHuman."""

    serializer_class = CryptocurrencySerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return Cryptocurrency.objects.filter(
            is_active=True
        ).order_by("symbol")