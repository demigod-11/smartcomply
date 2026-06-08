import pytest
from django.utils import timezone

from apps.alerts.models import Alert
from apps.alerts.usecases.evaluate_transaction import evaluate_transaction
from apps.transactions.models import Transaction


@pytest.mark.django_db
def test_evaluate_creates_large_transaction_alert(large_tx_rule):
    tx = Transaction.objects.create(
        transaction_id="EVAL1",
        account_id="ACC1",
        amount=15000,
        currency="USD",
        transaction_type="TRANSFER",
        timestamp=timezone.now(),
    )
    alerts = evaluate_transaction(str(tx.id))
    assert len(alerts) == 1
    assert Alert.objects.count() == 1


@pytest.mark.django_db
def test_frequency_dedup_prevents_repeat_alerts(frequency_rule):
    base = timezone.now()
    account = "ACC_FREQ"
    for i in range(6):
        tx = Transaction.objects.create(
            transaction_id=f"FREQ{i}",
            account_id=account,
            amount=100,
            currency="USD",
            transaction_type="TRANSFER",
            timestamp=base,
        )
        evaluate_transaction(str(tx.id))

    assert Alert.objects.count() == 1

    tx7 = Transaction.objects.create(
        transaction_id="FREQ_EXTRA",
        account_id=account,
        amount=100,
        currency="USD",
        transaction_type="TRANSFER",
        timestamp=base,
    )
    evaluate_transaction(str(tx7.id))
    assert Alert.objects.count() == 1
