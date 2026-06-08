import django_filters
from rest_framework import mixins, status, viewsets
from rest_framework.response import Response

from apps.identity.permissions import scoped_permission
from apps.rules.api.serializers import CreateRuleSerializer, RuleSerializer
from apps.rules.domain.commands import CreateRuleCommand
from apps.rules.models import Rule
from apps.rules.usecases.create_rule import create_rule


class RuleFilter(django_filters.FilterSet):
    rule_type = django_filters.CharFilter()
    is_active = django_filters.BooleanFilter()

    class Meta:
        model = Rule
        fields = ["rule_type", "is_active"]


class RuleViewSet(mixins.CreateModelMixin, mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = Rule.objects.all()
    serializer_class = RuleSerializer
    filterset_class = RuleFilter
    ordering_fields = ["name", "created_at"]
    ordering = ["name"]

    def get_permissions(self):
        if self.action == "create":
            return [scoped_permission("rules:write")()]
        if self.action == "list":
            return [scoped_permission("rules:read")()]
        return super().get_permissions()

    def create(self, request, *args, **kwargs):
        serializer = CreateRuleSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        rule = create_rule(
            CreateRuleCommand(
                name=data["name"],
                rule_type=data.get("rule_type", Rule.RuleType.LARGE_TRANSACTION),
                amount_threshold=data.get("amount_threshold"),
                frequency_limit=data.get("frequency_limit"),
                window_hours=data.get("window_hours"),
            ),
            actor=request.actor,
        )
        return Response(RuleSerializer(rule).data, status=status.HTTP_201_CREATED)
