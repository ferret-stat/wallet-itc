import pytest


@pytest.mark.asyncio
async def test_deposit(client):
    create_response = await client.post(
        "/api/v1/wallets/create",
        json={},
    )

    wallet_id = create_response.json()["wallet_id"]

    response = await client.post(
        f"/api/v1/wallets/{wallet_id}/operation",
        json={
            "operation_type": "DEPOSIT",
            "amount": "1000.00",
        },
    )

    assert response.status_code == 200
    assert response.json()["balance"] == "1000.00"


@pytest.mark.asyncio
async def test_withdraw(client):
    create_response = await client.post(
        "/api/v1/wallets/create",
        json={},
    )

    wallet_id = create_response.json()["wallet_id"]

    await client.post(
        f"/api/v1/wallets/{wallet_id}/operation",
        json={
            "operation_type": "DEPOSIT",
            "amount": "1000.00",
        },
    )

    response = await client.post(
        f"/api/v1/wallets/{wallet_id}/operation",
        json={
            "operation_type": "WITHDRAW",
            "amount": "300.00",
        },
    )

    assert response.status_code == 200
    assert response.json()["balance"] == "700.00"


@pytest.mark.asyncio
async def test_withdraw_insufficient_funds(client):
    create_response = await client.post(
        "/api/v1/wallets/create",
        json={},
    )

    wallet_id = create_response.json()["wallet_id"]

    response = await client.post(
        f"/api/v1/wallets/{wallet_id}/operation",
        json={
            "operation_type": "WITHDRAW",
            "amount": "100.00",
        },
    )

    assert response.status_code == 409

    balance_response = await client.get(
        f"/api/v1/wallets/{wallet_id}"
    )

    assert balance_response.json()["balance"] == "0.00"


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "amount",
    ["0", "-100", "100.123"],
)
async def test_invalid_amount(client, amount):
    create_response = await client.post(
        "/api/v1/wallets/create",
        json={},
    )

    wallet_id = create_response.json()["wallet_id"]

    response = await client.post(
        f"/api/v1/wallets/{wallet_id}/operation",
        json={
            "operation_type": "DEPOSIT",
            "amount": amount,
        },
    )

    assert response.status_code == 422


@pytest.mark.asyncio
async def test_invalid_operation_type(client):
    create_response = await client.post(
        "/api/v1/wallets/create",
        json={},
    )

    wallet_id = create_response.json()["wallet_id"]

    response = await client.post(
        f"/api/v1/wallets/{wallet_id}/operation",
        json={
            "operation_type": "TRANSFER",
            "amount": "100.00",
        },
    )

    assert response.status_code == 422
