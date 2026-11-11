from uuid import uuid4

import pytest


@pytest.mark.asyncio
async def test_create_wallet_with_random_uuid(client):
    response = await client.post(
        "/api/v1/wallets/create",
        json={},
    )

    assert response.status_code == 201

    data = response.json()

    assert data["wallet_id"] is not None
    assert data["balance"] == "0.00"


@pytest.mark.asyncio
async def test_create_wallet_with_custom_uuid(client):
    wallet_id = str(uuid4())

    response = await client.post(
        "/api/v1/wallets/create",
        json={"wallet_id": wallet_id},
    )

    assert response.status_code == 201

    data = response.json()

    assert data["wallet_id"] == wallet_id
    assert data["balance"] == "0.00"


@pytest.mark.asyncio
async def test_create_wallet_duplicate_uuid(client):
    wallet_id = str(uuid4())

    first_response = await client.post(
        "/api/v1/wallets/create",
        json={"wallet_id": wallet_id},
    )

    second_response = await client.post(
        "/api/v1/wallets/create",
        json={"wallet_id": wallet_id},
    )

    assert first_response.status_code == 201
    assert second_response.status_code == 409


@pytest.mark.asyncio
async def test_create_wallet_invalid_uuid(client):
    response = await client.post(
        "/api/v1/wallets/create",
        json={"wallet_id": "invalid-uuid"},
    )

    assert response.status_code == 422
