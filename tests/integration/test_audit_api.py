import pytest
from django.urls import reverse
from rest_framework import status

from apps.audit.models import AuditLog


@pytest.mark.django_db
class TestAuditAPI:
    def test_list_audit_logs_after_rule_create(
        self, api_client, admin_client, auth_headers
    ):
        _, key = admin_client
        api_client.post(
            reverse("rules-list"),
            data={"name": "Audited Rule", "amount_threshold": "8000.00"},
            format="json",
            **auth_headers(key),
        )
        response = api_client.get(reverse("audit-logs-list"), **auth_headers(key))
        assert response.status_code == status.HTTP_200_OK
        assert response.data["count"] >= 1
        assert AuditLog.objects.filter(action="rule.created").exists()

    def test_ingest_cannot_read_audit(self, api_client, ingest_client, auth_headers):
        _, key = ingest_client
        response = api_client.get(reverse("audit-logs-list"), **auth_headers(key))
        assert response.status_code == status.HTTP_403_FORBIDDEN
