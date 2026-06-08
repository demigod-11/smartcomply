import json

from django.core.cache import cache

from apps.identity.models import ApiClient

API_KEY_CACHE_TTL = 600
API_KEY_CACHE_PREFIX = "tm:apikey:"


def cache_key_for_hash(key_hash: str) -> str:
    return f"{API_KEY_CACHE_PREFIX}{key_hash}"


def get_cached_client(key_hash: str) -> dict | None:
    data = cache.get(cache_key_for_hash(key_hash))
    if data is None:
        return None
    return json.loads(data)


def set_cached_client(client: ApiClient) -> None:
    payload = {
        "id": str(client.id),
        "name": client.name,
        "scopes": client.scopes,
        "is_active": client.is_active,
    }
    cache.set(cache_key_for_hash(client.key_hash), json.dumps(payload), API_KEY_CACHE_TTL)


def invalidate_client_cache(key_hash: str) -> None:
    cache.delete(cache_key_for_hash(key_hash))
