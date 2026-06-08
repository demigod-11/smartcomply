from apps.rules.infrastructure.evaluators.python_evaluator import PythonRuleEvaluator


def get_rule_evaluator():
    try:
        from apps.rules.infrastructure.evaluators.rust_evaluator import RustRuleEvaluator

        return RustRuleEvaluator()
    except ImportError:
        return PythonRuleEvaluator()
