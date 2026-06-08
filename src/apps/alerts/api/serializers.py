from rest_framework import serializers

from apps.alerts.models import Alert


class AlertSerializer(serializers.ModelSerializer):
    rule = serializers.CharField(source="rule.name")
    transaction_id = serializers.CharField(source="transaction.transaction_id")

    class Meta:
        model = Alert
        fields = ["id", "rule", "account_id", "transaction_id", "created_at"]
