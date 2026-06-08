import uuid

from django.db import models
from django.db.models import Q


class Transaction(models.Model):
    class TransactionType(models.TextChoices):
        TRANSFER = "TRANSFER", "Transfer"
        DEPOSIT = "DEPOSIT", "Deposit"
        WITHDRAWAL = "WITHDRAWAL", "Withdrawal"

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    transaction_id = models.CharField(max_length=255, unique=True)
    account_id = models.CharField(max_length=255)
    amount = models.DecimalField(max_digits=18, decimal_places=2)
    currency = models.CharField(max_length=3)
    transaction_type = models.CharField(max_length=20, choices=TransactionType.choices)
    timestamp = models.DateTimeField()
    submitted_by_client = models.ForeignKey(
        "identity.ApiClient",
        on_delete=models.SET_NULL,
        null=True,
        related_name="submitted_transactions",
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "transactions"
        ordering = ["-timestamp"]
        indexes = [
            models.Index(fields=["account_id", "-timestamp"]),
            models.Index(fields=["created_at"]),
        ]
        constraints = [
            models.CheckConstraint(condition=Q(amount__gt=0), name="transactions_amount_positive"),
        ]
