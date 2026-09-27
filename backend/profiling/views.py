from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import InvestorProfile
from .serializers import InvestorProfileSerializer


class InvestorProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            profile = request.user.investor_profile
        except InvestorProfile.DoesNotExist:
            return Response(
                {
                    "detail": (
                        "Investor profile has not "
                        "been completed."
                    )
                },
                status=status.HTTP_404_NOT_FOUND,
            )

        serializer = InvestorProfileSerializer(
            profile
        )

        return Response(serializer.data)

    def post(self, request):
        serializer = InvestorProfileSerializer(
            data=request.data,
            context={
                "request": request,
            },
        )

        serializer.is_valid(
            raise_exception=True
        )

        profile = serializer.save()

        return Response(
            InvestorProfileSerializer(
                profile
            ).data,
            status=status.HTTP_200_OK,
        )