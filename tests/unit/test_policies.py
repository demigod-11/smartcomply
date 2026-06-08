from decimal import Decimal

from apps.rules.domain.policies.frequency import exceeds_frequency_limit
from apps.rules.domain.policies.large_transaction import exceeds_threshold


def test_exceeds_threshold():
    assert exceeds_threshold(Decimal("15000"), Decimal("10000"))
    assert not exceeds_threshold(Decimal("5000"), Decimal("10000"))


def test_exceeds_frequency_limit():
    assert exceeds_frequency_limit(6, limit=5)
    assert not exceeds_frequency_limit(5, limit=5)
