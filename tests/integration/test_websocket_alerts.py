import pytest
from asgiref.sync import sync_to_async
from channels.testing import WebsocketCommunicator
from django.urls import reverse
from rest_framework.test import APIClient

from apps.alerts.models import Alert
from config.asgi import application


def _post_large_transaction(ingest_key: str) -> int:
    client = APIClient()
    response = client.post(
        reverse("transactions-list"),
        data={
            "transaction_id": "TXN_WS",
            "account_id": "ACC_WS",
            "amount": "25000.00",
            "currency": "USD",
            "transaction_type": "TRANSFER",
            "timestamp": "2026-06-01T10:00:00Z",
        },
        format="json",
        HTTP_X_API_KEY=ingest_key,
    )
    return response.status_code


@pytest.mark.django_db(transaction=True)
@pytest.mark.asyncio
async def test_websocket_receives_alert_on_large_transaction(
    ingest_client, ops_client, large_tx_rule
):
    _, ops_key = ops_client
    _, ingest_key = ingest_client
    communicator = WebsocketCommunicator(
        application, f"/ws/alerts/?api_key={ops_key}"
    )
    connected, _ = await communicator.connect()
    assert connected

    status_code = await sync_to_async(_post_large_transaction)(ingest_key)
    assert status_code == 201
    alert_count = await sync_to_async(Alert.objects.count)()
    assert alert_count == 1

    message = await communicator.receive_json_from()
    assert message["transaction_id"] == "TXN_WS"
    assert message["account_id"] == "ACC_WS"

    await communicator.disconnect()
