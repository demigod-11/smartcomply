from apps.audit.decorators import audit_action
from apps.core.domain.actor import Actor
from apps.identity.domain.commands import UpdateApiClientCommand
from apps.identity.domain.platform_admin import is_platform_admin
from apps.identity.infrastructure.cache import invalidate_client_cache
from apps.identity.models import ApiClient


@audit_action("api_client.updated", entity_type="api_client")
def update_api_client(command: UpdateApiClientCommand, actor: Actor) -> ApiClient:
    if is_platform_admin(actor):
        client = ApiClient.objects.get(id=command.client_id)
    else:
        client = ApiClient.objects.get(id=command.client_id, created_by_id=actor.id)

    if command.is_active is not None:
        client.is_active = command.is_active
    if command.scopes is not None:
        client.scopes = command.scopes

    client.save(update_fields=["is_active", "scopes"])
    invalidate_client_cache(client.key_hash)
    return client
