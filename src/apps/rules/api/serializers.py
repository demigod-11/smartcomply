from rest_framework import serializers

from apps.rules.models import Rule


class CreateRuleSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=255)
    amount_threshold = serializers.DecimalField(
        max_digits=18, decimal_places=2, required=False, allow_null=True
    )
    rule_type = serializers.ChoiceField(
        choices=Rule.RuleType.choices, required=False, default=Rule.RuleType.LARGE_TRANSACTION
    )
    frequency_limit = serializers.IntegerField(required=False, allow_null=True)
    window_hours = serializers.IntegerField(required=False, allow_null=True)

    def validate(self, attrs):
        rule_type = attrs.get("rule_type", Rule.RuleType.LARGE_TRANSACTION)
        if rule_type == Rule.RuleType.LARGE_TRANSACTION and attrs.get("amount_threshold") is None:
            if "amount_threshold" not in self.initial_data:
                raise serializers.ValidationError(
                    {"amount_threshold": "Required for LARGE_TRANSACTION rules."}
                )
        return attrs


class RuleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rule
        fields = [
            "id",
            "name",
            "rule_type",
            "amount_threshold",
            "frequency_limit",
            "window_hours",
            "is_active",
            "created_at",
        ]
