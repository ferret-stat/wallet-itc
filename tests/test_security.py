import pytest

from httpx import ASGITransport, AsyncClient

from app.main import app


@pytest.mark.asyncio
async def test_missing_api_key():
    transport = ASGITransport(app=app)

    async with AsyncClient(
        transport=transport,
        base_url="http://test",
    ) as client:
        response = await client.post(
            "/api/v1/wallets/create",
            json={},
        )

    assert response.status_code == 401


@pytest.mark.asyncio
async def test_invalid_api_key():
    transport = ASGITransport(app=app)

    async with AsyncClient(
        transport=transport,
        base_url="http://test",
        headers={
            "X-API-Key": "wrong-key",
        },
    ) as client:
        response = await client.post(
            "/api/v1/wallets/create",
            json={},
        )

    assert response.status_code == 401
