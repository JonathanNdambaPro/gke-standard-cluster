from pathlib import Path

import duckdb
from dotenv import load_dotenv
from pydantic_settings import BaseSettings
from loguru import logger

FILE_DOTENV = Path(__file__).parents[1] / ".scripts.env"


load_dotenv(dotenv_path=FILE_DOTENV)

class Settings(BaseSettings):
    HMAC_KEY: str
    HMAC_PASSWORD: str


settings = Settings()
logger.info(settings.HMAC_KEY)
logger.info(settings.HMAC_PASSWORD)

con = duckdb.connect()
path_gcs_deltalake = ...
con.query(
    f"""
    CREATE SECRET (
        TYPE gcs,
        KEY_ID '{settings.HMAC_KEY}',
        SECRET '{settings.HMAC_PASSWORD}'
    );

    SELECT *
    FROM delta_scan('{ path_gcs_deltalake }')
    """  # noqa: S608
)
