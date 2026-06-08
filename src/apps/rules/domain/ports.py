from typing import Protocol


class RuleEvaluator(Protocol):
    def exceeds_threshold(self, amount: float, threshold: float) -> bool: ...
