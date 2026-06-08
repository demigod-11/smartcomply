from apps.rules.domain.policies.large_transaction import exceeds_threshold as policy_exceeds_threshold


class PythonRuleEvaluator:
    def exceeds_threshold(self, amount: float, threshold: float) -> bool:
        from decimal import Decimal

        return policy_exceeds_threshold(Decimal(str(amount)), Decimal(str(threshold)))
