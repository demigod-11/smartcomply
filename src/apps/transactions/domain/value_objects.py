from decimal import Decimal, InvalidOperation
from enum import Enum

from apps.core.exceptions import DomainError


class TransactionType(str, Enum):
    TRANSFER = "TRANSFER"
    DEPOSIT = "DEPOSIT"
    WITHDRAWAL = "WITHDRAWAL"

    @classmethod
    def from_string(cls, value: str) -> "TransactionType":
        try:
            return cls(value.upper())
        except ValueError as exc:
            raise DomainError(f"Invalid transaction_type: {value}") from exc


class Currency:
    def __init__(self, code: str):
        code = code.upper().strip()
        if len(code) != 3 or not code.isalpha():
            raise DomainError(f"Invalid currency code: {code}")
        self.code = code


class Money:
    def __init__(self, amount, currency: str):
        try:
            self.amount = Decimal(str(amount))
        except (InvalidOperation, ValueError) as exc:
            raise DomainError(f"Invalid amount: {amount}") from exc
        if self.amount <= 0:
            raise DomainError("Amount must be positive.")
        self.currency = Currency(currency)
