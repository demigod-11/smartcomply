import django_filters
from rest_framework import mixins, status, viewsets
from rest_framework.response import Response

from apps.identity.permissions import scoped_permission
from apps.transactions.api.serializers import CreateTransactionSerializer, TransactionSerializer
from apps.transactions.domain.commands import CreateTransactionCommand
from apps.transactions.models import Transaction
from apps.transactions.usecases.create_transaction import create_transaction


class TransactionFilter(django_filters.FilterSet):
    account_id = django_filters.CharFilter()
    transaction_type = django_filters.CharFilter()
    currency = django_filters.CharFilter()

    class Meta:
        model = Transaction
        fields = ["account_id", "transaction_type", "currency"]


class TransactionViewSet(mixins.CreateModelMixin, mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer
    filterset_class = TransactionFilter
    ordering_fields = ["timestamp", "amount", "created_at"]
    ordering = ["-timestamp"]

    def get_permissions(self):
        if self.action == "create":
            return [scoped_permission("transactions:write")()]
        if self.action == "list":
            return [scoped_permission("transactions:read")()]
        return super().get_permissions()

    def create(self, request, *args, **kwargs):
        serializer = CreateTransactionSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        transaction = create_transaction(
            CreateTransactionCommand(
                transaction_id=data["transaction_id"],
                account_id=data["account_id"],
                amount=data["amount"],
                currency=data["currency"],
                transaction_type=data["transaction_type"],
                timestamp=data["timestamp"],
            ),
            actor=request.actor,
        )
        return Response(TransactionSerializer(transaction).data, status=status.HTTP_201_CREATED)
