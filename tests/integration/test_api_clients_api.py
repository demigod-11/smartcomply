import pytest
from django.urls import reverse
from rest_framework import status

from apps.audit.models import AuditLog
from apps.identity.models import ApiClient


@pytest.mark.django_db
class TestApiClientsAPI:
    def test_create_api_client_returns_key_once(
        self, api_client, bootstrap_client, auth_headers
    ):
        _, key = bootstrap_client
        response = api_client.post(
            reverse("api-clients-list"),
            data={"name": "new-service", "scopes": ["transactions:write"]},
            format="json",
            **auth_headers(key),
        )
        assert response.status_code == status.HTTP_201_CREATED
        assert "api_key" in response.data
        assert response.data["api_key"].startswith("sc_")
        assert AuditLog.objects.filter(action="api_client.created").exists()

        list_response = api_client.get(reverse("api-clients-list"), **auth_headers(key))
        names = {item["name"] for item in list_response.data["results"]}
        assert "new-service" in names
        result = next(r for r in list_response.data["results"] if r["name"] == "new-service")
        assert "api_key" not in result
        assert "key_hash" not in result

    def test_platform_admin_lists_all_clients(
        self, api_client, bootstrap_client, auth_headers, db
    ):
        _, bootstrap_key = bootstrap_client

        other_owner, _ = ApiClient.create_client(
            name="other-owner",
            scopes=["api_clients:write", "api_clients:read", "api_clients:manage"],
            created_by_id=None,
        )
        ApiClient.create_client(
            name="other-owner-child",
            scopes=["transactions:write"],
            created_by_id=other_owner.id,
        )

        api_client.post(
            reverse("api-clients-list"),
            data={"name": "bootstrap-child", "scopes": ["transactions:read"]},
            format="json",
            **auth_headers(bootstrap_key),
        )

        list_response = api_client.get(reverse("api-clients-list"), **auth_headers(bootstrap_key))
        names = {item["name"] for item in list_response.data["results"]}
        assert names == {
            "platform-admin",
            "other-owner",
            "other-owner-child",
            "bootstrap-child",
        }

    def test_non_platform_admin_lists_only_own_clients(
        self, api_client, bootstrap_client, auth_headers, db
    ):
        _, bootstrap_key = bootstrap_client

        create_resp = api_client.post(
            reverse("api-clients-list"),
            data={
                "name": "operator",
                "scopes": ["api_clients:write", "api_clients:read", "api_clients:manage"],
            },
            format="json",
            **auth_headers(bootstrap_key),
        )
        operator_key = create_resp.data["api_key"]

        api_client.post(
            reverse("api-clients-list"),
            data={"name": "operator-child", "scopes": ["transactions:write"]},
            format="json",
            **auth_headers(operator_key),
        )

        list_response = api_client.get(reverse("api-clients-list"), **auth_headers(operator_key))
        names = {item["name"] for item in list_response.data["results"]}
        assert names == {"operator-child"}
        assert "platform-admin" not in names
        assert "operator" not in names

    def test_duplicate_api_client_name_returns_409(
        self, api_client, bootstrap_client, auth_headers
    ):
        _, key = bootstrap_client
        payload = {"name": "dup-client", "scopes": ["transactions:read"]}
        api_client.post(
            reverse("api-clients-list"), data=payload, format="json", **auth_headers(key)
        )
        response = api_client.post(
            reverse("api-clients-list"), data=payload, format="json", **auth_headers(key)
        )
        assert response.status_code == status.HTTP_409_CONFLICT

    def test_deactivate_api_client(
        self, api_client, bootstrap_client, auth_headers
    ):
        _, key = bootstrap_client
        create_resp = api_client.post(
            reverse("api-clients-list"),
            data={"name": "to-deactivate", "scopes": ["transactions:read"]},
            format="json",
            **auth_headers(key),
        )
        client_id = create_resp.data["id"]
        raw_key = create_resp.data["api_key"]

        patch_resp = api_client.patch(
            reverse("api-clients-detail", kwargs={"id": client_id}),
            data={"is_active": False},
            format="json",
            **auth_headers(key),
        )
        assert patch_resp.status_code == status.HTTP_200_OK

        denied = api_client.get(reverse("transactions-list"), **auth_headers(raw_key))
        assert denied.status_code == status.HTTP_401_UNAUTHORIZED
