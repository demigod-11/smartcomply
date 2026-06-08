import pytest
from django.urls import reverse
from rest_framework import status

from apps.audit.models import AuditLog
from apps.rules.models import Rule


@pytest.mark.django_db
class TestRulesAPI:
    def test_create_rule(self, api_client, admin_client, auth_headers):
        _, key = admin_client
        response = api_client.post(
            reverse("rules-list"),
            data={"name": "Custom Large Rule", "amount_threshold": "5000.00"},
            format="json",
            **auth_headers(key),
        )
        assert response.status_code == status.HTTP_201_CREATED
        assert response.data["amount_threshold"] == "5000.00"
        assert response.data["frequency_limit"] is None
        assert response.data["window_hours"] is None
        assert Rule.objects.filter(name="Custom Large Rule").exists()
        assert AuditLog.objects.filter(action="rule.created").exists()

    def test_duplicate_rule_returns_409(self, api_client, admin_client, auth_headers):
        _, key = admin_client
        payload = {"name": "Dup Rule", "amount_threshold": "1000.00"}
        api_client.post(
            reverse("rules-list"), data=payload, format="json", **auth_headers(key)
        )
        response = api_client.post(
            reverse("rules-list"), data=payload, format="json", **auth_headers(key)
        )
        assert response.status_code == status.HTTP_409_CONFLICT

    def test_list_rules(self, api_client, admin_client, auth_headers, large_tx_rule):
        _, key = admin_client
        response = api_client.get(reverse("rules-list"), **auth_headers(key))
        assert response.status_code == status.HTTP_200_OK
        assert response.data["count"] >= 1
