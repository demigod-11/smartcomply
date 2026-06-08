from apps.core.domain.actor import Actor
from apps.identity.models import ApiClient


def is_platform_admin(actor: Actor) -> bool:
    """Bootstrap platform-admin has no created_by and can manage all API clients."""
    return ApiClient.objects.filter(id=actor.id, created_by__isnull=True).exists()
