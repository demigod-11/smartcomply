import json
from urllib.parse import parse_qs

from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer

from apps.core.domain.actor import Actor
from apps.identity.infrastructure.cache import get_cached_client
from apps.identity.models import ApiClient


class AlertsConsumer(AsyncWebsocketConsumer):
    group_name = "alerts"

    async def connect(self):
        self._joined_group = False
        params = parse_qs(self.scope["query_string"].decode())
        raw_key = params.get("api_key", [None])[0]

        if not raw_key:
            await self.close(code=4001)
            return

        actor = await self._authenticate(raw_key)
        if actor is None or not actor.has_scope("alerts:stream"):
            await self.close(code=4003)
            return

        self.scope["actor"] = actor
        await self.channel_layer.group_add(self.group_name, self.channel_name)
        self._joined_group = True
        await self.accept()

    async def disconnect(self, close_code):
        if not getattr(self, "_joined_group", False):
            return
        try:
            await self.channel_layer.group_discard(self.group_name, self.channel_name)
        except Exception:
            pass

    async def alert_created(self, event):
        await self.send(text_data=json.dumps(event["payload"]))

    @staticmethod
    async def _authenticate(raw_key: str) -> Actor | None:
        from asgiref.sync import sync_to_async

        key_hash = ApiClient.hash_key(raw_key)
        cached = await sync_to_async(get_cached_client)(key_hash)
        if cached:
            if not cached["is_active"]:
                return None
            from uuid import UUID

            return Actor(
                id=UUID(cached["id"]),
                name=cached["name"],
                scopes=frozenset(cached["scopes"]),
            )

        try:
            client = await database_sync_to_async(ApiClient.objects.get)(key_hash=key_hash)
        except ApiClient.DoesNotExist:
            return None

        if not client.is_active:
            return None

        return Actor(id=client.id, name=client.name, scopes=frozenset(client.scopes))
