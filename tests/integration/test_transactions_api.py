import pytest
from django.urls import reverse
from rest_framework import status

from apps.transactions.models import Transaction


@pytest.mark.django_db
class TestTransactionsAPI:
    def test_create_transaction(self, api_client, ingest_client, auth_headers, large_tx_rule):
        _, key = ingest_client
        payload = {
            "transaction_id": "TXN001",
            "account_id": "ACC123",
            "amount": "5000.00",
            "currency": "USD",
            "transaction_type": "TRANSFER",
            "timestamp": "2026-06-01T10:00:00Z",
        }
        response = api_client.post(
            reverse("transactions-list"),
            data=payload,
            format="json",
            **auth_headers(key),
        )
        assert response.status_code == status.HTTP_201_CREATED
        assert Transaction.objects.filter(transaction_id="TXN001").exists()

    def test_duplicate_transaction_returns_409(
        self, api_client, ingest_client, auth_headers, large_tx_rule
    ):
        _, key = ingest_client
        payload = {
            "transaction_id": "TXN_DUP",
            "account_id": "ACC123",
            "amount": "100.00",
            "currency": "USD",
            "transaction_type": "TRANSFER",
            "timestamp": "2026-06-01T10:00:00Z",
        }
        api_client.post(
            reverse("transactions-list"), data=payload, format="json", **auth_headers(key)
        )
        response = api_client.post(
            reverse("transactions-list"), data=payload, format="json", **auth_headers(key)
        )
        assert response.status_code == status.HTTP_409_CONFLICT

    def test_list_transactions_with_pagination_and_filter(
        self, api_client, ingest_client, ops_client, auth_headers, large_tx_rule
    ):
        _, ingest_key = ingest_client
        _, ops_key = ops_client
        for i in range(3):
            api_client.post(
                reverse("transactions-list"),
                data={
                    "transaction_id": f"TXN_LIST_{i}",
                    "account_id": "ACC_FILTER",
                    "amount": "100.00",
                    "currency": "USD",
                    "transaction_type": "TRANSFER",
                    "timestamp": f"2026-06-0{i + 1}T10:00:00Z",
                },
                format="json",
                **auth_headers(ingest_key),
            )

        response = api_client.get(
            reverse("transactions-list") + "?account_id=ACC_FILTER&ordering=-timestamp&page_size=2",
            **auth_headers(ops_key),
        )
        assert response.status_code == status.HTTP_200_OK
        assert response.data["count"] == 3
        assert len(response.data["results"]) == 2

    def test_ingest_scope_cannot_list(self, api_client, ingest_client, auth_headers):
        _, key = ingest_client
        response = api_client.get(reverse("transactions-list"), **auth_headers(key))
        assert response.status_code == status.HTTP_403_FORBIDDEN
