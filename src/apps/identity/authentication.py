from uuid import UUID

from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed

from apps.core.domain.actor import Actor
from apps.identity.infrastructure.cache import get_cached_client, set_cached_client
from apps.identity.models import ApiClient


class APIKeyAuthentication(BaseAuthentication):
    header = "HTTP_X_API_KEY"

    def authenticate(self, request):
        raw_key = request.META.get(self.header)
        if not raw_key:
            raise AuthenticationFailed("API key required.")

        key_hash = ApiClient.hash_key(raw_key)
        cached = get_cached_client(key_hash)

        if cached:
            if not cached["is_active"]:
                raise AuthenticationFailed("API key is inactive.")
            actor = Actor(
                id=UUID(cached["id"]),
                name=cached["name"],
                scopes=frozenset(cached["scopes"]),
            )
            request.actor = actor
            return (None, actor)

        try:
            client = ApiClient.objects.get(key_hash=key_hash)
        except ApiClient.DoesNotExist as exc:
            raise AuthenticationFailed("Invalid API key.") from exc

        if not client.is_active:
            raise AuthenticationFailed("API key is inactive.")

        set_cached_client(client)
        actor = Actor(
            id=client.id,
            name=client.name,
            scopes=frozenset(client.scopes),
        )
        request.actor = actor
        return (None, actor)
