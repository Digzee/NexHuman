from rest_framework import serializers

from .models import InvestorProfile
from .services import InvestorProfilingService


class InvestorProfileSerializer(
    serializers.ModelSerializer
):
    risk_score = serializers.IntegerField(
        read_only=True
    )

    risk_label = serializers.CharField(
        read_only=True
    )

    risk_label_display = serializers.CharField(
        source="get_risk_label_display",
        read_only=True,
    )

    class Meta:
        model = InvestorProfile

        fields = (
            "id",
            "investment_horizon",
            "loss_tolerance",
            "volatility_comfort",
            "investment_experience",
            "growth_preference",
            "risk_score",
            "risk_label",
            "risk_label_display",
            "created_at",
            "updated_at",
        )

        read_only_fields = (
            "id",
            "risk_score",
            "risk_label",
            "risk_label_display",
            "created_at",
            "updated_at",
        )

    def validate(self, attrs):
        for field in (
            InvestorProfilingService.QUESTION_FIELDS
        ):
            value = attrs.get(field)

            if value is None:
                raise serializers.ValidationError(
                    {
                        field: (
                            "This questionnaire response "
                            "is required."
                        )
                    }
                )

            if not (
                InvestorProfilingService.MIN_ANSWER
                <= value
                <= InvestorProfilingService.MAX_ANSWER
            ):
                raise serializers.ValidationError(
                    {
                        field: (
                            "Response must be between "
                            "1 and 5."
                        )
                    }
                )

        return attrs

    def create(self, validated_data):
        user = self.context["request"].user

        result = (
            InvestorProfilingService.calculate_profile(
                validated_data
            )
        )

        profile, _ = (
            InvestorProfile.objects.update_or_create(
                user=user,
                defaults={
                    **validated_data,
                    **result,
                },
            )
        )

        return profile

    def update(self, instance, validated_data):
        answers = {
            field: validated_data.get(
                field,
                getattr(instance, field),
            )
            for field in (
                InvestorProfilingService.QUESTION_FIELDS
            )
        }

        result = (
            InvestorProfilingService.calculate_profile(
                answers
            )
        )

        for field, value in answers.items():
            setattr(
                instance,
                field,
                value,
            )

        instance.risk_score = result["risk_score"]
        instance.risk_label = result["risk_label"]

        instance.save()

        return instance