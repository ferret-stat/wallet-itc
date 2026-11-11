import pytest
from httpx import ASGITransport, AsyncClient
from sqlalchemy.ext.asyncio import (
    async_sessionmaker,
    create_async_engine,
)

from app.core.config import settings
from app.database.db import Base, get_db
from app.main import app


@pytest.fixture
async def test_engine():
    engine = create_async_engine(
        settings.test_database_url,
        pool_pre_ping=True,
    )

    async with engine.begin() as connection:
        await connection.run_sync(Base.metadata.drop_all)
        await connection.run_sync(Base.metadata.create_all)

    yield engine

    async with engine.begin() as connection:
        await connection.run_sync(Base.metadata.drop_all)

    await engine.dispose()


@pytest.fixture
async def test_session_factory(test_engine):
    return async_sessionmaker(  
        bind=test_engine,
        expire_on_commit=False,
    )


@pytest.fixture
async def client(test_session_factory):

    async def override_get_db():
        async with test_session_factory() as session:
            yield session

    app.dependency_overrides[get_db] = override_get_db

    transport = ASGITransport(app=app)

    async with AsyncClient(
        transport=transport,
        base_url="http://test",
        headers={
            "X-API-Key": settings.api_key,
        },
    ) as test_client:
        yield test_client

    app.dependency_overrides.clear()
