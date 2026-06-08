import uuid

from django.db import models
from django.db.models import Q


class Rule(models.Model):
    class RuleType(models.TextChoices):
        LARGE_TRANSACTION = "LARGE_TRANSACTION", "Large Transaction"
        HIGH_FREQUENCY = "HIGH_FREQUENCY", "High Frequency"

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255, unique=True)
    rule_type = models.CharField(max_length=30, choices=RuleType.choices)
    amount_threshold = models.DecimalField(max_digits=18, decimal_places=2, null=True, blank=True)
    frequency_limit = models.PositiveIntegerField(null=True, blank=True)
    window_hours = models.PositiveIntegerField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    created_by_client = models.ForeignKey(
        "identity.ApiClient",
        on_delete=models.SET_NULL,
        null=True,
        related_name="created_rules",
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "rules"
        indexes = [
            models.Index(fields=["is_active", "rule_type"]),
        ]
        constraints = [
            models.CheckConstraint(
                condition=Q(rule_type="LARGE_TRANSACTION", amount_threshold__gt=0)
                | ~Q(rule_type="LARGE_TRANSACTION"),
                name="rules_large_tx_threshold_positive",
            ),
            models.CheckConstraint(
                condition=Q(rule_type="HIGH_FREQUENCY", frequency_limit__gt=0)
                | ~Q(rule_type="HIGH_FREQUENCY"),
                name="rules_frequency_limit_positive",
            ),
            models.CheckConstraint(
                condition=Q(rule_type="HIGH_FREQUENCY", window_hours__gt=0)
                | ~Q(rule_type="HIGH_FREQUENCY"),
                name="rules_window_hours_positive",
            ),
        ]
