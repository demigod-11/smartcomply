import django_filters
from rest_framework import mixins, viewsets

from apps.alerts.api.serializers import AlertSerializer
from apps.alerts.models import Alert
from apps.identity.permissions import scoped_permission


class AlertFilter(django_filters.FilterSet):
    account_id = django_filters.CharFilter()
    rule_id = django_filters.UUIDFilter(field_name="rule_id")
    transaction_id = django_filters.CharFilter(field_name="transaction__transaction_id")

    class Meta:
        model = Alert
        fields = ["account_id", "rule_id", "transaction_id"]


class AlertViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = Alert.objects.select_related("rule", "transaction").all()
    serializer_class = AlertSerializer
    filterset_class = AlertFilter
    ordering_fields = ["created_at"]
    ordering = ["-created_at"]
    permission_classes = [scoped_permission("alerts:read")]
