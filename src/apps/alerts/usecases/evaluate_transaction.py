from datetime import timedelta

from django.db import IntegrityError

from apps.alerts.infrastructure.dedup import should_create_frequency_alert
from apps.alerts.models import Alert
from apps.alerts.services.notify import notify_alert_created
from apps.rules.infrastructure.cache import get_active_rules, load_active_rules_from_db, set_active_rules
from apps.rules.domain.policies.frequency import exceeds_frequency_limit
from apps.rules.infrastructure.evaluators import get_rule_evaluator
from apps.rules.models import Rule
from apps.transactions.models import Transaction


def _get_rules() -> list[dict]:
    cached = get_active_rules()
    if cached is not None:
        return cached
    rules = load_active_rules_from_db()
    set_active_rules(rules)
    return rules


def _alert_payload(alert: Alert) -> dict:
    return {
        "id": str(alert.id),
        "rule": alert.rule.name,
        "account_id": alert.account_id,
        "transaction_id": alert.transaction.transaction_id,
        "created_at": alert.created_at.isoformat().replace("+00:00", "Z"),
    }


def _create_alert(rule: dict, transaction: Transaction) -> Alert | None:
    try:
        alert = Alert.objects.create(
            rule_id=rule["id"],
            transaction=transaction,
            account_id=transaction.account_id,
        )
    except IntegrityError:
        return None

    alert = Alert.objects.select_related("rule", "transaction").get(id=alert.id)
    notify_alert_created(_alert_payload(alert))
    return alert


def evaluate_transaction(transaction_id: str) -> list[Alert]:
    transaction = Transaction.objects.get(id=transaction_id)
    rules = _get_rules()
    evaluator = get_rule_evaluator()
    created_alerts: list[Alert] = []

    for rule in rules:
        if rule["rule_type"] == Rule.RuleType.LARGE_TRANSACTION:
            threshold = rule["amount_threshold"]
            if threshold is None:
                continue
            if evaluator.exceeds_threshold(float(transaction.amount), threshold):
                alert = _create_alert(rule, transaction)
                if alert:
                    created_alerts.append(alert)

        elif rule["rule_type"] == Rule.RuleType.HIGH_FREQUENCY:
            window_hours = rule.get("window_hours") or 24
            limit = rule.get("frequency_limit") or 5
            window_start = transaction.timestamp - timedelta(hours=window_hours)

            txn_count = Transaction.objects.filter(
                account_id=transaction.account_id,
                timestamp__gt=window_start,
                timestamp__lte=transaction.timestamp,
            ).count()

            if exceeds_frequency_limit(txn_count, limit=limit):
                if should_create_frequency_alert(transaction.account_id):
                    alert = _create_alert(rule, transaction)
                    if alert:
                        created_alerts.append(alert)

    return created_alerts
