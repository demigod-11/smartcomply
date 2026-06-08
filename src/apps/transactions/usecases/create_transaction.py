from django_q.tasks import async_task

from apps.core.domain.actor import Actor
from apps.core.exceptions import DuplicateTransactionError
from apps.transactions.domain.commands import CreateTransactionCommand
from apps.transactions.domain.value_objects import Money, TransactionType
from apps.transactions.models import Transaction


def create_transaction(command: CreateTransactionCommand, actor: Actor) -> Transaction:
    if Transaction.objects.filter(transaction_id=command.transaction_id).exists():
        raise DuplicateTransactionError()

    money = Money(command.amount, command.currency)
    tx_type = TransactionType.from_string(command.transaction_type)

    transaction = Transaction.objects.create(
        transaction_id=command.transaction_id,
        account_id=command.account_id,
        amount=money.amount,
        currency=money.currency.code,
        transaction_type=tx_type.value,
        timestamp=command.timestamp,
        submitted_by_client_id=actor.id,
    )

    async_task("apps.alerts.infrastructure.tasks.evaluate_transaction.run", str(transaction.id))
    return transaction
