import json

from django.core.cache import cache

from apps.rules.models import Rule

ACTIVE_RULES_KEY = "tm:rules:active"
ACTIVE_RULES_TTL = 60


def get_active_rules() -> list[dict] | None:
    data = cache.get(ACTIVE_RULES_KEY)
    if data is None:
        return None
    return json.loads(data)


def set_active_rules(rules: list[dict]) -> None:
    cache.set(ACTIVE_RULES_KEY, json.dumps(rules), ACTIVE_RULES_TTL)


def invalidate_active_rules() -> None:
    cache.delete(ACTIVE_RULES_KEY)


def load_active_rules_from_db() -> list[dict]:
    rules = Rule.objects.filter(is_active=True)
    return [
        {
            "id": str(rule.id),
            "name": rule.name,
            "rule_type": rule.rule_type,
            "amount_threshold": float(rule.amount_threshold) if rule.amount_threshold else None,
            "frequency_limit": rule.frequency_limit,
            "window_hours": rule.window_hours,
        }
        for rule in rules
    ]
