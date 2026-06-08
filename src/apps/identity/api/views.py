from rest_framework import mixins, status, viewsets
from rest_framework.response import Response

from apps.identity.api.serializers import (
    ApiClientSerializer,
    CreateApiClientResponseSerializer,
    CreateApiClientSerializer,
    UpdateApiClientSerializer,
)
from apps.identity.domain.commands import CreateApiClientCommand, UpdateApiClientCommand
from apps.identity.domain.platform_admin import is_platform_admin
from apps.identity.models import ApiClient
from apps.identity.permissions import scoped_permission
from apps.identity.usecases.create_api_client import create_api_client
from apps.identity.usecases.update_api_client import update_api_client


class ApiClientViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.UpdateModelMixin,
    viewsets.GenericViewSet,
):
    serializer_class = ApiClientSerializer
    lookup_field = "id"

    def get_queryset(self):
        if is_platform_admin(self.request.actor):
            return ApiClient.objects.all().order_by("-created_at")
        return ApiClient.objects.filter(created_by_id=self.request.actor.id).order_by(
            "-created_at"
        )

    def get_permissions(self):
        if self.action == "create":
            return [scoped_permission("api_clients:write")()]
        if self.action in ("list", "retrieve"):
            return [scoped_permission("api_clients:read")()]
        if self.action in ("partial_update", "update"):
            return [scoped_permission("api_clients:manage")()]
        return super().get_permissions()

    def create(self, request, *args, **kwargs):
        serializer = CreateApiClientSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        client, raw_key = create_api_client(
            CreateApiClientCommand(
                name=serializer.validated_data["name"],
                scopes=serializer.validated_data["scopes"],
            ),
            actor=request.actor,
        )
        data = {
            "id": client.id,
            "name": client.name,
            "scopes": client.scopes,
            "api_key": raw_key,
            "created_at": client.created_at,
            "warning": "Store this key securely. It cannot be retrieved again.",
        }
        return Response(CreateApiClientResponseSerializer(data).data, status=status.HTTP_201_CREATED)

    def partial_update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = UpdateApiClientSerializer(data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        client = update_api_client(
            UpdateApiClientCommand(
                client_id=str(instance.id),
                is_active=serializer.validated_data.get("is_active"),
                scopes=serializer.validated_data.get("scopes"),
            ),
            actor=request.actor,
        )
        return Response(ApiClientSerializer(client).data)
