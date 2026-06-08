import pytest
from django.urls import reverse
from rest_framework import status


@pytest.mark.django_db
class TestAuthScopes:
    def test_missing_api_key_returns_401(self, api_client):
        response = api_client.get(reverse("transactions-list"))
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_scope_matrix(
        self, api_client, ingest_client, ops_client, admin_client, bootstrap_client, auth_headers
    ):
        _, ingest_key = ingest_client
        _, ops_key = ops_client
        _, admin_key = admin_client
        _, bootstrap_key = bootstrap_client

        assert (
            api_client.post(
                reverse("transactions-list"),
                data={
                    "transaction_id": "TXN_SCOPE",
                    "account_id": "A1",
                    "amount": "100.00",
                    "currency": "USD",
                    "transaction_type": "TRANSFER",
                    "timestamp": "2026-06-01T10:00:00Z",
                },
                format="json",
                **auth_headers(ingest_key),
            ).status_code
            == status.HTTP_201_CREATED
        )

        assert (
            api_client.post(
                reverse("transactions-list"),
                data={
                    "transaction_id": "TXN_SCOPE2",
                    "account_id": "A1",
                    "amount": "100.00",
                    "currency": "USD",
                    "transaction_type": "TRANSFER",
                    "timestamp": "2026-06-01T10:00:00Z",
                },
                format="json",
                **auth_headers(ops_key),
            ).status_code
            == status.HTTP_403_FORBIDDEN
        )

        assert (
            api_client.get(reverse("api-clients-list"), **auth_headers(admin_key)).status_code
            == status.HTTP_403_FORBIDDEN
        )

        assert (
            api_client.get(reverse("api-clients-list"), **auth_headers(bootstrap_key)).status_code
            == status.HTTP_200_OK
        )
