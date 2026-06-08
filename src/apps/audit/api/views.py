import django_filters
from rest_framework import mixins, viewsets

from apps.audit.api.serializers import AuditLogSerializer
from apps.audit.models import AuditLog
from apps.identity.permissions import scoped_permission


class AuditLogFilter(django_filters.FilterSet):
    entity_type = django_filters.CharFilter()
    action = django_filters.CharFilter()
    actor_name = django_filters.CharFilter()

    class Meta:
        model = AuditLog
        fields = ["entity_type", "action", "actor_name"]


class AuditLogViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = AuditLog.objects.all()
    serializer_class = AuditLogSerializer
    filterset_class = AuditLogFilter
    ordering_fields = ["created_at"]
    ordering = ["-created_at"]
    permission_classes = [scoped_permission("audit:read")]
