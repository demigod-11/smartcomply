import pytest
from django.urls import reverse
from rest_framework import status

from apps.alerts.models import Alert


@pytest.mark.django_db
class TestAlertsAPI:
    def test_alert_created_for_large_transaction(
        self, api_client, ingest_client, ops_client, auth_headers, large_tx_rule
    ):
        _, ingest_key = ingest_client
        _, ops_key = ops_client
        api_client.post(
            reverse("transactions-list"),
            data={
                "transaction_id": "TXN_ALERT",
                "account_id": "ACC123",
                "amount": "15000.00",
                "currency": "USD",
                "transaction_type": "TRANSFER",
                "timestamp": "2026-06-01T10:00:00Z",
            },
            format="json",
            **auth_headers(ingest_key),
        )

        assert Alert.objects.count() == 1
        response = api_client.get(reverse("alerts-list"), **auth_headers(ops_key))
        assert response.status_code == status.HTTP_200_OK
        assert response.data["count"] == 1
        assert response.data["results"][0]["rule"] == "Large Transaction Rule"

    def test_alerts_pagination_and_filter(
        self, api_client, ingest_client, ops_client, auth_headers, large_tx_rule
    ):
        _, ingest_key = ingest_client
        _, ops_key = ops_client
        for i in range(2):
            api_client.post(
                reverse("transactions-list"),
                data={
                    "transaction_id": f"TXN_A{i}",
                    "account_id": "ACC_ALERT",
                    "amount": "20000.00",
                    "currency": "USD",
                    "transaction_type": "TRANSFER",
                    "timestamp": f"2026-06-0{i + 1}T10:00:00Z",
                },
                format="json",
                **auth_headers(ingest_key),
            )

        response = api_client.get(
            reverse("alerts-list") + "?account_id=ACC_ALERT",
            **auth_headers(ops_key),
        )
        assert response.status_code == status.HTTP_200_OK
        assert response.data["count"] == 2
