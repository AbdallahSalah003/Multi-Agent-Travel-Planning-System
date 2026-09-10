import os
import certifi
from dotenv import load_dotenv
from psycopg import AsyncConnection
from psycopg.rows import dict_row

load_dotenv()

os.environ["SSL_CERT_FILE"] = certifi.where()
os.environ["REQUESTS_CA_BUNDLE"] = certifi.where()

def _get_database_url():
    database_url = os.getenv("DATABASE_URL")

    if not database_url:
        raise ValueError(
            "DATABASE_URL is missing. Please add your Render PostgreSQL External Database URL to .env"
        )

    if "sslmode=" not in database_url:
        separator = "&" if "?" in database_url else "?"
        database_url = f"{database_url}{separator}sslmode=require"

    return database_url


async def get_db_conn():
    DATABASE_URL = _get_database_url()

    conn = await AsyncConnection.connect(
        conninfo=DATABASE_URL,
        autocommit=True,
        row_factory=dict_row
    )

    return conn 