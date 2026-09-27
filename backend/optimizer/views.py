from rest_framework import status
from rest_framework.permissions import (
    IsAuthenticated,
)
from rest_framework.response import Response
from rest_framework.views import APIView

from portfolios.models import Portfolio

from .models import OptimizationRun
from .serializers import (
    OptimizationRunSerializer,
)
from .services.portfolio_optimization_service import (
    PortfolioOptimizationService,
)


class PortfolioOptimizationView(APIView):
    permission_classes = [IsAuthenticated]

    def post(
        self,
        request,
        portfolio_id,
    ):
        try:
            portfolio = Portfolio.objects.get(
                id=portfolio_id,
                owner=request.user,
            )
        except Portfolio.DoesNotExist:
            return Response(
                {
                    "detail": (
                        "Portfolio not found."
                    )
                },
                status=status.HTTP_404_NOT_FOUND,
            )

        try:
            run = (
                PortfolioOptimizationService()
                .optimise(
                    user=request.user,
                    portfolio=portfolio,
                )
            )
        except ValueError as error:
            return Response(
                {
                    "detail": str(error),
                },
                status=(
                    status.HTTP_400_BAD_REQUEST
                ),
            )
        except RuntimeError:
            return Response(
                {
                    "detail": (
                        "Market data is temporarily "
                        "unavailable."
                    )
                },
                status=(
                    status.HTTP_503_SERVICE_UNAVAILABLE
                ),
            )

        return Response(
            OptimizationRunSerializer(
                run
            ).data,
            status=status.HTTP_201_CREATED,
        )


class OptimizationHistoryView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        runs = (
            OptimizationRun.objects.filter(
                user=request.user
            )
            .select_related("portfolio")
            .prefetch_related("allocations")
        )

        serializer = (
            OptimizationRunSerializer(
                runs,
                many=True,
            )
        )

        return Response(
            serializer.data
        )