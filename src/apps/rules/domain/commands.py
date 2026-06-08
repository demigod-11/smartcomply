from dataclasses import dataclass
from decimal import Decimal


@dataclass(frozen=True)
class CreateRuleCommand:
    name: str
    rule_type: str
    amount_threshold: Decimal | None = None
    frequency_limit: int | None = None
    window_hours: int | None = None
