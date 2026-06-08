import pytest
from django.core.cache import cache
from rest_framework.test import APIClient

from apps.identity.models import ApiClient
from apps.rules.models import Rule


@pytest.fixture(autouse=True)
def clear_cache():
    cache.clear()
    yield
    cache.clear()


@pytest.fixture
def api_client():
    return APIClient()


def _make_client(name: str, raw_key: str, scopes: list[str]) -> tuple[ApiClient, str]:
    client, _ = ApiClient.objects.update_or_create(
        name=name,
        defaults={"key_hash": ApiClient.hash_key(raw_key), "scopes": scopes, "is_active": True},
    )
    return client, raw_key


@pytest.fixture
def bootstrap_client(db):
    return _make_client(
        "platform-admin",
        "sc_test_bootstrap",
        ["api_clients:write", "api_clients:read", "api_clients:manage"],
    )


@pytest.fixture
def ingest_client(db):
    return _make_client("ingestion-service", "sc_test_ingest", ["transactions:write"])


@pytest.fixture
def ops_client(db):
    return _make_client(
        "ops-reader",
        "sc_test_ops",
        ["transactions:read", "alerts:read", "alerts:stream"],
    )


@pytest.fixture
def admin_client(db):
    return _make_client("rule-admin", "sc_test_admin", ["rules:write", "rules:read", "audit:read"])


@pytest.fixture
def large_tx_rule(db):
    rule, _ = Rule.objects.get_or_create(
        name="Large Transaction Rule",
        defaults={
            "rule_type": Rule.RuleType.LARGE_TRANSACTION,
            "amount_threshold": 10000,
            "is_active": True,
        },
    )
    return rule


@pytest.fixture
def frequency_rule(db):
    rule, _ = Rule.objects.get_or_create(
        name="High Frequency Rule",
        defaults={
            "rule_type": Rule.RuleType.HIGH_FREQUENCY,
            "frequency_limit": 5,
            "window_hours": 24,
            "is_active": True,
        },
    )
    return rule


@pytest.fixture
def auth_headers():
    def _headers(raw_key: str):
        return {"HTTP_X_API_KEY": raw_key}

    return _headers
