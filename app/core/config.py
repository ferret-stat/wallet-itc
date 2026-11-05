import os
from dotenv import load_dotenv
from urllib.parse import quote_plus

load_dotenv()


class Settings:
    app_name = os.getenv("APP_NAME", "Wallet API")

    pg_user = os.getenv("POSTGRE_USER")
    pg_pass = os.getenv("POSTGRE_PASS")
    pg_name = os.getenv("POSTGRE_NAME")
    pg_host = os.getenv("POSTGRE_HOST", "localhost")
    pg_port = int(os.getenv("POSTGRE_PORT", "5432"))

    if not all([pg_user, pg_pass, pg_name]):
        raise ValueError("Missing PostgreSQL environment variables")

    conn_string = (
        f"postgresql+asyncpg://"
        f"{quote_plus(pg_user)}:{quote_plus(pg_pass)}"
        f"@{pg_host}:{pg_port}/{pg_name}"
    )


settings = Settings()