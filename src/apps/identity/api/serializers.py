from rest_framework import serializers

from apps.identity.models import ApiClient

VALID_SCOPES = {
    "transactions:write",
    "transactions:read",
    "rules:write",
    "rules:read",
    "alerts:read",
    "alerts:stream",
    "audit:read",
    "api_clients:write",
    "api_clients:read",
    "api_clients:manage",
}


class CreateApiClientSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=255)
    scopes = serializers.ListField(child=serializers.CharField())

    def validate_scopes(self, value):
        invalid = set(value) - VALID_SCOPES
        if invalid:
            raise serializers.ValidationError(f"Invalid scopes: {sorted(invalid)}")
        if not value:
            raise serializers.ValidationError("At least one scope is required.")
        return value


class UpdateApiClientSerializer(serializers.Serializer):
    is_active = serializers.BooleanField(required=False)
    scopes = serializers.ListField(child=serializers.CharField(), required=False)

    def validate_scopes(self, value):
        if value is None:
            return value
        invalid = set(value) - VALID_SCOPES
        if invalid:
            raise serializers.ValidationError(f"Invalid scopes: {sorted(invalid)}")
        return value


class ApiClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = ApiClient
        fields = ["id", "name", "scopes", "is_active", "created_at"]


class CreateApiClientResponseSerializer(serializers.Serializer):
    id = serializers.UUIDField()
    name = serializers.CharField()
    scopes = serializers.ListField(child=serializers.CharField())
    api_key = serializers.CharField()
    created_at = serializers.DateTimeField()
    warning = serializers.CharField()
