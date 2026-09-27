from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import AdvisorQuestionSerializer
from .services import AdvisorService


class AdvisorView(APIView):
    permission_classes = [
        IsAuthenticated,
    ]

    def post(self, request):
        serializer = AdvisorQuestionSerializer(
            data=request.data
        )

        serializer.is_valid(
            raise_exception=True
        )

        try:
            answer = AdvisorService().ask(
                user=request.user,
                message=(
                    serializer.validated_data[
                        "message"
                    ]
                ),
            )
        except RuntimeError as exc:
            return Response(
                {
                    "detail": str(exc),
                },
                status=(
                    status.HTTP_503_SERVICE_UNAVAILABLE
                ),
            )

        return Response(
            {
                "answer": answer,
            },
            status=status.HTTP_200_OK,
        )