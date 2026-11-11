from uuid import uuid4

import pytest


@pytest.mark.asyncio
async def test_get_wallet_balance(client):
    create_response = await client.post(
        "/api/v1/wallets/create",
        json={},
    )

    wallet_id = create_response.json()["wallet_id"]

    response = await client.get(
        f"/api/v1/wallets/{wallet_id}"
    )

    assert response.status_code == 200

    data = response.json()

    assert data["wallet_id"] == wallet_id
    assert data["balance"] == "0.00"


@pytest.mark.asyncio
async def test_get_nonexistent_wallet(client):
    wallet_id = str(uuid4())

    response = await client.get(
        f"/api/v1/wallets/{wallet_id}"
    )

    assert response.status_code == 404
