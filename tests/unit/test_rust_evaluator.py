import pytest

from apps.rules.infrastructure.evaluators.python_evaluator import PythonRuleEvaluator

pytest.importorskip("tm_rules", reason="Rust module not built")

from apps.rules.infrastructure.evaluators.rust_evaluator import RustRuleEvaluator


def test_rust_exceeds_threshold():
    ev = RustRuleEvaluator()
    assert ev.exceeds_threshold(15000.0, 10000.0)
    assert not ev.exceeds_threshold(5000.0, 10000.0)


def test_python_evaluator_parity():
    py = PythonRuleEvaluator()
    assert py.exceeds_threshold(15000.0, 10000.0)
    assert not py.exceeds_threshold(5000.0, 10000.0)
