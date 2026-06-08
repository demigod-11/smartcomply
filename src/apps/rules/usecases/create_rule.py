from apps.audit.decorators import audit_action
from apps.core.domain.actor import Actor
from apps.core.exceptions import DomainError, DuplicateRuleError
from apps.rules.domain.commands import CreateRuleCommand
from apps.rules.infrastructure.cache import invalidate_active_rules
from apps.rules.models import Rule


@audit_action("rule.created", entity_type="rule")
def create_rule(command: CreateRuleCommand, actor: Actor) -> Rule:
    if Rule.objects.filter(name=command.name).exists():
        raise DuplicateRuleError()

    if command.rule_type == Rule.RuleType.LARGE_TRANSACTION:
        if command.amount_threshold is None:
            raise DomainError("amount_threshold is required for LARGE_TRANSACTION rules.")
        rule = Rule.objects.create(
            name=command.name,
            rule_type=command.rule_type,
            amount_threshold=command.amount_threshold,
            frequency_limit=None,
            window_hours=None,
            created_by_client_id=actor.id,
        )
    elif command.rule_type == Rule.RuleType.HIGH_FREQUENCY:
        rule = Rule.objects.create(
            name=command.name,
            rule_type=command.rule_type,
            amount_threshold=None,
            frequency_limit=command.frequency_limit or 5,
            window_hours=command.window_hours or 24,
            created_by_client_id=actor.id,
        )
    else:
        raise DomainError(f"Unknown rule_type: {command.rule_type}")

    invalidate_active_rules()
    return rule
