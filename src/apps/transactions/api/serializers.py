from rest_framework import serializers

from apps.transactions.models import Transaction


class CreateTransactionSerializer(serializers.Serializer):
    transaction_id = serializers.CharField(max_length=255)
    account_id = serializers.CharField(max_length=255)
    amount = serializers.DecimalField(max_digits=18, decimal_places=2)
    currency = serializers.CharField(max_length=3)
    transaction_type = serializers.CharField(max_length=20)
    timestamp = serializers.DateTimeField()


class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = [
            "id",
            "transaction_id",
            "account_id",
            "amount",
            "currency",
            "transaction_type",
            "timestamp",
            "created_at",
        ]
