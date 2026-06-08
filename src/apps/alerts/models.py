import uuid

from django.db import models


class Alert(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    rule = models.ForeignKey("rules.Rule", on_delete=models.CASCADE, related_name="alerts")
    transaction = models.ForeignKey(
        "transactions.Transaction", on_delete=models.CASCADE, related_name="alerts"
    )
    account_id = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "alerts"
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["account_id", "-created_at"]),
            models.Index(fields=["rule"]),
            models.Index(fields=["transaction"]),
        ]
        constraints = [
            models.UniqueConstraint(
                fields=["rule", "transaction"],
                name="alerts_unique_rule_transaction",
            ),
        ]
