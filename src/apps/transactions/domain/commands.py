from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal


@dataclass(frozen=True)
class CreateTransactionCommand:
    transaction_id: str
    account_id: str
    amount: Decimal
    currency: str
    transaction_type: str
    timestamp: datetime
