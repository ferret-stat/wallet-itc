import os
from urllib.parse import quote_plus

from dotenv import load_dotenv

load_dotenv()


class Settings:
    app_name: str = os.getenv("APP_NAME", "Wallet API")
    api_key: str = os.getenv("API_KEY")

    pg_user: str = os.getenv("POSTGRE_USER")
    pg_pass: str = os.getenv("POSTGRE_PASS")
    pg_name: str = os.getenv("POSTGRE_NAME")
    pg_host: str = os.getenv("POSTGRE_HOST", "localhost")
    pg_port: int = int(os.getenv("POSTGRE_PORT", "5432"))

    if not all([pg_user, pg_pass, pg_name]):
        raise ValueError("Missing PostgreSQL environment variables")

    database_url = (
        f"postgresql+asyncpg://"
        f"{quote_plus(pg_user)}:{quote_plus(pg_pass)}"
        f"@{pg_host}:{pg_port}/{pg_name}"
    )

    test_user: str = os.getenv("TEST_USER")
    test_pass: str = os.getenv("TEST_PASS")
    test_name: str = os.getenv("TEST_NAME")
    test_host: str = os.getenv("TEST_HOST", "localhost")
    test_port: int = int(os.getenv("TEST_PORT", "5432"))

    if not all([test_user, test_pass, test_name]):
        raise ValueError("Missing TestDB environment variables")

    test_database_url = (
        f"postgresql+asyncpg://"
        f"{quote_plus(test_user)}:{quote_plus(test_pass)}"
        f"@{test_host}:{test_port}/{test_name}"
    )


settings = Settings()