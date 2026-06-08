class RustRuleEvaluator:
    def __init__(self):
        import tm_rules

        self._module = tm_rules

    def exceeds_threshold(self, amount: float, threshold: float) -> bool:
        return self._module.exceeds_threshold(amount, threshold)
