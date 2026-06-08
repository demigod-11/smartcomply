from apps.audit.decorators import audit_action
from apps.core.domain.actor import Actor
from apps.core.exceptions import DuplicateApiClientError
from apps.identity.domain.commands import CreateApiClientCommand
from apps.identity.infrastructure.cache import invalidate_client_cache
from apps.identity.models import ApiClient


@audit_action("api_client.created", entity_type="api_client")
def create_api_client(command: CreateApiClientCommand, actor: Actor) -> tuple[ApiClient, str]:
    if ApiClient.objects.filter(name=command.name).exists():
        raise DuplicateApiClientError()

    client, raw_key = ApiClient.create_client(
        name=command.name,
        scopes=command.scopes,
        created_by_id=actor.id,
    )
    invalidate_client_cache(client.key_hash)
    return client, raw_key
