import asyncio

import pytest


@pytest.mark.asyncio
async def test_concurrent_deposits(client):
    create_response = await client.post(
        "/api/v1/wallets/create",
        json={},
    )

    wallet_id = create_response.json()["wallet_id"]

    async def deposit():
        return await client.post(
            f"/api/v1/wallets/{wallet_id}/operation",
            json={
                "operation_type": "DEPOSIT",
                "amount": "10.00",
            },
        )

    responses = await asyncio.gather(
        *(deposit() for _ in range(100))
    )

    assert all(
        response.status_code == 200
        for response in responses
    )

    balance_response = await client.get(
        f"/api/v1/wallets/{wallet_id}"
    )

    assert balance_response.status_code == 200
    assert balance_response.json()["balance"] == "1000.00"
