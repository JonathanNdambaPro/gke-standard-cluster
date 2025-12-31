from pathlib import Path

import duckdb
from dotenv import load_dotenv
from jinja2 import Template
from loguru import logger
from pydantic_settings import BaseSettings

FILE_DOTENV = Path(__file__).parents[1] / ".scripts.env"
FILE_SQL = Path(__file__).parent / "request" / "read_deltalake.sql"


load_dotenv(dotenv_path=FILE_DOTENV)


class Settings(BaseSettings):
    HMAC_KEY: str
    HMAC_PASSWORD: str


settings = Settings()
logger.info(settings.HMAC_KEY)
logger.info(settings.HMAC_PASSWORD)


con = duckdb.connect()
path_gcs_deltalake = "gs://event-driven/ingest_table/"

with open(FILE_SQL) as f:
    template = Template(f.read())


query = template.render(
    hmac_key=settings.HMAC_KEY,
    hmac_password=settings.HMAC_PASSWORD,
    path_gcs_deltalake=path_gcs_deltalake,
)


logger.info("SQL syntax is valid for DuckDB.")

data = con.query(query=query).df()

print(data)
