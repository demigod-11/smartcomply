from rest_framework import serializers

from apps.audit.models import AuditLog


class AuditLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = AuditLog
        fields = [
            "id",
            "action",
            "entity_type",
            "entity_id",
            "payload",
            "actor_type",
            "actor_id",
            "actor_name",
            "created_at",
        ]
