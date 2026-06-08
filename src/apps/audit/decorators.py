import functools
import json
from uuid import UUID

from apps.audit.models import AuditLog
from apps.core.domain.actor import Actor


def _serialize_payload(obj) -> dict:
    if hasattr(obj, "__dict__"):
        data = {}
        for key, value in vars(obj).items():
            if key.startswith("_"):
                continue
            if isinstance(value, UUID):
                data[key] = str(value)
            else:
                try:
                    json.dumps(value)
                    data[key] = value
                except TypeError:
                    data[key] = str(value)
        return data
    return {"value": str(obj)}


def audit_action(action: str, entity_type: str):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            actor: Actor = kwargs.get("actor") or (args[1] if len(args) > 1 else None)
            command = args[0] if args else None
            result = func(*args, **kwargs)

            entity_id = getattr(result, "id", None)
            if entity_id is None and isinstance(result, tuple):
                entity_id = getattr(result[0], "id", None)

            payload = _serialize_payload(command) if command else {}

            if actor and entity_id:
                AuditLog.objects.create(
                    action=action,
                    entity_type=entity_type,
                    entity_id=entity_id,
                    payload=payload,
                    actor_type=actor.type,
                    actor_id=actor.id,
                    actor_name=actor.name,
                )
            return result

        return wrapper

    return decorator
